# Edge One Pages 部署指南

## 快速部署步骤

### 1. 本地构建

```bash
# 安装依赖（如果还没有）
pip install -r requirements.txt

# 运行构建脚本，生成静态文件
python build_static.py
```

构建完成后，静态文件会输出到 `output/` 目录。

### 2. 推送到 GitHub

```bash
git add .
git commit -m "Add Edge One Pages deployment files"
git push
```

### 3. 在 Edge One Pages 导入部署

1. 登录 [Edge One Pages 控制台](https://pages.edgeone.cn/)
2. 点击「新建项目」
3. 选择「导入已有仓库」
4. 授权并选择你的 GitHub 仓库
5. 配置构建设置：
   - **构建命令**: `python build_static.py`
   - **输出目录**: `output`
   - **安装命令**: `pip install -r requirements.txt`
6. 点击「部署」

### 4. 自定义域名（可选）

在项目设置中绑定你的自定义域名。

## 项目结构说明

```
├── edgeone.json          # Edge One Pages 配置文件
├── build_static.py       # 构建脚本，生成静态 JSON 数据
├── static_index.html     # 静态版前端页面（直接加载 JSON）
├── output/               # 构建输出目录（部署到 Edge One Pages）
│   ├── index.html
│   ├── province.json
│   ├── city.json
│   ├── minute.json
│   ├── gender.json
│   ├── mobile.json
│   ├── status.json
│   ├── browser.json
│   ├── age_group.json
│   ├── prophet.json
│   └── static/
│       ├── js/
│       └── css/
├── templates/            # Django 模板（本地开发用）
├── static/               # 静态资源
└── data/                 # 数据文件
```

## 工作原理

1. **构建阶段**: `build_static.py` 读取 CSV 数据，预生成所有 JSON 文件
2. **部署阶段**: Edge One Pages 将 `output/` 目录部署为静态站点
3. **访问阶段**: 前端直接加载静态 JSON 文件，无需后端服务器

## 注意事项

- 数据是静态的（基于 nginx_2025.csv），如需更新数据，需重新运行构建并部署
- 项目不再需要 Django 运行时，所有数据在构建时预处理
- 预测功能使用移动平均算法，在构建时预计算

## 本地开发

如需本地开发调试 Django 版本：

```bash
python manage.py runserver
```

访问 http://localhost:8000
