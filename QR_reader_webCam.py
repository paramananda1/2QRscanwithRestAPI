# To build Run : pyinstaller --onefile  QR_reader_webCam.py
# cp dist/QR_reader_webCam .
# ./QR_reader_webCam or.png 30  .........image and angel as input 
import json
import math
import sys

import cv2
import numpy as np
from pyzbar.pyzbar import decode


#########################################################################
#   barcodeReader()                                                     
#########################################################################
def barcodereder(image, debug):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcode = decode(gray_img)

    itemsFound = []
    for decodedObject in barcode:
        if debug:
            print("QR:\n", decodedObject)
        data = {"Data": decodedObject.data}
        vertices = decodedObject.polygon
        pts = np.array(vertices, np.int32)
        vertices = []
        for p in pts:
            d = {"X": p[0], "Y": p[1]}
            vertices.append(d)

        center = {
            "X": (pts[2][0] + pts[0][0]) / 2,
            "Y": (pts[2][1] + pts[0][1]) / 2
        }
        boundingBox = {
            "vertices": vertices,
            "center": center
        }
        rect = {
            "Left": decodedObject.rect[0],
            "Top": decodedObject.rect[1],
            "Width": decodedObject.rect[2],
            "Height": decodedObject.rect[3]
        }
        item = {
            "data": data,
            "boundingBox": boundingBox,
            "Rect": rect
        }

        itemsFound.append(item)
    # For loop END
    viewportGridSize = {
        "X": 50,
        "Y": 100
    }  ## TBD

    finalData = {
        "viewportGridSize": viewportGridSize,
        "itemsFound": itemsFound
    }
    if debug:
        print(finalData)

    # finalData_json = json.dump(finalData)
    return finalData


########################################################################
#   main process
##########################################################################
def process(frame, angel, debug):
    # Process frame from camera
    json_data = barcodereder(frame, debug)
    #
    # Distance between two points P(x1, y1) and Q(x2, y2) is
    # d(P, Q) = qurt( (x2 − x1)^2 + (y2 − y1)^2 )
    #
    center_1 = json_data["itemsFound"][0]["boundingBox"]["center"]
    center_2 = json_data["itemsFound"][1]["boundingBox"]["center"]
    h = math.sqrt(((center_2["X"] - center_1["X"]) ** 2) + ((center_2["Y"] - center_1["Y"]) ** 2))
    angleA = int(angel)  ## input
    angleB = 90  ## constant
    angleC = 90 - angleA
    #            A
    #        p  | \  h
    #           |  \
    #           B---C
    #             b
    #  if A = 30 => b = 90 and c = 60  , the value of h = center 1 - center 2
    # p =  cos(A) * h  ,  b = ( sin(A) * h )
    # Verify: h^2 = p^2 + b^2

    p = math.cos(angleA) * h
    # b = math.sin(angleA)*h
    b = math.sqrt((h * h) - (p * p))
    if debug:
        print(h * h)
        print((p * p) + (b * b))
        if (h * h) == (p * p) + (b * b):
            print("all side looks good:")
    dev_point = {
        "X": center_2["X"] - b,
        "Y": center_2["Y"] - b
    }
    all_points = {
        "center1": center_1,
        "center2": center_2,
        "deviation": dev_point
    }
    all_angle = {
        "A": angleA,
        "B": angleB,
        "C": angleC
    }
    final_json = {
        "QR-Data": json_data,
        "Points": all_points,
        "Angle": all_angle
    }

    if debug:
        print("\nfinal json data: \n", final_json)
    return final_json


########################################################################
#   Main()
#########################################################################
def main():
    # camera_port = 0
    # camera = cv2.VideoCapture(camera_port)
    # Check if camera opened successfully
    # if (cap.isOpened() == False):
    #    print("Error opening video stream or file")
    # cv2.waitKey()
    if len(sys.argv) < 3:
        return 0
    debug = False
    image = sys.argv[1]
    angel = sys.argv[2]
    camera = cv2.VideoCapture(image)
    print(sys.argv)
    # Read the frame from camera
    ret, frame = camera.read()
    if not ret:
        sys.exit("ERROR::: unable to Read the frame from camera \n")

    # release Camera so that others can use the camera as soon as possible
    camera.release()
    del camera
    final_data = process(frame, angel, debug)
    #final_data = json.dumps(str(process(frame, angel, debug)))
    if debug:
        print(final_data)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(str(final_data), f, ensure_ascii=False, indent=4)
    # When everything done, release the capture
    # cv2.destroyAllWindows()
    print(final_data)


if __name__ == '__main__':
    main()
