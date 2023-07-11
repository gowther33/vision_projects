import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = (157-50), (240-192)


def checkParkingSpace(imgProc):

    spaceCounter = 0

    for pos in posList:
        x,y = pos
        imgCrop = imgProc[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), imgCrop)
    
        # We are going to count the pixels each of the car spaces has if there are many then there is a car otherwise no car
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, 
                           str(count),(x,y+height-3), 
                           scale=1, 
                           thickness=2, 
                           offset=0,
                           colorR=(0,0,255)
                        )
        # Space is free
        if count < 900:
            color = (0,255,0) #green
            thickness = 5
            spaceCounter += 1
        # Not free
        else:
            color = (0,0,255) #red
            thickness = 2

        cv2.rectangle(img, 
                    pos, 
                    (pos[0]+width, pos[1]+height), 
                    color,
                    thickness
                )
    cvzone.putTextRect(img, 
                        f"Free Spaces: {spaceCounter}/{len(posList)}",(100,50), 
                        scale=3, 
                        thickness=5, 
                        offset=20,
                        colorR=(0,200,0)
                    )
            
while True:
    # If current frame == total frames then start from 0
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = cap.read()
    # convert to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3),1)
    # Convert to binary image
    imgThreshold = cv2.adaptiveThreshold(imgBlur,
                                        255, 
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 
                                        25, 
                                        16
                                    )

    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.uint8)

    imgDilate = cv2.dilate(imgMedian,kernel=kernel, iterations=1)


    checkParkingSpace(imgDilate)

    
    cv2.imshow("image",img)
    # cv2.imshow("imageBlur",imgBlur)
    # cv2.imshow("imageThres",imgMedian)
    cv2.waitKey(10)