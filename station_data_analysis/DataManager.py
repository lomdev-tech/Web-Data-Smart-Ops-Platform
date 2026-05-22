import pandas as pd
import  numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / 'data' / 'nginx_2025.csv'

class DataManager:
    _instance = None
    _dataset = None
    #初始化构造器
    def __init__(self):
        if self._dataset is None:
            self.load_data()
    def __new__(cls,*args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def load_data(cls):
        try:
            cls._dataset = pd.read_csv(DATA_FILE)
            pd.set_option('display.max_columns', None)
            column_name = ['ip', 'province', 'city', 'access', 'mobile',
                           'browser', 'gender', 'age', 'method', 'url',
                           'status']
            cls._dataset.columns = column_name
            # 1. 处理 age 列空值：用中位数填充
            median_age = cls._dataset['age'].median()
            cls._dataset.fillna(value={'age': median_age}, inplace=True)
            mode_age = cls._dataset['age'].mode()[0]  # mode 返回 Series，取第一个�?
            cls._dataset['age'] = np.where(~cls._dataset['age'].between(0, 120), mode_age, cls._dataset['age'])
            cls._dataset['age'] = cls._dataset['age'].apply(np.int64)
            print("数据加载成功!")
            # print("数据加载成功!预览前五行\n")
            # print(cls._dataset.head())
        except FileNotFoundError as e:
            print(f"错误:未找到文件{e.filename}")
            raise
        except Exception as e:
            print("数据加载失败:", str(e))
            raise

    @classmethod
    def get_data(cls):
        if cls._dataset is None:
            cls.load_data()
        return cls._dataset
    @classmethod
    def get_columns(self, column_name):
        if column_name not in self._dataset.columns:
            raise ValueError(f"列名{column_name}不存在")
        return self._dataset[column_name]
    @classmethod
    def get_statistics(self):
        if self._dataset is None:
            self.load_data()
        return self._dataset.describe(include='all')
    @classmethod
    def filter_by_province(self, province):
        if self._dataset is None:
            self.load_data()
        return self._dataset[self._dataset['province'] == province]
    @classmethod
    def get_age_gruops(self):
        if self._dataset is None:
            self.load_data()
        bins = [0, 18, 30, 45, 60, 100]
        labels = ['0-18', '19-30', '31-45', '46-60', '60+']
        age_groups = pd.cut(self._dataset['age'], bins=bins, labels=labels,right=False)
        return age_groups.value_counts().sort_index()
    @classmethod
    def get_status_counts(self):
        if self._dataset is None:
            self.load_data()
        return self._dataset['status'].value_counts().sort_index()
    @classmethod
    def get_top_cities(self, n=10):
        if self._dataset is None:
            self.load_data()
        return self._dataset['city'].value_counts().head(n)
    @classmethod
    def save_data(self, filename):
        if self._dataset is None:
            self.load_data()
        try:
            self._dataset.to_csv(filename, index=False)
            print(f"数据已保存在{filename}")
        except Exception as e:
            print("数据保存失败:", str(e))
