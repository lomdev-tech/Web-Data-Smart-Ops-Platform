import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django settings模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangodemo.settings')

# 导入Django并设置
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel需要的handler
def handler(request):
    return application(request)
