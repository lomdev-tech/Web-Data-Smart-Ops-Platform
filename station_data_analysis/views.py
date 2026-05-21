from django.shortcuts import render
# 导入httpresponse包
from django.http import HttpResponse, JsonResponse
import pandas as pd
from station_data_analysis.DataManager import DataManager
# 全局成员
PROVINCES_DIC = {
    "台湾省": "台湾",
    "山东省": "山东",
    "香港特别行政区": "香港",
    "江苏省": "江苏",
    "北京市": "北京",
    "云南省": "云南",
    "天津市": "天津",
    "甘肃省": "甘肃",
    "湖北省": "湖北",
    "安徽省": "安徽",
    "内蒙古自治区": "内蒙古",
    "浙江省": "浙江",
    "广东省": "广东",
    "陕西省": "陕西",
    "江西省": "江西",
    "四川省": "四川",
    "山西省": "山西",
    "福建省": "福建",
    "吉林省": "吉林",
    "贵州省": "贵州",
    "黑龙江省": "黑龙江",
    "湖南省": "湖南",
    "河南省": "河南",
    "上海市": "上海",
    "河北省": "河北",
    "重庆市": "重庆",
    "辽宁省": "辽宁",
    "澳门特别行政区": "澳门",
    "宁夏回族自治区": "宁夏",
    "西藏自治区": "西藏",
    "青海省": "青海",
    "新疆维吾尔自治区": "新疆",
    "广西壮族自治区": "广西",
    "海南省": "海南"
}
MOBILE_DIC = {
    "Android": "安卓",
    "iPhone": "苹果",
    "Windows Phone": "微软",
    "Symbian": "塞班",
    "BlackBerry": "黑莓",
    "Other": "其他",
    "mi": "小米",
    "huawei": "华为",
    "OPPO": "OPPO",
    "vivo": "vivo",
    "Meizu": "魅族",
    "zte": "中兴",
    "nokiya": "诺基亚"
}
BROWSER_DIC = {
    "Chrome": "谷歌",
    "Firefox": "火狐",
    "Safari": "苹果",
    "Edge": "Edge",
    "Opera": "Opera",
    "QQ": "QQ",
    "Sogou": "搜狗",
    "Baidu": "百度",
    "Yandex": "Yandex",
    "UC": "UC",
    "360": "360",
    "Other": "其他"
}
origin_data = DataManager.get_data()
# 写一个hello页面
def hello(request):
    return HttpResponse("Hello World!")
# Create your views here.
def home(request):
    return render(request, 'index.html')
def visited_minute_count(request):
    result = {
        'minute': [],
        'count': []

    }
    data_copy = origin_data.copy()
    data_copy['access'] = data_copy['access'].str[11:16]
    use_data = data_copy.groupby('access').size()
    for k, v in use_data.items():
        result['minute'].append(k)
        result['count'].append(v)
    print(result)
    return JsonResponse(result,safe=False)
def count_province(request):
    results = [

        # {'province':[],
        #  'count':[]}
    ]
    data = origin_data.groupby('province').size()
    for k,v in data.items():
        results.append({'province':PROVINCES_DIC[k],'count':v})
    return JsonResponse(results,safe=False)

def count_city(request):
    result = {
        'city': [],
        'count': []
    }
    city_data = origin_data.groupby('city').size()
    
    for k, v in city_data.items():
        result['city'].append(k)
        result['count'].append(int(v))
    
    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})

def count_gender(request):
    results = []
    gender_data = origin_data.groupby('gender').size()
    
    for gender, count in gender_data.items():
        results.append({
            'gender': gender,
            'count': int(count)
        })
    
    return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})

def count_mobile(request):

    results = []
    mobile_data = origin_data.groupby('mobile').size()
    
    for mobile, count in mobile_data.items():
        mobile_name = MOBILE_DIC.get(mobile, mobile)
        results.append({
            'mobile': mobile_name,
            'count': int(count)
        })
    
    return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})

def count_status(request):

    result = {
        'code': [],
        'count': []
    }
    status_data = origin_data.groupby('status').size()
    for status, count in status_data.items():
        result['code'].append(int(status))
        result['count'].append(int(count))
    
    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})

def count_browser(request):

    result = {}
    browser_data = origin_data.groupby('browser').size()
    
    for browser, count in browser_data.items():
        browser_name = BROWSER_DIC.get(browser, browser)
        result[browser_name] = int(count)
    
    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})


def get_all_data(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 100))
    if page_size > 1000:
        page_size = 1000
    
    # 计算起始和结束位置
    start = (page - 1) * page_size
    end = start + page_size
    
    # 获取总记录数
    total_count = len(origin_data)
    
    # 分页获取数据
    paginated_data = origin_data.iloc[start:end]
    
    # 将DataFrame转换为字典列表
    data_list = paginated_data.to_dict(orient='records')
    
    # 构建响应数据
    response_data = {
        'total': total_count,
        'page': page,
        'page_size': page_size,
        'total_pages': (total_count + page_size - 1) // page_size,
        'data': data_list
    }
    
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

def count_age_group(request):
    """年龄段分布统计"""
    data = origin_data.copy()
    # 定义年龄段分组
    bins = [0, 18, 30, 45, 60, 150]
    labels = ['0-18', '19-30', '31-45', '46-60', '60+']
    data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels)

    # 统计各年龄段访问量
    age_group_counts = data['age_group'].value_counts().reindex(labels, fill_value=0)

    # 统计各年龄段偏好页面
    age_url_data = data.groupby(['age_group', 'url'], observed=False).size().unstack(fill_value=0)
    age_url_data = age_url_data.reindex(labels, fill_value=0)

    result = {
        'age_groups': labels,
        'counts': [int(age_group_counts[g]) for g in labels],
        'url_preference': {}
    }

    # 为每个年龄段添加页面偏好数据
    for url in data['url'].unique():
        if url in age_url_data.columns:
            result['url_preference'][url] = [int(age_url_data.loc[g, url]) for g in labels]
        else:
            result['url_preference'][url] = [0] * len(labels)

    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})


def prophet(request):
    """使用移动平均进行简单预测"""
    dataset_new = origin_data.copy()
    dataset_new["access"] = dataset_new["access"].str[:19]
    result = dataset_new.groupby('access').size()

    ds = []
    y = []
    for minute, value in result.items():
        ds.append(minute)
        y.append(value)

    if len(y) < 10:
        return JsonResponse(data={'error': '数据量不足'}, status=400)

    # 使用移动平均进行预测
    window_size = min(20, len(y) // 3)  # 窗口大小
    ma = pd.Series(y).rolling(window=window_size, min_periods=1).mean()

    # 预测未来60个时间点（基于最后的移动平均值和趋势）
    last_ma = ma.iloc[-1]
    trend = (ma.iloc[-1] - ma.iloc[-min(10, len(ma))]) / min(10, len(ma))  # 计算趋势

    predictions = []
    for i in range(60):
        pred = last_ma + trend * (i + 1)
        predictions.append(max(0, int(round(pred))))

    # 生成时间标签
    last_time = pd.to_datetime(ds[-1])
    future_times = [(last_time + pd.Timedelta(seconds=i+1)).strftime('%H:%M:%S') for i in range(60)]

    res = {
        'xAxis': future_times,
        'yAxis': predictions
    }
    return JsonResponse(res, safe=False)
