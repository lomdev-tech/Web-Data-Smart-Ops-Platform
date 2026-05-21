from django.urls import path
from . import views
# 配置二级路由
urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('',views.home),
    path('minute/',views.visited_minute_count),
    path('province/',views.count_province),
    path('city/', views.count_city, name='count_city'),
    path('gender/', views.count_gender, name='count_gender'),
    path('mobile/', views.count_mobile, name='count_mobile'),
    path('browser/', views.count_browser, name='count_browser'),
    path('status/', views.count_status, name='count_status'),
    path('age_group/', views.count_age_group, name='count_age_group'),
    path('prophet/', views.prophet, name='predict_prophet'),
    path('list/', views.get_all_data, name='get_all_data')
]
