# Automatic-Cat-Feeder
Allows a Raspberry Pi to detect a brown cat using OpenCV, revealing a food bowl.  
Looks for certain colors only present in my cat's fur so that my roommates' cat can't eat her food.

## How to install
Run `pip install --upgrade pip setuptools wheel numpy` first, and then `apt-get install libhdf5-dev libatlas3-base libjasper-dev`. Finally, run `pip install -r requirements.txt` in root of repo.  
You must enable Legacy Camera support using `raspi-config`.

## How it works
First, the Pi detects the presence of a cat using a limit switch underneath a platform.  
Then, it turns on an array of white LEDs in order to aid with lighting.  
Finally, it enables the camera and uses OpenCV in order to detect if it is the proper cat.  
If it is the proper cat, it uses a stepper motor driving a pinion on a rack in order to reveal the food bowl and allows the cat to eat.  
It waits for the cat to step off the platform, and retracts the food bowl after disabling the light.

## How to setup
Hardware:
 - Raspberry Pi 3+ (tested with Raspberry 4 Model B)
 - A Raspberry Pi compatible 1080p camera
 - One limit switch
 - A ULN2003 stepper motor driver
 - A 28BYJ-48 5V stepper motor
 - Bright white LEDs
 - 3D printed parts, will release later potentially

Install the camera in to the ribbon cable slot on the Raspberry Pi board.  
Wire up the limit switch to the respective pin you chose in `core.py`.  
Wire up the stepper motor to the motor driver.  
Wire the motor driver to the respective pins for the motor phases in `core.py`.  
Wire the white LEDs to the pin you chose in `core.py`.  
Place a platform on top of the limit switch.  
Mount the camera above the platform facing downward.  
Place the food bowl in the food shelf and position in front of platform.
