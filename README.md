# chesspy
Detect chess pieces on chesstempo boards using opencv in python.

## Usage
```
usage: detect.py [-h] [-color {w,b}] [-t TIME] file

positional arguments:
  file                  png image filename to parse

optional arguments:
  -h, --help            show this help message and exit
  -color {w,b}          color to move, "w" or "b"
  -t TIME, --time TIME  sunfish thinking time, default=5
```

Or use the provided `screenshot.py` script to grab a screenshot and immediately start analyzing it:
```
python screenshot.py
```

## Example
Take the screenshot ![Example screenshot](/samples/stellung3.png?raw=true "Example Screenshot")

After template matching the detected board is passed to sunfish, which calculates the optimal move and prints it in the original picture:
```
c:\dev\chesspy>python detect.py samples\stellung3.png
Parsing file samples\stellung3.png None
FEN 1rb1nrk1/2q2p1p/p1p3p1/2QNP3/P7/6P1/1PP2P1P/3RR1K1
Detected board: (b)



 . k . r r . . .
 p . p . . p p .
 . p . . . . . .
 . . . . . . . p
 . . . p n q . .
 . P . . . P . P
 P . P . . Q . .
 . K R N . B R .


Suggested move (score): c6d5 1181

c:\dev\chesspy>
```
![Example screenshot](/screenshots/output.png?raw=true "Example Screenshot")

## Dependencies

Using http://opencv.org/ to detect the pieces and [Sunfish](https://github.com/thomasahle/sunfish) python chess engine to analyse the board and predict the next move.
