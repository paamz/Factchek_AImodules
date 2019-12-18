# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:05:17 2019

@author: IT2
"""
from flask_restful import Resource
from flask import request,jsonify
import cv2,os,io,glob
import numpy as np
from google.cloud import vision
from google.protobuf.json_format import MessageToDict
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'D:\G_Apis\VisionApis\appPY\**********.json' 

class db_ImageFC(Resource):
    def post(self): 
        original = request.files['img']
        #path = request.files['img']
        #cur = mysql.connection.cursor()
        try:
           #_original = request.files['img']
           in_memory_file = io.BytesIO()
           original.save(in_memory_file)
           # convert string of image data to uint8
           nparr = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
           color_image_flag = 1
           original = cv2.imdecode(nparr, color_image_flag)#decode image
           original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
           #original = cv2.imread("D:\detect_how_similar_images_are\images\images.png")
           mypath="D:/G_Apis/ImgCheck/factCres"
           data_path = os.path.join(mypath,'*g')
           files = glob.glob(data_path)
           print(type(files))
           m_result = {}
           result = []
           data= []
           for f1 in files:
               print(f1) 
               image_to_compare = cv2.imread(f1)
               image_to_compare = image_to_compare.astype('uint8')
               image_to_compare = cv2.cvtColor(image_to_compare, cv2.COLOR_BGR2GRAY)
               #Check for similarities between the 2 images
               sift = cv2.xfeatures2d.SIFT_create()
               kp_1, desc_1 = sift.detectAndCompute(original, None)
               kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)
               
               index_params = dict(algorithm=0, trees=5)
               search_params = dict()
               flann = cv2.FlannBasedMatcher(index_params, search_params)
               
               matches = flann.knnMatch(desc_1, desc_2, k=2)
               
               good_points = []
               for m, n in matches:
                   if m.distance < 0.6*n.distance:             
                       good_points.append(m)           
               #Define how similar they are
               number_keypoints = 0
               if len(kp_1) <= len(kp_2):
                   number_keypoints = len(kp_1)
               else:
                   number_keypoints = len(kp_2)
               
               #print("Keypoints 1ST Image: " + str(len(kp_1)))
               #print("Keypoints 2ND Image: " + str(len(kp_2)))
               print("GOOD Matches:", len(good_points))
               #res = dict(f1,len(good_points))
               for l in range(len(f1)):
                   m_result = dict((k,len(good_points)) for k in ['ImageLink','MatchedScore'])
                   m_result['ImageLink'] = f1
                   m_result['MatchedScore'] = len(good_points) / number_keypoints * 100
               data.append(m_result['MatchedScore'])    
               result.append(m_result)
              #m_result.update(res)
               print("How good it's the match: ", len(good_points) / number_keypoints * 100)        
#                           result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)
#                          
#                          cv2.imshow("result", cv2.resize(result, None, fx=0.4, fy=0.4))
#                          cv2.imwrite("feature_matching.jpg", result)            
               cv2.imshow("Original", cv2.resize(original, None, fx=0.4, fy=0.4))
               cv2.imshow("Duplicate", cv2.resize(image_to_compare, None, fx=0.4, fy=0.4))
           #m_result.sort(reverse = True)
           #cv2.destroyAllWindows()
           s_result = sorted(result, key = lambda i: i['MatchedScore'],reverse=True)
           data.sort(reverse=True)
           #print(statistics.mean(data[:5]))
           print('$$$$$$$$$original here.........',original)
           for i in data:
              if i > 89:
                   return jsonify(s_result)
# =============================================================================
#               else:
#                   ImgDetect_web()
# =============================================================================
# =============================================================================
#                    # try:
#                        original = request.files['img']
#                        print('in side vison original here.........',original)
#                        client = vision.ImageAnnotatorClient()
#                        #[START vision_python_migration_web_detection]
#                        #with io.open(path, 'rb') as image_file:
#                        #content = path.tobytes()
#                        imageData = io.BytesIO(request.get_data())
#                        content  = imageData.read()
#                        print('content............',content)
#                        
#                        image = vision.types.Image(content=content)
#                        print('imageeeeeeeeeee',image)
#                                    
#                        response = client.web_detection(image=image)
#                        print('response^^^^^^^^^^^^^^^^^^^^^',response)
#                        annotations = response.web_detection
#                        _annotations = MessageToDict(annotations)#conversion of RepeatedCompositeCo object
#                        res_annotations = _annotations['pagesWithMatchingImages']
#                        if res_annotations:
#                             return jsonify(res_annotations)
# =============================================================================
                    #except:
                         #return jsonify({"Result":"Doesn't match anywhwere..!"})

        except Exception as e:
            return e
