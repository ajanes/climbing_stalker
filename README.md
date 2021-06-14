# ClimbingStalker

A python application that detects and tracks climbers movements with a Stereolabs ZED2 and writes the collected data in csv files.

The main file you need to run is stalker.py, which needs all the files except the cv_viewer folder, the stalker_gui.py and the methode_tests.py.

For testing and understanding while running live stalker_gui.py can be used, it has all the features of stalker.py but also a GUI and it can print data into the console. Writing into files has to be activated in code.

For testing with already existing data methode_tests.py can be used to test the code with not easy to reproduce situations.

Coordinates are given by the following rules:

X: left to right, 0 in the middle, body center as point on axes
Y: bottom to top, 0 in the middle, body center as point on axes
Z: Front to back, 0 at camera

Position in m
Velocity in m/s
Dimensions in m

This Code contains Code from the ZED SDK Samples used as inspiration

The code supports 2 modes to get y_velocity. One uses the given velocity from the camera, the other one calculates it from the positions.
If you use the velocity from the camera you can ignore the last coloum in the CSV file. 
