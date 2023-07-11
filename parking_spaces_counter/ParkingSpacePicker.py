import cv2
import pickle


try:
    # Save positions in the pickle object
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

width, height = (157-50), (240-192)


def mouseClick(events, x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for ind,pos in enumerate(posList):
            x1,y1 = pos
            if x1 < x < x1+width and y1 < y < y1+height:
                posList.pop(ind)

    # Save positions in the pickle object
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    img = cv2.imread('carParkImg.png')
    # p1 = start point (x,y), p2 = (width,height)
    # Marking parking space 
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), (255,0,255),2)

    cv2.imshow("image", img)
    # Detect Mouse click
    cv2.setMouseCallback("image", mouseClick)
    cv2.waitKey(1)
