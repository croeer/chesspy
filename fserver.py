from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from detect import *

# Initialize the Flask application
app = Flask(__name__)

# curl -F "file=@samples/stellung6-1.png" localhost:5000/api/test

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    print(request.headers)
    #data = request.files['file']
    #img = cv2.imread(data)
    #read image file string data
    filestr = request.files['file'].read()
    #convert string data to numpy array
    npimg = np.fromstring(filestr, np.uint8)
    # convert numpy array to image
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cv2.imwrite("uploaded.png", img)
    fen,move = parseImg(img, None)

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0]),
    'fen': fen,
    'move': move}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
