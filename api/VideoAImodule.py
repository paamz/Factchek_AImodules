# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 17:34:47 2019

@author: IT2
"""
import os
from flask_restful import Resource
from flask import Flask,jsonify,request
from apiclient.discovery import build
from google.cloud import videointelligence
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToDict
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'db_factcheck'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

api_key = 'AIzaSyDM9hLPKnx6yo-l8FyVthqefYA69JXMIbg'
resource = build("customsearch",'v1', developerKey=api_key).cse()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'crescendoFactchek.json' 
client = vision.ImageAnnotatorClient()

mysql = MySQL(app)

class VideoFC(Resource):
    #def analyze_labels():
    def post(self):            
        labels = []
        path = request.files['ivideo']
        # [START video_label_tutorial_construct_request]
        video_client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.enums.Feature.LABEL_DETECTION]
    
        #with io.open(path,'rb') as file:
        input_content = path.read()
    
        operation = video_client.annotate_video(
            input_content=input_content, features=features)
        #operation = video_client.annotate_video(path, features=features)
        # [END video_label_tutorial_construct_request]
        print('\nProcessing video for label annotations:')
    
        #[START video_label_tutorial_check_operation]
        result = operation.result(timeout=30)
        print('\nFinished processing.')
        # [END video_label_tutorial_check_operation]
        # [START video_label_tutorial_parse_response]
        segment_labels = result.annotation_results[0].segment_label_annotations
        for i, segment_label in enumerate(segment_labels):
            print('Video label description: {}'.format(
                segment_label.entity.description))
            labels.append(segment_label.entity.description) 
            for category_entity in segment_label.category_entities:
                print('\tLabel category description: {}'.format(
                    category_entity.description))
            
            for i, segment in enumerate(segment_label.segments):
                confidence = segment.confidence         
                print('\tConfidence: {}'.format(confidence))
            print('\n')         
        # [END video_label_tutorial_parse_response]
        #--------------------------end of lable_analyze()---=--------------          
        if labels:
        #def Vcust_search(itext):#fun for custom serach  
             s_result = []
             print(labels)
             result = resource.list(q=labels, cx='017795299087749107028:onvo85h2owu',searchType='image').execute()
             print(len(result['items']))
             for item in result['items']:
                 for i in range(len(result['items'])):
                     res = dict((k, item[k]) for k in ['title','link','image'] if k in item) 
                 s_result.append(res)
                 
             return jsonify(s_result)
