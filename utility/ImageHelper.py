import cv2
from PIL import Image

SAVE_IMAGE_DIRECTORY = ".\images\\"

def ConvertImageToPNG(fileName, image_array):
    im = Image.fromarray(image_array)
    im.save(SAVE_IMAGE_DIRECTORY + fileName + ".jpeg")


def GetSampleImage(id):
    return cv2.imread(".\images\\testimg"+ id +".jpeg")
