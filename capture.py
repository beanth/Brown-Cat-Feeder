import cv2
import time
import numpy

_, image_encoded = cv2.imencode('.jpg', cv2.imread('images/no-sample.jpg'))
samples = [["now", 53.1]]

current_frame = image_encoded

_, image_encoded = cv2.imencode('.jpg', cv2.imread('images/front.png'))

current_frame = image_encoded