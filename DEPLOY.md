# 网站运营数链智维平台 - 部署指南

## 项目简介

基于Django的数据可视化大屏项目，使用ECharts展示Nginx日志数据分析结果。

### 技术栈

- Python 3.12
- Django 6.0
- Pandas + NumPy
- ECharts (前端可视化)
- NeuralProphet (时间序列预测)

---

## 一、本地开发环境搭建

### 1.1 克隆项目

```bash
git clone https://github.com/你的用户名/项目名.git
cd 项目名
```

### 1.2 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 1.3 安装依赖

```bash
pip install -r requirements.txt
```

### 1.4 启动开发服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 查看效果

---

## 二、Vercel 部署

### 2.1 准备工作

#### 注册Vercel账号

1. 访问 https://vercel.com
2. 点击 "Sign Up"
3. 选择 "Continue with GitHub" 用GitHub账号登录

#### 安装Vercel CLI

```bash
npm install -g vercel
```

> 如果没有Node.js，先安装：https://nodejs.org/

### 2.2 登录Vercel

```bash
vercel login
```

浏览器会自动打开，授权登录即可。

### 2.3 上传项目到GitHub

```bash
# 在项目目录执行
git init
git add .
git commit -m "初始提交"
git remote add origin https://github.com/你的用户名/项目名.git
git push -u origin main
```

### 2.4 部署到Vercel

#### 方式一：通过Vercel网站（推荐新手）

1. 登录 https://vercel.com/dashboard
2. 点击 "Add New..." → "Project"
3. 选择 "Import Git Repository"
4. 选择你的GitHub仓库
5. 点击 "Deploy"

#### 方式二：通过命令行

```bash
# 在项目目录执行
vercel

# 按提示操作：
# Set up and deploy? → Y
# Which scope? → 选择你的账号
# Link to existing project? → N
# Project name? → 回车默认或输入自定义名称
# Directory is empty? → N
# Want to override settings? → N
```

### 2.5 访问部署结果

部署完成后会显示访问地址：

```
https://项目名.vercel.app
```

---

## 三、Vercel 配置说明

### 3.1 vercel.json

```json
{
  "builds": [
    {
      "src": "Djangodemo/wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "Djangodemo/wsgi.py"
    }
  ]
}
```

### 3.2 api/index.py

Vercel的入口文件，负责加载Django WSGI应用。

### 3.3 requirements.txt

Python依赖列表，Vercel会自动安装。

---

## 四、环境变量配置

### 4.1 在Vercel网站配置

1. 进入项目设置 → "Environment Variables"
2. 添加以下变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| SECRET_KEY | 你的密钥 | Django密钥 |
| DEBUG | False | 关闭调试模式 |

### 4.2 生成安全密钥

```python
# 在Python中执行
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 五、已知问题与解决方案

### 5.1 NeuralProphet/PyTorch 体积过大

**问题**：Vercel免费版限制250MB，PyTorch+NeuralProphet超过限制

**解决方案**：

#### 方案A：移除预测功能

注释掉 `index.html` 中预测图表的相关代码：

```html
<!-- 注释掉这段 -->
<!--
<div class="chart-container line2-container">
    <div class="chart-title">未来一小时网站访问量预测</div>
    <div class="chart" id="line2-chart"></div>
</div>
-->
```

同时注释掉对应的JS代码。

#### 方案B：使用轻量预测库

替换NeuralProphet为 `statsmodels`：

```bash
# requirements.txt 中替换
statsmodels>=0.14
```

### 5.2 CSV数据文件

Vercel是无服务器环境，文件系统是只读的。

**解决方案**：将CSV数据打包到项目中上传

```bash
# 确保 data/nginx_2025.csv 在项目根目录
git add data/nginx_2025.csv
git commit -m "添加数据文件"
git push
```

### 5.3 SQLite数据库

Vercel每次部署会重置文件系统，SQLite数据会丢失。

**解决方案**：
- 如果只是展示静态数据，不需要数据库
- 如需持久化，使用外部数据库（如Supabase、PlanetScale）

---

## 六、自定义域名

### 6.1 在Vercel添加域名

1. 进入项目设置 → "Domains"
2. 输入你的域名
3. 按提示配置DNS

### 6.2 DNS配置

在域名服务商添加：

```
类型: CNAME
名称: @ 或 www
值: cname.vercel-dns.com
```

---

## 七、项目结构

```
Djangodemo/
├── api/
│   └── index.py          # Vercel入口
├── data/
│   └── nginx_2025.csv    # 数据文件
├── Djangodemo/           # Django项目配置
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/               # 静态资源
│   ├── css/
│   └── js/
├── station_data_analysis/ # 主应用
│   ├── views.py
│   ├── urls.py
│   └── DataManager.py
├── templates/
│   └── index.html        # 主页面
├── vercel.json           # Vercel配置
├── requirements.txt      # Python依赖
└── manage.py
```

---

## 八、API接口列表

| 路径 | 说明 |
|------|------|
| `/` | 主页面 |
| `/province/` | 省份访问量 |
| `/city/` | 城市访问量Top10 |
| `/minute/` | 分钟级访问趋势 |
| `/gender/` | 性别分布 |
| `/mobile/` | 手机类型分布 |
| `/status/` | 状态码分布 |
| `/browser/` | 浏览器分布 |
| `/age_group/` | 年龄段分布 |
| `/prophet/` | 时间序列预测 |
| `/list/` | 分页数据列表 |

---

## 九、常见问题

### Q: 部署后页面空白？

检查浏览器控制台(F12)是否有报错，常见原因：
- 静态文件路径问题
- API接口返回错误

### Q: API接口500错误？

检查Vercel的Function日志：
1. 进入项目 → "Functions"
2. 查看错误日志

### Q: 如何更新部署？

```bash
git add .
git commit -m "更新内容"
git push
```

Vercel会自动重新部署。

---

## 十、联系方式

如有问题，请通过以下方式联系：

- GitHub Issues: https://github.com/你的用户名/项目名/issues
- Email: 你的邮箱

---

## 许可证

MIT License
