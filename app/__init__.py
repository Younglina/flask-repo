# app/__init__.py
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

# 导入路由
from app import routes
