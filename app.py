        # -*- coding: utf-8 -*-
"""Created on Thu Dec 12 15:02:1 2019

@author: IT2
"""
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    from api import *
    app.run(host="0.0.0.0",port=8080) 