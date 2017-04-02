# chesspy
Detect chess pieces on chesstempo boards using opencv in python.

## Usage
todo

## Example
Take the screenshot ![Example screenshot](/samples/stellung3.png?raw=true "Example Screenshot")

After template matching the detected board is passed to sunfish, which calculates the optimal move and prints it in the original picture:
![Example screenshot](/screenshots/image.png?raw=true "Example Screenshot")
![Example screenshot](/screenshots/output.png?raw=true "Example Screenshot")

## Dependencies

Using http://opencv.org/ to detect the pieces and [Sunfish](https://github.com/thomasahle/sunfish) python chess engine to analyse the board and predict the next move.
