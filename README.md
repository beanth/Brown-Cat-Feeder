# Brown-Cat-Feeder
 Allows a Raspberry Pi 4 to detect a brown cat using OpenCV and reveal a food bowl.

Looks for certain colors only present in my cat's coat so that my roommates' cat
doesn't eat all of her food.

First, the Pi detects the presence of a cat using limit switches in a platform.
Then, it turns on an array of white LEDs in order to allow the camera to see the color
of the cat better. Finally, it enables the camera and uses OpenCV in order to detect
if it is the proper cat. If it's the proper cat, it uses a stepper motor in order to reveal
the food bowl and allows them to eat.