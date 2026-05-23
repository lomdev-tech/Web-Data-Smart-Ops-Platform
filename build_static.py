#!/usr/bin/env python
"""
构建脚本：将 Django 项目转换为静态站点
在 Edge One Pages 部署前运行此脚本，预生成所有 JSON 数据文件
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'data' / 'nginx_2025.csv'
OUTPUT_DIR = BASE_DIR / 'output'

# 省份映射
PROVINCES_DIC = {
    "台湾省": "台湾", "山东省": "山东", "香港特别行政区": "香港",
    "江苏省": "江苏", "北京市": "北京", "云南省": "云南", "天津市": "天津",
    "甘肃省": "甘肃", "湖北省": "湖北", "安徽省": "安徽",
    "内蒙古自治区": "内蒙古", "浙江省": "浙江", "广东省": "广东",
    "陕西省": "陕西", "江西省": "江西", "四川省": "四川", "山西省": "山西",
    "福建省": "福建", "吉林省": "吉林", "贵州省": "贵州",
    "黑龙江省": "黑龙江", "湖南省": "湖南", "河南省": "河南", "上海市": "上海",
    "河北省": "河北", "重庆市": "重庆", "辽宁省": "辽宁",
    "澳门特别行政区": "澳门", "宁夏回族自治区": "宁夏", "西藏自治区": "西藏",
    "青海省": "青海", "新疆维吾尔自治区": "新疆", "广西壮族自治区": "广西",
    "海南省": "海南"
}

MOBILE_DIC = {
    "Android": "安卓", "iPhone": "苹果", "Windows Phone": "微软",
    "Symbian": "塞班", "BlackBerry": "黑莓", "Other": "其他",
    "mi": "小米", "huawei": "华为", "OPPO": "OPPO", "vivo": "vivo",
    "Meizu": "魅族", "zte": "中兴", "nokiya": "诺基亚"
}

BROWSER_DIC = {
    "Chrome": "谷歌", "Firefox": "火狐", "Safari": "苹果", "Edge": "Edge",
    "Opera": "Opera", "QQ": "QQ", "Sogou": "搜狗", "Baidu": "百度",
    "Yandex": "Yandex", "UC": "UC", "360": "360", "Other": "其他"
}


def load_data():
    df = pd.read_csv(DATA_FILE)
    df.columns = ['ip', 'province', 'city', 'access', 'mobile',
                   'browser', 'gender', 'age', 'method', 'url', 'status']
    median_age = df['age'].median()
    df.fillna(value={'age': median_age}, inplace=True)
    mode_age = df['age'].mode()[0]
    df['age'] = np.where(~df['age'].between(0, 120), mode_age, df['age'])
    df['age'] = df['age'].apply(np.int64)
    return df


def generate_province(df):
    data = df.groupby('province').size()
    return [{'province': PROVINCES_DIC.get(k, k), 'count': int(v)} for k, v in data.items()]


def generate_city(df):
    city_data = df.groupby('city').size()
    return {'city': list(city_data.index), 'count': [int(v) for v in city_data.values]}


def generate_minute(df):
    data_copy = df.copy()
    data_copy['access'] = data_copy['access'].str[11:16]
    use_data = data_copy.groupby('access').size()
    return {'minute': list(use_data.index), 'count': [int(v) for v in use_data.values]}


def generate_gender(df):
    gender_data = df.groupby('gender').size()
    return [{'gender': g, 'count': int(c)} for g, c in gender_data.items()]


def generate_mobile(df):
    mobile_data = df.groupby('mobile').size()
    return [{'mobile': MOBILE_DIC.get(m, m), 'count': int(c)} for m, c in mobile_data.items()]


def generate_status(df):
    status_data = df.groupby('status').size()
    return {'code': [int(s) for s in status_data.index], 'count': [int(c) for c in status_data.values]}


def generate_browser(df):
    browser_data = df.groupby('browser').size()
    return {BROWSER_DIC.get(b, b): int(c) for b, c in browser_data.items()}


def generate_age_group(df):
    data = df.copy()
    bins = [0, 18, 30, 45, 60, 150]
    labels = ['0-18', '19-30', '31-45', '46-60', '60+']
    data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels)

    age_group_counts = data['age_group'].value_counts().reindex(labels, fill_value=0)
    age_url_data = data.groupby(['age_group', 'url'], observed=False).size().unstack(fill_value=0)
    age_url_data = age_url_data.reindex(labels, fill_value=0)

    result = {
        'age_groups': labels,
        'counts': [int(age_group_counts[g]) for g in labels],
        'url_preference': {}
    }
    for url in data['url'].unique():
        if url in age_url_data.columns:
            result['url_preference'][url] = [int(age_url_data.loc[g, url]) for g in labels]
        else:
            result['url_preference'][url] = [0] * len(labels)
    return result


def generate_prophet(df):
    dataset_new = df.copy()
    dataset_new["access"] = dataset_new["access"].str[:19]
    result = dataset_new.groupby('access').size()

    ds, y = [], []
    for minute, value in result.items():
        ds.append(minute)
        y.append(value)

    if len(y) < 10:
        return {'xAxis': [], 'yAxis': []}

    window_size = min(20, len(y) // 3)
    ma = pd.Series(y).rolling(window=window_size, min_periods=1).mean()

    last_ma = ma.iloc[-1]
    trend = (ma.iloc[-1] - ma.iloc[-min(10, len(ma))]) / min(10, len(ma))

    predictions = [max(0, int(round(last_ma + trend * (i + 1)))) for i in range(60)]

    last_time = pd.to_datetime(ds[-1])
    future_times = [(last_time + pd.Timedelta(seconds=i + 1)).strftime('%H:%M:%S') for i in range(60)]

    return {'xAxis': future_times, 'yAxis': predictions}


def main():
    print("开始构建静态数据文件...")

    df = load_data()
    print(f"数据加载成功，共 {len(df)} 条记录")

    OUTPUT_DIR.mkdir(exist_ok=True)

    generators = {
        'province.json': generate_province,
        'city.json': generate_city,
        'minute.json': generate_minute,
        'gender.json': generate_gender,
        'mobile.json': generate_mobile,
        'status.json': generate_status,
        'browser.json': generate_browser,
        'age_group.json': generate_age_group,
        'prophet.json': generate_prophet,
    }

    for filename, generator in generators.items():
        data = generator(df)
        output_file = OUTPUT_DIR / filename
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  已生成 {filename}")

    # 复制静态资源
    import shutil
    static_output = OUTPUT_DIR / 'static'
    if static_output.exists():
        shutil.rmtree(static_output)
    shutil.copytree(BASE_DIR / 'static', static_output)
    print("  已复制静态资源")

    # 复制静态版本的 index.html
    import shutil
    shutil.copy(BASE_DIR / 'static_index.html', OUTPUT_DIR / 'index.html')
    print("  已生成 index.html")

    # 生成 edgeone.json 配置
    edgeone_config = {
        "name": "djangodemo",
        "outputDirectory": "./output",
        "routes": [
            {"src": "/(.*)", "dest": "/index.html"}
        ]
    }
    with open(OUTPUT_DIR / 'edgeone.json', 'w', encoding='utf-8') as f:
        json.dump(edgeone_config, f, indent=2)
    print("  已生成 edgeone.json")

    print("\n构建完成！静态文件已输出到 output/ 目录")
    print("请将 output/ 目录部署到 Edge One Pages")


if __name__ == '__main__':
    main()
