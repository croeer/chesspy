# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 21:00:17 2015

@author: croeer
"""
import cv2
import numpy as np
import packages.sunfish as sunfish
import packages.xboard as xboard
import imutils

def getPositionsByTemplateMatching( filename, img, threshold ):
    #print "matching", filename
    ret=[]
    template = cv2.imread(filename,0)
    w, h = template.shape[::-1]

    # templates are taken for 134x134 field size so image must be scaled accordingly
    img_scaled = imutils.resize(img, width = 8*134)
    #cv2.imwrite(filename + 'scaled.png', img_scaled)
    scalefactor = img.shape[1] / float(img_scaled.shape[1])

    boximg = np.copy(img_scaled)
    res = cv2.matchTemplate(img_scaled,template,cv2.TM_CCOEFF_NORMED)
    #threshold = 0.4
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

        cv2.rectangle(boximg, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    
    cv2.imwrite(filename + '.png', boximg)

    return scalefactor, ret

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

def transformCoordinatesToField( board, scalefactor, points ):
    #print "transforming", points
    binSizeX = board[2]//8
    binSizeY = board[3]//8
    #print binSizeX, binSizeY

    ret = []
    
    for point in points:
        #print "point", point
        pointInBoardCoordinates = [(int)(x*scalefactor) for x in point] #(point[0]-board[0],point[1]-board[1])
        #print "maps to", pointInBoardCoordinates

        binX = -(-pointInBoardCoordinates[0]//binSizeX)
        binY = -(-pointInBoardCoordinates[1]//binSizeY)
        #print binX, binY
        ret.append((binX,9-binY))
        #return (chr(ord('a')+(binX-1)),chr(ord('1')+(9-binY-1)))
        #print chr(ord('a')+(binX-1)) + chr(ord('1')+(9-binY-1)) # human readable
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

    f, wp = getPositionsByTemplateMatching('templates/white_pawn.png', img, 0.4)
    whitePawns = transformCoordinatesToField(board, f, wp)
    f, wr = getPositionsByTemplateMatching('templates/white_rook.png', img, 0.5)
    whiteRooks = transformCoordinatesToField(board, f, wr)
    f, wk = getPositionsByTemplateMatching('templates/white_knight.png', img, 0.6)
    whiteKnights = transformCoordinatesToField(board, f, wk)
    f, wb = getPositionsByTemplateMatching('templates/white_bishop.png', img, 0.5)
    whiteBishops = transformCoordinatesToField(board, f, wb)
    f, wkg = getPositionsByTemplateMatching('templates/white_king.png', img, 0.6)
    whiteKing = transformCoordinatesToField(board, f, wkg)
    f, wq = getPositionsByTemplateMatching('templates/white_queen.png', img, 0.6)
    whiteQueens = transformCoordinatesToField(board, f, wq)

    f, bp = getPositionsByTemplateMatching('templates/black_pawn.png', img, 0.8)
    blackPawns = transformCoordinatesToField(board, f, bp)
    f, br = getPositionsByTemplateMatching('templates/black_rook.png', img, 0.6)
    blackRooks = transformCoordinatesToField(board, f, br)
    f, bk = getPositionsByTemplateMatching('templates/black_knight.png', img, 0.6)
    blackKnights = transformCoordinatesToField(board, f, bk)
    f, bb = getPositionsByTemplateMatching('templates/black_bishop.png', img, 0.6)
    blackBishops = transformCoordinatesToField(board, f, bb)
    f, bkg = getPositionsByTemplateMatching('templates/black_king.png', img, 0.6)
    blackKing = transformCoordinatesToField(board, f, bkg)
    f, bq = getPositionsByTemplateMatching('templates/black_queen.png', img, 0.6)
    blackQueens = transformCoordinatesToField(board, f, bq)

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
