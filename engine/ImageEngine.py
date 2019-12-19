import math
import time

import cv2
import numpy as np
import pytesseract as pytesseract
from imutils.object_detection import non_max_suppression

from utility import ImageHelper

DEBUG = True

def find_template(img, template):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = template.shape

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)


    if(DEBUG):
        cv2.imshow("Template", template)
        cv2.imshow("Find Template", img)
        cv2.waitKey(0)

    return loc[::-1]

def scan_image_old(app_img):
    ImageHelper.ConvertImageToPNG("est1", app_img)

    grey_screen_image = cv2.cvtColor(app_img, cv2.COLOR_BGR2GRAY)
    ImageHelper.ConvertImageToPNG("est2", grey_screen_image)

    ret, mask = cv2.threshold(grey_screen_image, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(grey_screen_image, grey_screen_image, mask=mask)
    ImageHelper.ConvertImageToPNG("est3", image_final)

    ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)
    ImageHelper.ConvertImageToPNG("est4", new_img)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation
    ImageHelper.ConvertImageToPNG("est5", dilated)

    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    index = 0
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        # Don't plot small false positives that aren't text
        if w < 35 and h < 35:
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(app_img, (x, y), (x + w, y + h), (255, 0, 255), 2)


        #you can crop image and send to OCR  , false detected will return no text :)
        cropped = app_img[y :y +  h , x : x + w]
        config = ("-l eng --oem 1 --psm 13")
        scanned_text = pytesseract.image_to_string(cropped,config=config)

        s = 'images/cropped/crop_' + str(index) + '_' + scanned_text + '_.jpg'
        cv2.imwrite(s , cropped)
        index = index + 1

    # write original image with added contours to disk
    ImageHelper.ConvertImageToPNG("est7", app_img)
    cv2.imshow('\images\captcha_result', app_img)
    cv2.waitKey()

def scan_image(img):
    ImageHelper.ConvertImageToPNG("est1", img)
    app_img = img.copy()

    app_img = cv2.medianBlur(app_img, 3)
    ImageHelper.ConvertImageToPNG("est1_2", app_img)
    cv2.imshow("Output2", app_img)

    grey_screen_image = cv2.cvtColor(app_img, cv2.COLOR_BGR2GRAY)
    ImageHelper.ConvertImageToPNG("est2", grey_screen_image)

    ret, mask = cv2.threshold(grey_screen_image, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(grey_screen_image, grey_screen_image, mask=mask)
    ImageHelper.ConvertImageToPNG("est3", image_final)

    ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)
    ImageHelper.ConvertImageToPNG("est4", new_img)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated = cv2.dilate(new_img, kernel, iterations=9)  # dilate , more the iteration more the dilation
    ImageHelper.ConvertImageToPNG("est5", dilated)

    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    index = 0
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        # Don't plot small false positives that aren't text
        if w < 35 and h < 35:
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(app_img, (x, y), (x + w, y + h), (255, 0, 255), 2)


        #you can crop image and send to OCR  , false detected will return no text :)
        cropped = app_img[y :y +  h , x : x + w]
        config = ("-l eng --oem 1 --psm 13")
        scanned_text = pytesseract.image_to_string(cropped,config=config)

        s = 'images/cropped/crop_' + str(index) + '_' + scanned_text + '_.jpg'
        cv2.imwrite(s , cropped)
        index = index + 1

    # write original image with added contours to disk
    ImageHelper.ConvertImageToPNG("est7", app_img)
    cv2.imshow('\images\captcha_result', app_img)
    cv2.waitKey()


def decode_predictions(scores, geometry):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scoresData[x] < 0.5:
                continue

            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)

def scan_image3(org_img, width, height, east, min_confidence = 0.5):
    # load the input image and grab the image dimensions
    image = org_img
    #image = cv2.imread(".\images\est1.jpeg")
    orig = image.copy()
    (H, W) = image.shape[:2]


    width = math.floor(width / 32) * 32
    height = math.floor(height / 32) * 32
    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    rW = W / float(newW)
    rH = H / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east)

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []

    alloutput = ""

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((endX - startX) * 0.0)
        dY = int((endY - startY) * 0.1)

        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(width, endX + (dX * 2))
        endY = min(height, endY + (dY * 2))

        # extract the actual padded ROI
        roi = orig[startY:endY, startX:endX]

        # in order to apply Tesseract v4 to OCR text we must supply
        # (1) a language, (2) an OEM flag of 4, indicating that the we
        # wish to use the LSTM neural net model for OCR, and finally
        # (3) an OEM value, in this case, 7 which implies that we are
        # treating the ROI as a single line of text
        config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(roi, config=config)

        # add the bounding box coordinates and OCR'd text to the list
        # of results
        results.append(((startX, startY, endX, endY), text))

        # sort the results bounding box coordinates from top to bottom
        results = sorted(results, key=lambda r: r[0][1])
        output = orig.copy()

        # loop over the results
        for ((startX, startY, endX, endY), text) in results:
            # display the text OCR'd by Tesseract
            alloutput = alloutput + text + ", "

            # strip out non-ASCII text so we can draw the text on the image
            # using OpenCV, then draw the text and a bounding box surrounding
            # the text region of the input image
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()

            cv2.rectangle(output, (startX, startY), (endX, endY),
                          (0, 0, 255), 2)
            cv2.putText(output, text, (startX, startY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
    print("Final TEXT")
    print("========")
    print("{}\n".format(alloutput))
        # show the output image
    cv2.imshow("Text Detection", output)
    cv2.waitKey(0)

def scan_image2(org_img, width, height, east, min_confidence = 0.5):
    # load the input image and grab the image dimensions
    image = org_img
    #image = cv2.imread(".\images\est1.jpeg")
    orig = image.copy()
    (H, W) = image.shape[:2]


    width = math.floor(width / 32) * 32
    height = math.floor(height / 32) * 32
    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    rW = W / float(newW)
    rH = H / float(newH)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east)

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []

    alloutput = ""

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((endX - startX) * 0.0)
        dY = int((endY - startY) * 0.1)

        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(width, endX + (dX * 2))
        endY = min(height, endY + (dY * 2))

        # extract the actual padded ROI
        roi = orig[startY:endY, startX:endX]

        # in order to apply Tesseract v4 to OCR text we must supply
        # (1) a language, (2) an OEM flag of 4, indicating that the we
        # wish to use the LSTM neural net model for OCR, and finally
        # (3) an OEM value, in this case, 7 which implies that we are
        # treating the ROI as a single line of text
        config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(roi, config=config)

        # add the bounding box coordinates and OCR'd text to the list
        # of results
        results.append(((startX, startY, endX, endY), text))
        alloutput = alloutput + text + ", "
        # sort the results bounding box coordinates from top to bottom
        results = sorted(results, key=lambda r: r[0][1])
        output = orig.copy()

    print("Final TEXT")
    print("========")
    print("{}\n".format(alloutput))
        # show the output image
    cv2.imshow("Text Detection", output)
    cv2.waitKey(0)