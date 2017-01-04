# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 18:50:46 2015

@author: croeer
"""
import argparse
from functions import *
import packages.xboard as xboard

parser = argparse.ArgumentParser()
parser.add_argument('file', help='png image filename to parse')
parser.add_argument('color', help='color to move, "w" or "b"', choices=['w','b'])

args = parser.parse_args()

print "Parsing file " + args.file
#img_rgb = cv2.imread('samples/all_pieces.png')
img_rgb = cv2.imread(args.file)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

img_masked,b = getBoard(img_gray)
img_board = img_gray[ b[1]:b[1]+b[3] , b[0]:b[0]+b[2] ]
#cv2.imwrite('outboard.png', img_board)

fen = setupBoard(b, img_board)

color = args.color
rochade = '-' # 'KQkq'
pos = xboard.parseFEN(fen + ' ' + color + ' ' + rochade + ' - 0 1')
print "Detected board: (" + color + ')'
print(' '.join(pos.board))

move, score = sunfish.search(pos)
move = move if color == 'w' else (119-move[0], 119-move[1])
print "Suggested move:", sunfish.render(move[0]) + sunfish.render(move[1])

# draw arrow for suggested move
cv2.arrowedLine(img_rgb,pointInGlobalCoordinates(b,move[0]),pointInGlobalCoordinates(b,move[1]),(0,0,255),5)
cv2.imwrite('output.png', img_rgb)
