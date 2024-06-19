import cv2
import time
import numpy
from picamera2 import Picamera2, Preview
from datetime import datetime

_, image_encoded = cv2.imencode('.jpg', cv2.imread('images/no-sample.jpg'))

def capture_loop(data):
	cam = Picamera2()
	cam_config = cam.create_preview_configuration()
	cam.configure(cam_config)
	cam.start_preview(Preview.NULL)
	cam.start()
	while data[2]:
		time.sleep(1)
		_, image_encoded = cv2.imencode('.jpg', cam.capture_array())
		data[0] = image_encoded
		data[1].append([datetime.now(), 30])
	
	cam.stop()
