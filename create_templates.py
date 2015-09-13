# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 21:01:44 2015

@author: croeer

Split all_pieces2 into single 134x134 fields

"""

import cv2
import numpy as np
from functions import *

img_rgb = cv2.imread('samples/all_pieces2.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

_,b = getBoard(img_gray)
img_board = img_rgb[ b[1]:b[1]+b[3] , b[0]:b[0]+b[2] ]

w,h = (134,134)
i=0
for x in range(1,9):
    for y in range(1,9):
        i+=1
        p = ((x-1)*134, (y-1)*134)

        cropped = img_board[ p[0]:p[0]+w, p[1]:p[1]+h ]
        cv2.imwrite('fields/crop' + str(i) + '.png', cropped)