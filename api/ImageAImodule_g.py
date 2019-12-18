# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 12:03:07 2019

@author: IT2
"""
from flask_restful import Resource
from flask import request,jsonify
import cv2,os
import numpy as np
from google.cloud import vision
from google.protobuf.json_format import MessageToDict
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'#########.json' 

class g_ImageFC(Resource):
    def post(self): 
        try:
            """Detects web annotations given an image."""
            path = request.files['img']
            client = vision.ImageAnnotatorClient()
            #[START vision_python_migration_web_detection]
            #with io.open(path, 'rb') as image_file:
            print(path)
            content = path.read()
            print('content............',content)
            image = vision.types.Image(content=content)
            print('imgaeeeeeeeeeeeeeee',image)
        
            response = client.web_detection(image=image)
            annotations = response.web_detection
            _annotations = MessageToDict(annotations)#conversion of RepeatedCompositeCo object
            res_annotations = _annotations['pagesWithMatchingImages']
        
            return jsonify(res_annotations)
        
        except Exception as e:
            return e
