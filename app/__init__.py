# app/__init__.py
from flask import Flask

# 通过指定static_folder参数来告诉Flask静态文件所在的目录
# 指定template_folder,直接渲染Vue打包后的index.html
# 使用static_url_path参数可以设置静态文件请求的URL前缀。如果不指定，Flask会使用默认的/static
app = Flask(__name__, static_folder='../static', template_folder='../static', static_url_path='/flask')
app.config.from_object(__name__)

# 导入路由
from app import routes
