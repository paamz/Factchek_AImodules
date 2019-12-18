# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 17:49:44 2019

@author: IT2
"""
from flask_restful import Api
from app import app
from .TextAImodule import factchekText
from .ImageAImodule import db_ImageFC
from .VideoAImodule import VideoFC
from .ImageAImodule_g import g_ImageFC

api = Api(app)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'db_factcheck'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

api.add_resource(factchekText,"/factchekText")
api.add_resource(db_ImageFC,"/db_ImageFC")
api.add_resource(g_ImageFC,"/g_ImageFC")
api.add_resource(VideoFC,"/VideoFC")
