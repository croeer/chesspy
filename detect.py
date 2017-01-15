# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 18:50:46 2015

@author: croeer
"""
import argparse
from functions import *
from color import *
import packages.tools as tools
import imutils

def parsePngFile(file, color):
	print "Parsing file", file, color
	img_rgb = cv2.imread(file)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

	img_masked,b = getBoard(img_gray)
	img_board = img_gray[ b[1]:b[1]+b[3] , b[0]:b[0]+b[2] ]
	img_board_color = img_rgb[ b[1]:b[1]+b[3] , b[0]:b[0]+b[2] ]
	_, f = detectTargetField( img_board_color )
	#print "board, field", b, f
	img_field_color = img_board_color[ f[1]:f[1]+f[3] , f[0]:f[0]+f[2] ]
	#cv2.imwrite('outboard.png', img_board_color)
	#cv2.imwrite('outfield.png', img_field_color)

	fen, boardArr = setupBoard(b, img_board)
	print "FEN", fen
	rochade = '-' # 'KQkq'

	if color is None:
		# Try to detect color of last move. f contains the target field of enemys last move
		center = (f[0]+f[2]/2, f[1]+f[3]/2)
		#print center
		lastMove = transformCoordinatesToField(b, 1.0, [center])[0]
		#print "last move", lastMove
		pos = tools.parseFEN(fen + ' w ' + rochade + ' - 0 1')
		index = (8-lastMove[1])*8+lastMove[0]-1
		#print "index", index
		target = boardArr[index]
		#print "target", target
		if target.isupper():
			color = 'b'
		else:
			color = 'w'
		#print "color", color

	pos = tools.parseFEN(fen + ' ' + color + ' ' + rochade + ' - 0 1')
	print "Detected board: (" + color + ')'
	print(' '.join(pos.board))

	searcher = sunfish.Searcher()
	move, score = searcher.search(pos, secs=5)
	move = move if color == 'w' else (119-move[0], 119-move[1])
	print "Suggested move (score):", sunfish.render(move[0]) + sunfish.render(move[1]), score

	# draw arrow for suggested move
	cv2.arrowedLine(img_rgb,pointInGlobalCoordinates(b,move[0]),pointInGlobalCoordinates(b,move[1]),(0,0,255),5)
	cv2.imwrite('output.png', img_rgb)
	
	cv2.arrowedLine(img_board_color,pointInGlobalCoordinates(b,move[0]),pointInGlobalCoordinates(b,move[1]),(0,0,255),5)
	img_board_color_scaled = imutils.resize(img_board_color, width = 200)
	cv2.imwrite('outputboard.png', img_board_color_scaled)
	cv2.imshow("Suggested move", img_board_color_scaled)
	cv2.waitKey(0)
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('file', help='png image filename to parse')
	parser.add_argument('-color', help='color to move, "w" or "b"', required=False, choices=['w','b'])

	args = parser.parse_args()
	parsePngFile(args.file, args.color)
