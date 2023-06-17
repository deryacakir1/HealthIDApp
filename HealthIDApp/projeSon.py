# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:56:47 2023

@author: melik
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from arayuzui import *
import cv2

uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

def ac():
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")


    org = (30,30)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    weared_mask = "Saglikli Degil!"
    not_weared_mask = "Saglikli"

    cap = cv2.VideoCapture(0)


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Acilamiyor!")
            
        gray_image = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray_image, 1.1, 7)
        
        if(len(faces) == 0):
            cv2.putText(frame, "Yuz Bulunamadi!", org, fontFace, 
                        fontScale, (255,255,255), 2)
        else:
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), 
                              (255,0,0), 2)
                roi_gray = gray_image[y:y+h, x:x+w]
                
                mouth = mouth_cascade.detectMultiScale(roi_gray,
                                                       1.4, 15)
                i = 0
                if(len(mouth) == 0):
                    cv2.putText(frame, weared_mask, org, fontFace,
                                fontScale, (0,0,255), 
                                2, cv2.LINE_AA)
                else:
                    cv2.putText(frame, not_weared_mask, org, 
                                fontFace, fontScale, (0,255,0),
                                4, cv2.LINE_AA)
                    for mx, my, mw, mh in mouth:
                        if i == 0:
                            i+=1
                            cv2.rectangle(frame, (mx+x,my+y),
                                          (mx+x+mw, my+y+mh), (0,0,255),3)
                        else:
                            pass
            
        cv2.imshow("Maske Tespiti Arayuzu",frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("by")
            break



    cap.release()
    cv2.destroyAllWindows()
    
    
ui.kameraAc.clicked.connect(ac)  
sys.exit(uygulama.exec_())  
