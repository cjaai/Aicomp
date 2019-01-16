#####################
#Convert json format to yolo faomart
# 2018/12/12 by Tony
#####################

import string
import sys
import json
import numpy as np
import cv2
import os
import subprocess
import shutil
import glob
import pandas as pd
import csv
import image
from collections import namedtuple
from itertools import product
from math import acos, sin, cos, radians
from numpy import*
from statistics import mean, median,variance,stdev

# The folder of output Json file
jsonPath = "./json/"

pair=[['0','Car'],['1','Bus'],['2','Truck'],['3','Svehicle'],['4','Pedestrian'],['5','Motorbike'],['6','Bicycle'],['7','Train'],['8','Signal'],['9','Signs']]

def jsonToCsv():
    mycolumns = ['categoryNo','x1','y1','x2','y2']
    

    files = [f for f in os.listdir(jsonPath) if f.endswith('.json')]
    for k, file in enumerate(files):

        df = pd.DataFrame(columns=mycolumns)

        fullFileName = os.path.join(jsonPath, file)
        with open(fullFileName, 'r') as f:
            data = json.load(f)
    
        for i, d in enumerate(data['labels']):
            category = d['category']
            print(category)

            for p in pair:
                if (p[1] == category):
                    categoryNo = p[0]
                    break

            print(categoryNo)

            xy = d['box2d']
            print(xy['x1'])
            print(xy['y1'])
            print(xy['x2'])
            print(xy['x2'])

            centerX = (xy['x1'] + (xy['x2'] - xy['x1']) / 2) / 1936
            centerY = (xy['y1'] + (xy['y2'] - xy['y1']) / 2) / 1216

            width = (xy['x2'] - xy['x1']) / 1936
            height = (xy['y2'] - xy['y1']) / 1216

            #df.loc[len(df)] = [categoryNo,d['category'],xy['x1'],xy['y1'],xy['x2'],xy['x2']]
            df.loc[len(df)] = [categoryNo,centerX,centerY,width,height]
              
        filename, file_extension = os.path.splitext(file)    
        df.to_csv(filename + '.txt', index=False,header=None, sep=' ')
    
jsonToCsv()      
