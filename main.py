import cv2
import numpy
import threading
from flask import Flask, jsonify, request, Response
from capture import capture_loop
from datetime import datetime
  
# creating a Flask app 
app = Flask(__name__)

samples = [cv2.imencode('.jpg', cv2.imread('images/no-sample.jpg')), []]

@app.route('/', methods = ['GET'])
def main():
	if (request.method == 'GET'):
		data = samples[0].tobytes()
		res = Response(data)
		res.headers["Content-Type"] = "image/jpeg"
		return res

# A simple function to calculate the square of a number 
# the number to be squared is sent in the URL when we use GET 
# on the terminal type: curl http://127.0.0.1:5000 / home / 10 
# this returns 100 (square of 10) 
@app.route('/data', methods = ['GET'])
def fetch_data():
	ret = jsonify(samples[1])
	samples[1] = []
	return ret

# driver function 
if __name__ == '__main__': 
	thread = threading.Thread(target=capture_loop, args=(samples,))
	thread.start()

	app.run(debug=True, host="0.0.0.0", port=5010)

	thread.join()