# Django 项目 Vercel 官网部署指导书

适用项目：`Djangodemo`  
部署方式：Vercel 官网新建项目并导入 GitHub 仓库  
当前状态：部署所需文件已在仓库中准备完成

## 1. 已准备好的部署文件

仓库已经补齐以下 Vercel 部署文件：

- `requirements.txt`：声明 Django、pandas、numpy、WhiteNoise 依赖。
- `.python-version`：指定 Python 3.12。
- `wsgi.py`：提供 Vercel 可识别的根级 WSGI 入口，并暴露 `app`。
- `vercel.json`：配置构建命令 `python manage.py collectstatic --noinput`，并排除虚拟环境、训练日志、模型检查点等无关文件。
- `.vercelignore`：减少无关文件进入 Vercel 构建上下文。
- `static/js/*.map`：补齐 JS sourcemap，避免 WhiteNoise 构建失败。

代码也已调整：

- `Djangodemo/settings.py` 默认使用生产配置，`DEBUG` 默认关闭。
- `Djangodemo/settings.py` 使用 Django 6 推荐的 `STORAGES` 配置 WhiteNoise。
- `station_data_analysis/DataManager.py` 使用项目根目录定位 `data/nginx_2025.csv`，不再依赖当前运行目录。
- `station_data_analysis/views.py` 移除了 `/minute/` 接口中的调试日志输出。

## 2. GitHub 推送前确认

部署前请确保这些改动已经提交并推送到 GitHub。

建议提交命令：

```powershell
git status
git commit -m "Prepare Django project for Vercel deployment"
git push
```

本地训练检查点 `.lr_find_d215b1f0-8e8a-43f6-8d43-ff90a7566ec6.ckpt` 已建议从 Git 跟踪中移除，避免拖慢 Vercel 构建。文件会保留在本地，不需要上传到 GitHub。

## 3. Vercel 官网导入步骤

1. 打开 [Vercel 官网](https://vercel.com/)。
2. 使用 GitHub 账号登录。
3. 点击 `Add New...`。
4. 选择 `Project`。
5. 在 `Import Git Repository` 中选择本项目仓库。
6. `Root Directory` 保持为包含 `manage.py` 的仓库根目录。
7. 其他构建配置保持默认，因为仓库中的 `vercel.json` 已经配置好。
8. 点击 `Deploy`。

首次部署不强制要求手动配置环境变量，仓库已有默认值可以跑起来。

生产环境上线后，建议在 Vercel 的 `Project Settings -> Environment Variables` 中补充：

```txt
SECRET_KEY=替换为你自己的随机密钥
DEBUG=False
ALLOWED_HOSTS=.vercel.app,你的正式域名
CSRF_TRUSTED_ORIGINS=https://*.vercel.app,https://你的正式域名
```

## 4. 部署后验证

部署成功后访问 Vercel 分配的域名，检查：

- `/` 首页是否正常打开。
- `/hello/` 是否返回 `Hello World!`。
- `/minute/` 是否返回 JSON。
- `/city/` 是否返回 JSON。
- `/status/` 是否返回 JSON。

如果首页打开但图表不显示，打开浏览器开发者工具的 Network 面板，确认上述接口是否返回 200。

## 5. 本地已完成的校验

已在本地完成：

- Python 文件语法编译。
- `python manage.py check`。
- `python manage.py collectstatic --noinput --clear`。
- Django 测试客户端访问 `/`、`/hello/`、`/minute/`、`/city/`、`/status/`。

这些检查均已通过。

## 6. 官方参考

- Vercel Django 零配置支持公告：<https://vercel.com/changelog/zero-configuration-django-support>
- Vercel Git 部署文档：<https://vercel.com/docs/deployments/git>
- Vercel Python Runtime 文档：<https://vercel.com/docs/functions/runtimes/python>
- Vercel 环境变量文档：<https://vercel.com/docs/environment-variables>
