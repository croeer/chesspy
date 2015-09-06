# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 21:00:17 2015

@author: croeer
"""


import cv2
import numpy as np
import packages.sunfish as sunfish
import packages.xboard as xboard

def getPositionsByTemplateMatching( filename, img ):
    ret=[]
    template = cv2.imread(filename,0)
    w, h = template.shape[::-1]
    
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]): 
        addPt = True
        # check for similar points in close range
        aktPt = (pt[0] + w/2, pt[1] + h/2)
        
        for chkPt in ret:
            #print 'Checking point ' , aktPt[0], aktPt[1], ' against ', chkPt[0], chkPt[1], ': ', (chkPt[0]-aktPt[0])**2+(chkPt[1]-aktPt[1])**2
            if (chkPt[0]-aktPt[0])**2+(chkPt[1]-aktPt[1])**2 < 100:
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
    
    mask = np.zeros((img.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)
    res = cv2.bitwise_and(img,mask)
    #cv2.imwrite('detected.png',res)

    return res, cv2.boundingRect(best_cnt)

def transformCoordinatesToField( board, points ):
    binSizeX = board[2]//8
    binSizeY = board[3]//8

    ret = []
    
    for point in points:
        pointInBoardCoordinates = (point[0]-board[0],point[1]-board[1])
        
        binX = -(-pointInBoardCoordinates[0]//binSizeX)
        binY = -(-pointInBoardCoordinates[1]//binSizeY)
     
        ret.append((binX,9-binY))
        #return (chr(ord('a')+(binX-1)),chr(ord('1')+(9-binY-1)))
        #return chr(ord('a')+(binX-1)) + chr(ord('1')+(9-binY-1)) # human readable
    return ret

def pointInGlobalCoordinates( board, field ):
    p0,p1 = (board[0],board[1])
    rank, fil = divmod(field - sunfish.A1, 10)
    binSizeX = board[2]//8
    binSizeY = board[3]//8
    p0 = p0 + binSizeX*fil + binSizeX/2
    p1 = p1 + binSizeY*(8+rank-1) + binSizeY/2
    return (p0,p1) 

def replaceFig( key, pieces, boardL ):
    for p in pieces:
        pos = 63+p[0]-8*p[1]
        #print key, p, pos
        boardL[pos]=key
    return
    
def setupBoard( board, img ):
    whitePawns = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/white_pawn.png', img))
    whiteRooks = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/white_rook.png', img))
    whiteKnights = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/white_knight.png', img))
    whiteBishops = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/white_bishop.png', img))
    whiteKing = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/white_king.png', img))
    whiteQueens = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/white_queen.png', img))
    blackPawns = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/black_pawn.png', img))
    blackRooks = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/black_rook.png', img))
    blackKnights = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/black_knight.png', img))
    blackBishops = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/black_bishop.png', img))
    blackKing = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/black_king.png', img))
    blackQueens = transformCoordinatesToField(board, getPositionsByTemplateMatching('templates/black_queen.png', img))
    
    boardL = ['o']*64
    for k,v in {'P':whitePawns,'R':whiteRooks,'N':whiteKnights,'B':whiteBishops,'K':whiteKing,'Q':whiteQueens}.iteritems():
        replaceFig(k,v,boardL)
    
    for k,v in {'p':blackPawns,'r':blackRooks,'n':blackKnights,'b':blackBishops,'k':blackKing,'q':blackQueens}.iteritems():
        replaceFig(k,v,boardL)
    
    stri = ''
    for k in range(64):
        stri = stri + boardL[k]
        if (k+1) % 8 == 0 and k < 63:
            stri = stri + '/'
    for k in range(8,0,-1):
        stri = stri.replace('o'*k, str(k))
    return stri
