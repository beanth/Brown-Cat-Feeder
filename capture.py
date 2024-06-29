import cv2
import time
import numpy
from picamera2 import Picamera2, Preview

lower_color_bound = (0, 15, 71)
upper_color_bound = (36, 220, 235)

def capture_loop(data):
	cam = Picamera2()
	cam_config = cam.create_preview_configuration()
	cam.configure(cam_config)
	#{'AeExposureMode': (0, 3, 0), 'AeMeteringMode': (0, 3, 0), 'AwbMode': (0, 7, 0), 'AeFlickerMode': (0, 1, 0), 'AnalogueGain': (1.0, 63.9375, None), 'FrameDurationLimits': (16971, 1103354, None), 'AeConstraintMode': (0, 3, 0), 'NoiseReductionMode': (0, 4, 0), 'Sharpness': (0.0, 16.0, 1.0), 'AwbEnable': (False, True, None), 'StatsOutputEnable': (False, True, None), 'Contrast': (0.0, 32.0, 1.0), 'Saturation': (0.0, 32.0, 1.0), 'Brightness': (-1.0, 1.0, 0.0), 'ColourGains': (0.0, 32.0, None), 'AeFlickerPeriod': (100, 1000000, None), 'HdrMode': (0, 4, 0), 'ExposureValue': (-8.0, 8.0, 0.0), 'ScalerCrop': ((16, 0, 256, 256), (16, 0, 2560, 1920), (16, 0, 2560, 1920)), 'ExposureTime': (134, 0, None), 'AeEnable': (False, True, None)}
	#cam.set_controls({"AwbEnable": True, 'AwbMode': 3, 'AeExposureMode': 3})
	cam.start_preview(Preview.NULL)
	cam.start()
	
	with cam.controls as ctrl:
		ctrl.AwbEnable = True
		ctrl.AwbMode = 4
		ctrl.AnalogueGain = 14.0
		ctrl.AeEnable = True
	
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
		#for y in range(90): # cut off some of the noise
		#	for x in range(width):
		#		mask[y][x] = 0
		#	if y > 100:
		#		break
		num_food = numpy.sum(mask)
		result = cv2.bitwise_and(image, image, mask=mask)
		color = (255, 255, 255)
		if num_food < 6000000:
			color = (50, 50, 255)
		result = cv2.putText(result, str(num_food), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA, False)
		_, image_encoded = cv2.imencode('.jpg', result)
		data[0] = image_encoded
		
		if num_food >= 6000000:
			data[1].append([time.time(), int(num_food)])
	
	cam.stop()
