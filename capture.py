import cv2
import time
import numpy
from picamera2 import Picamera2, Preview
from datetime import datetime

def capture_loop(data):
	cam = Picamera2()
	cam_config = cam.create_preview_configuration()
	cam.configure(cam_config)
	cam.start_preview(Preview.NULL)
	cam.start()
	
	while data[2]:
		time.sleep(1)
		image = cam.capture_array()
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		_, image_encoded = cv2.imencode('.jpg', image)
		data[0] = image_encoded
		data[1].append([datetime.now(), 30])
	
	cam.stop()
