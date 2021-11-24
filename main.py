import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller
cap=cv2.VideoCapture(0)
#0 is web cam id
cap.set(3,1280)
cap.set(4,720)

detector=HandDetector(detectionCon=0.8)
Blist=[]
def drawAllKeys(Blist,img):
    for i in Blist:
        x,y=i.pos
        w,h=i.size
        cv2.rectangle(img,i.pos,(x+w,y+h),(0,0,0),cv2.FILLED)
        cv2.putText(img,i.text,(x+25,y+60),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)
    return img
    
class Buttons():
    def __init__(self,pos,text,size=[100,100]):
        self.pos=pos
        self.size=size
        self.text=text





listOfKeys=[["Q","W","E","R","T","Y","U","I","O","P"],
           ["A","S","D","F","G","H","J","K","L",";"],
           ["Z","X","C","V","B","N","M",",",".","/"]]
kb=Controller()
for i in range(len(listOfKeys)):
        for j,key in enumerate(listOfKeys[i]):
            Blist.append(Buttons((100*j+25,100*i+25),key))
    
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList,bbx=detector.findPosition(img)
    #lmList,bboxInfo=detector.findHand(img)
    #img=sample.drawKeys(img)
    img=drawAllKeys(Blist,img)
    if lmList:
        for i in Blist:
            x,y=i.pos
            w,h=i.size
            #mediapipe index finger landmark is 8
            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img,i.pos,(x+w,y+h),(255,0,0),cv2.FILLED)
                cv2.putText(img,i.text,(x+30,y+55),cv2.FONT_HERSHEY_PLAIN,5,(255,0,255),5)
                dist, _, _ =detector.findDistance(8,12,img)
                if dist<39:
                    kb.press(i.text)
                    cv2.rectangle(img,i.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
                    cv2.putText(img,i.text,(x+30,y+55),cv2.FONT_HERSHEY_PLAIN,5,(0,0,0),5)
                    sleep(0.25)
                    
                
    cv2.imshow("Image",img)
    cv2.waitKey(1)
