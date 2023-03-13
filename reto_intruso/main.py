import numpy as np
import cv2
import tkinter as tk
from tkinter import *

def alarma():
    
    cap = cv2.VideoCapture(1)
    mov = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)

    cv2.ocl.setUseOpenCL(True)

    while True:
        ret,frame = cap.read()

        if not ret:
            print("CAMERA PROBLEM")
            break

        mascara = mov.apply(frame)

        contornos = mascara.copy()

        con, jerarquia = cv2.findContours(contornos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in con:
            if cv2.contourArea(c) < 4000:
                continue
            if cv2.contourArea(c) >= 4000:
                (x,y,w,h) = cv2.boundingRect(c)

                cv2.rectangle(frame, (x,y), (x+w, y+h),(0,0,255),2)
                cv2.putText(frame, '{}'.format("Alarma"),(x,y-5),1,1.3,(0,0,255),1,cv2.LINE_AA)

            cv2.imshow("Alarma activa", frame)
            cv2.imshow("Umbral", mascara)
            cv2.imshow("Contornos", contornos)

            k = cv2.waitKey(5)
            if k ==  27:
                break

    cap.release()
    cv2.destroyAllWindows()

def normal():
    cap = cv2.VideoCapture(0)
    mov = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)

    cv2.ocl.setUseOpenCL(False)

    while(True):
        ret,frame = cap.read()

        if not ret:
            break
        
        mascara = mov.apply(frame)

        contornos = mascara.copy()

        con, jerarquia = cv2.findContours(contornos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in con:
            if cv2.contourArea(c) < 1500:
                continue
            if cv2.contourArea(c) >= 1500:
                (x,y,w,h) = cv2.boundingRect(c)

                cv2.rectangle(frame, (x,y), (x+w, y+h),(0,0,255),2)
                cv2.putText(frame, '{}'.format("Alarma"),(x,y-5),1,1.3,(0,0,255),1,cv2.LINE_AA)

            cv2.imshow("Alarma Inactiva", frame)
            cv2.imshow("Umbral", mascara)
            cv2.imshow("Contornos", contornos)

            k = cv2.waitKey(5)
            if k ==  27:
                break

        cap.release()
        cv2.destroyAllWindows()



def pantalla_principal():
    global pantalla
    pantalla = Tk()
    pantalla.geometry("400x350")
    pantalla.title("Intruder deteccion")
    Label(text="sistema de seguridad", bg = 'gray', width="300", height="2", font = ("Verdana, 13")).pack()
    Label(pantalla, text="").pack()
    Button(text= "Activar alarma", height=2, width=30, command=alarma).pack()
    Label(pantalla, text="").pack()
    Button(text= "Desactivar alarma", height=2, width=30, command=normal).pack()
    pantalla.mainloop()

alarma()


