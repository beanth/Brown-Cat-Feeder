import cv2
import numpy
import threading
import signal
import logging
import sys
from flask import Flask, jsonify, request, Response
from capture import capture_loop
from datetime import datetime
  
app = Flask(__name__)
app.logger.setLevel(logging.ERROR)
log = logging.getLogger('werkzeug')
log.disabled = True

samples = [cv2.imencode('.jpg', cv2.imread('images/no-sample.jpg'))[1], [], True]

def gen_frame():
	oldFrame = 0
	while True:
		frame = samples[0].tobytes()
		if (frame != oldFrame):
			oldFrame = frame
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
		else:
			yield (b'')

@app.route('/', methods = ['GET'])
def main():
	if (request.method == 'GET'):
		#data = samples[0].tobytes()
		res = Response(gen_frame(),
			mimetype='multipart/x-mixed-replace; boundary=frame')
		#res.headers["Content-Type"] = "image/jpeg"
		res.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
		res.headers["Pragma"] = "no-cache"
		res.headers["Expires"] = "0"
		res.cache_control.max_age = 0
		return res

@app.route('/data', methods = ['GET'])
def fetch_data():
	ret = jsonify(samples[1])
	samples[1] = []
	return ret
	
	
# clean up thread if Flask is killed
def signal_handler(sig, frame):
    samples[2] = False
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# driver function 
if __name__ == '__main__': 
	thread = threading.Thread(target=capture_loop, args=(samples,))
	thread.start()

	app.run(debug=False, host="0.0.0.0", port=5010, threaded=True)

	thread.join()
