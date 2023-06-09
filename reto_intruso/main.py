import numpy as np
import cv2
import tkinter as tk
from tkinter import *

def alarma():
    
    #Creamos el video
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FOURCC, 0x32595559)
    cap.set(cv2.CAP_PROP_FPS, 25)
    
    #Llamada al detector de video
    mov = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)
    
    #history: tamano del historico 
    #dist2Threshold: umbral de distancia al cuadrado, entre el pixel y la muestra para decidir si un pixel esta cerca de esa muestra
    #detectShadows: opcion para la deteccion de sombras

    cv2.ocl.setUseOpenCL(True)

    while True:
        ret,frame = cap.read()
        
        #Si no se lee el video bien, se termina el programa
        if not ret:
            print("CAMERA PROBLEM")
            break
        
        #Aplicamos detector
        mascara = mov.apply(frame)
        
        #Creamos copia para detectar los contornos
        contornos = mascara.copy()
        
        #Busqueda de contornos
        con, jerarquia = cv2.findContours(contornos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        #Iteracion de contornos
        for c in con:
            
            #Se elimina ruido (contornos pequenos)
            if cv2.contourArea(c) < 4000:
                continue
            if cv2.contourArea(c) >= 4000:
                
                #Obtenemos limites de contornos
                (x,y,w,h) = cv2.boundingRect(c)
                
                #Dibujo del rectangulo
                cv2.rectangle(frame, (x,y), (x+w, y+h),(0,0,255),2)
                cv2.putText(frame, '{}'.format("Alarma"),(x,y-5),1,1.3,(0,0,255),1,cv2.LINE_AA)

            #Mostramos la camara, mascara y contornos
            cv2.imshow("Alarma activa", frame)
            cv2.imshow("Umbral", mascara)
            cv2.imshow("Contornos", contornos)

            if cv2.waitKey(20) & 0xFF==ord('p'):
                print("Finished")
                return

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


