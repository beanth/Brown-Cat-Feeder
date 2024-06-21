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
		height = image.shape[0]
		width = image.shape[1]
		########################
		######### TODO ######### MAKE MASK SIZE AND POSITION CUSTOMIZABLE
		########################
		for y in range(90): # cut off some of the noise
			for x in range(width):
				mask[y][x] = 0
			if y > 100:
				break
		num_food = numpy.sum(mask)
		result = cv2.bitwise_and(image, image, mask=mask)
		result = cv2.putText(result, str(num_food), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA, False)
		_, image_encoded = cv2.imencode('.jpg', result)
		data[0] = image_encoded
		data[1].append([datetime.now(), int(num_food)])
	
	cam.stop()
