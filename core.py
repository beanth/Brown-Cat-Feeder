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

lower_color_bound = numpy.array([14, 0, 0])
upper_color_bound = numpy.array([30, 154, 154]) # my cat's coat color

def openTray():
    # 

def closeTray():
    #

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
                
                for frame in cam.capture_continuous(feed, format = "bgr", use_video_port = True):
                    image = frame.array
                    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv_image, lower_color_bound, upper_color_bound)
                    if numpy.sum(mask) > 200000: # my cat detected! 500x400 square of her coat
                        # potentially disable light, might mess with their vision more
                        openTray()
                        time.sleep(2) # wait for tray to open
                        while GPIO.input(SWITCH_PIN):
                            time.sleep(1)

                        closeTray()
                        break

                    # clear stream
                    feed.truncate(0)
        except:
            print("CAMERA NOT CONNECTED PROPERLY/ENABLED")


    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.5)
