import cv2
import time
import numpy
from picamera2 import Picamera2, Preview
from datetime import datetime

lower_color_bound = (0, 45, 83)
upper_color_bound = (30, 187, 255)

def capture_loop(data):
	cam = Picamera2()
	cam_config = cam.create_preview_configuration()
	cam.configure(cam_config)
	cam.start_preview(Preview.NULL)
	cam.start()
	
	while data[2]:
		time.sleep(1)
		image = cam.capture_array()
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower_color_bound, upper_color_bound)
		result = cv2.bitwise_and(image, image, mask=mask)
		_, image_encoded = cv2.imencode('.jpg', result)
		data[0] = image_encoded
		data[1].append([datetime.now(), 30])
	
	cam.stop()
