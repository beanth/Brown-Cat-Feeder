from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
import cv2
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# PIN CONSTANTS
LED_PIN = 3
MOTOR_PIN = 5
SWITCH_PIN = 7

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN)

upper_color_bound = numpy.array([30, 154, 154])

while True:
    if GPIO.input(SWITCH_PIN):
        print("ACTIVATED")
        GPIO.output(LED_PIN, GPIO.HIGH)
        
        try:
            with PiCamera() as cam:
                cam.resolution = (1920, 1080)
                cam.framerate = 30
                feed = PiRGBArray(cam, size = (1920, 1080))
                time.sleep(1)
                
                for frame in cam.capture_continuous(feed, format="bgr", use_video_port=True):
                    image = frame.array
                    cv2.imshow("Frame", image)
                    # clear stream
                    feed.truncate(0)
        except:
            print("CAMERA NOT CONNECTED PROPERLY/ENABLED")


    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.5)
