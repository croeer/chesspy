import pyscreenshot as ImageGrab
from detect import *

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
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

	ImageGrab.grab_to_file('screenshot.png')
	parsePngFile('screenshot.png', args.color)

