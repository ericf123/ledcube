#LED cube
This is a collection of Python scripts and an Arduino sketch to control a 4x4x4 cube of LEDs. I built it for E40M at Stanford.
##Project Structure
In the `src` directory, you will find three subdirectories:
* controller
* arduino
* test

###controller
This directory holds the Python scripts used to control the LED cube over serial. 

####main.py
Runs a loop that displays a menu asking for what to do, then runs that action. 

####vision.py
Uses OpenCV to apply an HSV filter to the webcam image. It draws a bounding box around the largest green contour it finds using the HSV filter, and gets the angle of this box. 
This angle is translated into a z-value on [0,3], which corresponds to the active plane on the cube.

####corner.py
Displays a pattern that expands from (0,0,0) to (3,3,3) and then goes back the other way. And back. And forth. And back. And forth.

####raindrop.py
Displays a pattern that is supposed to look like rain falling.

####symbol.py 
Creates a map from characters to a 2D-cube representation. 

####cubestate.py
This is basically the core of the controller system. It encodes the current state of all of the LEDs on the cube as 8 bytes of data for transmission over serial. 
The encoding is done primarly to prevent overflowing the 64 byte serial buffer on the Arduino. Since we can change the state of the entire cube 8 times before filling the buffer, we can change the state of the cube extremely quickly and often.
The method for encoding the data is described in detail in the file itself.

####expirationqueue.py
Provides a convenient wrapper around deque that only pops off elements if a certain amount of time has passed. 
This can be used to make LEDs turn off automatically after a certain amount of time. cubestate leverages expirationqueue to do exactly this.

####snake.py 
This is an unfinished 3D snake game I tried to write for the cube. As of now, it moves a single LED around the cube and responds (poorly) to input from the keyboard (WASD).

###arduino
Stores the Arduino sketch that runs on the microcontroller. It basically reads any available serial input, decodes it, and uses it to drive the multiplexed LED cube.

###test
These are a bunch of test files I wrote while debugging/working on new features. You should pretty much ignore everything in here.

##Usage
Run `python main.py` in the `controller` directory to get a loop that displays a menu with everything you can do with the cube.
If you get an error like `Could not open serial port. Bye.` It means you must change the path in the line where the cubestate instance is created in `main.py`. This should be the path to the serial port to which the Arduino is connected.

While running, each menu option can be terminated by pressing `^C` (ctrl+c), which will return you to the menu.

##Dependencies
* Python 3
* OpenCV 3 (with Python 3 bindings)
* numpy
* pySerial


##Contributing
Why would you?



