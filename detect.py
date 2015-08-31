# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 18:50:46 2015

@author: croeer
"""

import cv2
import numpy as np
import packages.sunfish as sunfish
import packages.xboard as xboard
#from matplotlib import pyplot as plt

#pos = xboard.parseFEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

#move, score = sunfish.search(pos)

#print move, score
#print("My move:", sunfish.render(move[0]) + sunfish.render(move[1]))
#pos = pos.move(move)
#print(' '.join(pos.board))


img_rgb = cv2.imread('samples/all_pieces.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

def getPositionsByTemplateMatching( filename, img ):
    ret=[]
    template = cv2.imread(filename,0)
    w, h = template.shape[::-1]
    
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8   
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
    
    return cv2.boundingRect(best_cnt)

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

def replaceFig( key, pieces, boardL ):
    for p in pieces:
        pos = 63+p[0]-8*p[1] #8*(p[1]-1)+p[0]-1
        print key, p, pos
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
    
    boardL = [' ']*64
    for k,v in {'P':whitePawns,'R':whiteRooks,'N':whiteKnights,'B':whiteBishops,'K':whiteKing,'Q':whiteQueens}.iteritems():
        replaceFig(k,v,boardL)
    
    for k,v in {'p':blackPawns,'r':blackRooks,'n':blackKnights,'b':blackBishops,'k':blackKing,'q':blackQueens}.iteritems():
        replaceFig(k,v,boardL)
    
    return "".join(boardL)



img_rgb2=img_rgb.copy()
b = getBoard(img_gray)
print setupBoard(b, img_gray)

#print transformCoordinatesToField(board, foundPieces)

#cv2.rectangle(img_rgb2,(x,y),(x+w,y+h),(0,255,0),2)
#cv2.imwrite('bb.png',img_rgb2)

#img_cont=img_rgb.copy()
#cv2.drawContours(img_cont, [best_cnt], 0, (0,255,0), 3)

#img = cv2.drawContours(img_gray, contours, -1, (0,255,0), 3)
#cv2.imwrite('cont.png',img_cont)
#cv2.imshow('Image', img_rgb)
#cv2.waitKey(0)

