# Description
This is a bot that uses pyautogui and some android emulator to help automate certain tasks in the mobile game 
King's Raid. The program CV2 to help with capturing images, and matching based on templates to find locations of 
where to click. CV2 is also used for some pre image processing for using Python-Tesseract as an optical character 
recognition (OCR) tool that utilizes machine learning to determine characters. A UI is also implemented using eel. 'Eel 
is a little Python library for making simple Electron-like offline HTML/JS GUI apps, with full access to Python 
capabilities and libraries'. Eel was mainly used because the GUI was done using HTML and since, I am familiar with 
styling it was an easier choice.

# TODO
There is a lot more I want to do but here is an in-completed todo list (it was probably continue to grow)
- [ ]  Improve accuracy of image recognition
    - [ ]  Change to black and white (rather then grey+black)
    - [ ]  Log images
    - [ ]  Teach tesseract?
    - [ ]  Parallelize?
- [x]  Implement page scrolling
- [x]  Fix Button clicking for events.
- [ ]  Implement Cached position for buttons (rather then template match for grind)
- [ ]  improve logging
- [x]  Clean up code
    - [x]  segment into modules? (inventory module)
    - [x]  segment into Macros and micro functions and utility?? and logging
- [ ]  Implement randomization
- [ ]  Allow repositioning of NOX
- [x]  Start on league of honor as next module
    - [ ]  Universal Hero class
    - [ ]  Figure out a method to check skills + exec + check if alive
    - [x]  Pick and Ban phase
        - [x]  Pick and Ban priority
- [x]  Create a GUI
- [ ]  Show Error Items
- [ ]  How to exit prematurely
- [x]  Add Scrolling

##CV2 
OpenCV-Python - used to solve computer vision problems.

## Tesseract (don't need anymore?)
Used for image to text
pip install pytesseract

https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/
pip install --upgrade imutils
https://github.com/ZER-0-NE/EAST-Detector-for-text-detection-using-OpenCV

https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00#introduction
