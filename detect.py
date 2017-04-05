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
import config

def parsePngFile(file, color):
	print "Parsing file", file, color
	img_rgb = cv2.imread(file)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

	img_masked,b = getBoard(img_gray)
	img_board = img_gray[ b[1]:b[1]+b[3] , b[0]:b[0]+b[2] ]
	img_board_color = img_rgb[ b[1]:b[1]+b[3] , b[0]:b[0]+b[2] ]

	if (config.verbosity):	
		cv2.imwrite('outboard.png', img_board_color)

	fen, boardArr = setupBoard(b, img_board)
	castle = config.castle

	if color is None:
		# Try to detect color of last move. f contains the target field of enemys last move
		_, f = detectTargetField( img_board_color )
		img_field_color = img_board_color[ f[1]:f[1]+f[3] , f[0]:f[0]+f[2] ]
		if (config.verbosity):	
			cv2.imwrite('outfield.png', img_field_color)

		center = (f[0]+f[2]/2, f[1]+f[3]/2)
		#print center
		lastMove = transformCoordinatesToField(b, 1.0, [center])[0]
		#print "last move", lastMove
		index = (8-lastMove[1])*8+lastMove[0]-1
		#print "index", index
		target = boardArr[index]
		#print "target", target
		if target.isupper():
			color = 'b'
		else:
			color = 'w'
		#print "color", color
	
	fen = fen + ' ' + color + ' ' + castle + ' - 0 1'
	print "FEN", fen
	pos = tools.parseFEN(fen)
	print "Detected board: (" + color + ')'
	print(' '.join(pos.board))

	searcher = sunfish.Searcher()
	move, score = searcher.search(pos, secs=config.time)
	move = move if color == 'w' else (119-move[0], 119-move[1])
	print "Suggested move (score):", sunfish.render(move[0]) + sunfish.render(move[1]), score

	# draw arrow for suggested move
	cv2.arrowedLine(img_rgb,pointInGlobalCoordinates(b,move[0]),pointInGlobalCoordinates(b,move[1]),(0,0,255),5)
	cv2.imwrite('output.png', img_rgb)
	
	cv2.arrowedLine(img_board_color,pointInGlobalCoordinates(b,move[0]),pointInGlobalCoordinates(b,move[1]),(0,0,255),5)
	img_board_color_scaled = imutils.resize(img_board_color, width = 200)
	
	if (config.verbosity):	
		cv2.imwrite('outputboard.png', img_board_color_scaled)

	if (config.show_move):
		cv2.imshow("Suggested move", img_board_color_scaled)
		cv2.waitKey(0)
	
	for i in range(config.additional_moves):
		pos = pos.move(move)
		move, score = searcher.search(pos, secs=config.time)
		if (color == 'b'):
			color = 'w'
		else:
			color = 'b'
		move = move if color == 'w' else (119-move[0], 119-move[1])
		print "Suggested move (score):", sunfish.render(move[0]) + sunfish.render(move[1]), score
	
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('file', help='png image filename to parse')
	parser.add_argument('-color', help='color to move, "w" or "b" (color is autodetected if omitted)', required=False, choices=['w','b'])
	parser.add_argument('-t', '--time', help='sunfish thinking time, default=5', required=False, type=int, default=5)
	parser.add_argument('-v','--verbose', help='increase output verbosity and saving of status images', action='store_true')
	parser.add_argument('--show_move', dest='show_move', help='show best move window (default)', action='store_true')
	parser.add_argument('--hide_move', dest='show_move', help='hide best move window', action='store_false')
	parser.add_argument('--castle', help='castling possibilities (default: -)', required=False, choices=['KQkq','Kkq','Qkq','kq','KQk','Kk','Qk','k','KQq','Kq','Qq','q','K','Q','KQ','-'], default='-')
	parser.add_argument('-a','--additional_moves', help='number of additional moves to calculate', type=int, default=0)
	parser.set_defaults(show_move=True)	
	
	args = parser.parse_args()
	config.verbosity = args.verbose
	config.show_move = args.show_move
	config.time = args.time
	config.castle = args.castle
	config.additional_moves = args.additional_moves
	parsePngFile(args.file, args.color)
