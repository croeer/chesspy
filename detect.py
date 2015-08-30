# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 18:50:46 2015

@author: croeer
"""

import cv2
import numpy as np
import packages.sunfish as sunfish
import packages.xboard
#from matplotlib import pyplot as plt

#pos = packages.xboard.parseFEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

#move, score = sunfish.search(pos)

#print move
#print score

img_rgb = cv2.imread('samples/all_pieces.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

def getPositionsByTemplateMatching( filename, img ):
    ret=[]
    template = cv2.imread(filename,0)
    w, h = template.shape[::-1]
    
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]): 
        addPt = True
        # check for similar points in close range
        aktPt = (pt[0] + w/2, pt[1] + h/2)
        
        for chkPt in ret:
            #print 'Checking point ' , aktPt[0], aktPt[1], ' against ', chkPt[0], chkPt[1], ': ', (chkPt[0]-aktPt[0])**2+(chkPt[1]-aktPt[1])**2
            if (chkPt[0]-aktPt[0])**2+(chkPt[1]-aktPt[1])**2 < 25:
                addPt = False
                break
        if addPt:
            ret.append( aktPt )
        #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    return ret

def getBoard( img ):
    ret,thresh = cv2.threshold(img,127,255,0)
    contours, _ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #print 'Found %d contours' % (len(contours))
    # find board
    max_area = 0
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = cnt
    
    return cv2.boundingRect(best_cnt)

def transformCoordinatesToField( board, point ):
    return

print getPositionsByTemplateMatching('templates/black_pawn.png', img_gray)    

img_rgb2=img_rgb.copy()
x,y,w,h = getBoard(img_gray)
cv2.rectangle(img_rgb2,(x,y),(x+w,y+h),(0,255,0),2)
cv2.imwrite('bb.png',img_rgb2)

img_cont=img_rgb.copy()
cv2.drawContours(img_cont, [best_cnt], 0, (0,255,0), 3)

#img = cv2.drawContours(img_gray, contours, -1, (0,255,0), 3)
cv2.imwrite('cont.png',img_cont)
#cv2.imshow('Image', img_rgb)
#cv2.waitKey(0)

