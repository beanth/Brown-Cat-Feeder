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

while True:
    if GPIO.input(SWITCH_PIN):
        GPIO.output(LED_PIN, GPIO.HIGH)
        with PiCamera() as cam:
            cam.resolution = (640, 480)
            cam.framerate = 32
            feed = PiRGBArray(cam, size = (640, 480))
            time.sleep(1)

            for frame in cam.capture_continuous(feed, format="bgr", use_video_port=True):
                image = frame.array
                cv2.imshow("Frame", image)
                # clear the stream in preparation for the next frame
                feed.truncate(0)


    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.5)