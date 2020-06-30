import cv2
import numpy as np

#capturing our video from webcam
cap=cv2.VideoCapture(0)
#setting frame width and height
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)

'''
other color values
myColors=[[5,107,0,19,255,255],
            [133,56,0,159,156,255],
            [57,76,0,100,255,255],
            [90,48,0,118,255,255]]
colorValues=[[51,153,255],          ## BGR
                 [255,0,255],
                 [0,255,0],
                 [255,0,0]]
                 
'''
#list of our colors
#orange , purple ,green
myColors=[
[57,76,0,100,255,255],
            ]
colorValues=[          ## BGR
                 [0,255,0],
               ]
  #BGR


#x,y,colorIndex
mypoints=[]


#getting colors from myColors list
#setting the upper and lower values and create a mask
def findColor(img,myColors,colorValues):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        #cv2.imshow(str(color[0]), mask)
        #now we get our mask values in image using contours
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),15,colorValues[count],cv2.FILLED)
        if(x!=0 and y!=0):
            newPoints.append([x,y,count])
        count+=1
    return newPoints


#our get contours from detecting shapes module
def getContours(img):
    countours,Hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    ObjectType=""
    x,y,w,h=0,0,0,0
    #contours are curve joining all continous points
    for cnt in countours:
        area=cv2.contourArea(cnt)
        if(area>500):
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            perimeter=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*perimeter,True)
            #print(len(approx))
            objCorner=len(approx)
            x, y, w, h=cv2.boundingRect(approx)
    return x+w//2,y

# to draw points on canvas
def drawOnCanvas(mypoints,colorValues):
    for point in mypoints:
        cv2.circle(imgResult,(point[0],point[1]),10,colorValues[point[2]],cv2.FILLED)

while True:
    success, img=cap.read()
    imgResult=img.copy()
    newPoints=findColor(img, myColors,colorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            mypoints.append(newP)
    if len(mypoints)!=0:
        drawOnCanvas(mypoints,colorValues)
    cv2.imshow("video",imgResult)

    if cv2.waitKey(1)&0xFF==ord('q'):
        cv2.destroyAllWindows()
        break
