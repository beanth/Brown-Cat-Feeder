from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
import cv2
import time
import numpy

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# PIN CONSTANTS
LED_PIN = 3
SWITCH_PIN = 4

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
GPIO.setup(SWITCH_PIN, GPIO.IN)

# MOTOR PHASES
MOTOR_PINS = [0, 5, 6, 13] #[27, 29, 31, 33]
TRAY_EXTEND_DEGREES = 360 # 4096 for full rotation
STEPS_PER_ROTATION = 4096
STEP_TIME = 0.001 # 0.002 # time to wait between each step
# if set too low, steps will be skipped
STEP_SEQUENCE = [[1, 0, 0, 1],
                 [1, 0, 0, 0],
                 [1, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 1],
                 [0, 0, 0, 1]]

for i in range(len(MOTOR_PINS)):
    print(i)
    GPIO.setup(MOTOR_PINS[i], GPIO.OUT)
    GPIO.output(MOTOR_PINS[i], GPIO.LOW)

lower_color_bound = numpy.array([14, 0, 0])
upper_color_bound = numpy.array([30, 154, 154]) # my cat's coat color

CAMERA_X_RES = 1920
CAMERA_Y_RES = 1088

motor_steps = 0

def runMotor(degrees, direction): # direction: true is cw, false is ccw
    global motor_steps
    for i in range(round(degrees / 360 * STEPS_PER_ROTATION)):
        for pin in range(len(MOTOR_PINS)):
            GPIO.output(MOTOR_PINS[pin], STEP_SEQUENCE[motor_steps % len(STEP_SEQUENCE)][pin])

        if direction:
            motor_steps -= 1
        else:
            motor_steps += 1

        time.sleep(STEP_TIME)

def openTray():
    print("OPENING TRAY")
    runMotor(TRAY_EXTEND_DEGREES, False)

def closeTray():
    print("CLOSING TRAY")
    runMotor(TRAY_EXTEND_DEGREES, True)

while True:
    if GPIO.input(SWITCH_PIN):
        print("ACTIVATED")
        GPIO.output(LED_PIN, GPIO.HIGH)
        
        try:
            with PiCamera() as cam:
                cam.resolution = (CAMERA_X_RES, CAMERA_Y_RES) # set up camera
                cam.framerate = 30
                feed = PiRGBArray(cam, size = (CAMERA_X_RES, CAMERA_Y_RES))
                time.sleep(1) # let sensor adjust exposure etc.
                
                for frame in cam.capture_continuous(feed, format = "bgr", use_video_port = True):
                    image = frame.array
                    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # convert to HSV for use with inRange
                    mask = cv2.inRange(hsv_image, lower_color_bound, upper_color_bound) # create a bit mask

                    # of what pixels fall within the color range
                    if numpy.sum(mask) > 10:#384000: # my cat detected! 500x400 square of her coat was found
                        # -- potentially disable light, might mess with their vision more -- #
                        openTray() # open the food tray

                        while GPIO.input(SWITCH_PIN): # wait for the kitty to eat
                            time.sleep(1)

                        GPIO.output(LED_PIN, GPIO.LOW)
                        feed.truncate(0)
                        closeTray() # close the food tray
                        break

                    # clear stream
                    feed.truncate(0)
        except:
            print("CAMERA NOT CONNECTED PROPERLY/ENABLED")


    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.1)
