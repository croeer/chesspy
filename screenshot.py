import pyscreenshot as ImageGrab
from detect import *

if __name__ == '__main__':
	ImageGrab.grab_to_file('screenshot.png')
	parsePngFile('screenshot.png', 'w')
	parsePngFile('screenshot.png', 'b')

