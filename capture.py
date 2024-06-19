import cv2
import time
import numpy
from datetime import datetime

_, image_encoded = cv2.imencode('.jpg', cv2.imread('images/no-sample.jpg'))

def capture_loop(data):
	# camera capture logic
	# with PiCamera() as cam:
	#data[1].append([datetime.now(), 13])
	while True:
		time.sleep(1)
		if not obj[0]:
			_, image_encoded = cv2.imencode('.jpg', cv2.imread('images/no-sample.jpg'))
			data[0] = image_encoded