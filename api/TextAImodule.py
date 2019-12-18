# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:27:58 2019

@author: IT2
"""
from flask_restful import Resource
from flask import Flask,request,jsonify
import requests
from app import app
import os
from apiclient.discovery import build

from flask_mysqldb import MySQL
# =============================================================================
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_DB'] = 'db_factcheck'
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"
# =============================================================================
mysql = MySQL(app)

api_key = '#################################'
resource = build("seach_engine name",'v1', developerKey=api_key,cache_discovery=True).cse()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'%%%%%%5.json' 

class factchekText(Resource):
    def post(self):
            try:
                _json = request.json
                Text = _json['fact_query']
                # Description = _json['Description']
                cur = mysql.connection.cursor()
        #         sql = "SELECT * from facttext WHERE Title LIKE %s OR  description LIKE %s"
        #         args = [Text]
        #         print(args)
        #         cur.execute(sql,(args,)) 
                cur.execute("SELECT * from facttext WHERE Title LIKE '%%%s%%' OR  description LIKE '%%%s%%'"%(Text,Text)) 
                #results = cur.fetchall()
                #print(results)
                db_result = cur.fetchall()
                 #print('by db...',db_result)
                if db_result:
                     print('by db111...',db_result)
                     return jsonify(db_result)               
                elif True:
                     #def factchek():
                     _query = str.encode(Text)
                     print(_query)
                     headers = {
                          'Accept': 'application/json',
                     }
                     params = (
                          ('query', _query),
                          ('key', 'your_api_key'),
                     )
                     print(params)
                     response = requests.get('https://factchecktools.googleapis.com/v1alpha1/claims:search', headers=headers, params=params)
                     g_result =  response.json()
                     if g_result:
                         print('by gFact..',g_result)
                         return  g_result
                     else:
                         #def cust_search():
                         #itext = request.json['text']
                         print('@@@@@@@@@@@@@@inside custome serach......',Text)
                         s_result = []
                         result = resource.list(q=Text, cx='017795299087749107028:onvo85h2owu',searchType='image').execute()
                         for item in result['items']:
                         #s_result += (item['title'], item['link'])
                             for i in range(len(result['items'])):
                                 res = dict((k, item[k]) for k in ['title','link','image'] if k in item) 
                                 s_result.append(res)  
                                 return jsonify(s_result) 
                                  
            except Exception as e:
                print(e)
            
            finally:
                cur.close() 
        
