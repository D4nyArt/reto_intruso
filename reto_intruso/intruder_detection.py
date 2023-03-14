import numpy as np
import cv2
import tkinter as tk
from tkinter import *
import pygame

Contour_Area = 4000
History = 500
Dist2Threshold = 400

def alarma(cap, mov):
    
    
    #history: tamano del historico 
    #dist2Threshold: umbral de distancia al cuadrado, entre el pixel y la muestra para decidir si un pixel esta cerca de esa muestra
    #detectShadows: opcion para la deteccion de sombras

    cv2.ocl.setUseOpenCL(True)

    #while True:
    ret,frame = cap.read()
    
    #Si no se lee el video bien, se termina el programa
    if not ret:
        print("CAMERA PROBLEM")
        quit()
    
    #Aplicamos detector
    mascara = mov.apply(frame)
    
    #Creamos copia para detectar los contornos
    contornos = mascara.copy()
    
    #Busqueda de contornos
    con, jerarquia = cv2.findContours(contornos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #Iteracion de contornos
    for c in con:
        
        #Se elimina ruido (contornos pequenos)
        if cv2.contourArea(c) < Contour_Area:
            continue
        if cv2.contourArea(c) >= Contour_Area:
            
            #Obtenemos limites de contornos
            (x,y,w,h) = cv2.boundingRect(c)
            
            #Dibujo del rectangulo
            cv2.rectangle(frame, (x,y), (x+w, y+h),(0,0,255),2)
            cv2.rectangle(contornos, (x,y), (x+w, y+h),(0,0,255),2)
            cv2.putText(frame, '{}'.format("Alarma"),(x,y-5),1,1.3,(0,0,255),1,cv2.LINE_AA)
        #Mostramos la camara, mascara y contornos
        cv2.imshow("Alarma activa", frame)
        cv2.imshow("Umbral", mascara)
        cv2.imshow("Contornos", contornos)
        if cv2.waitKey(20) & 0xFF==ord('p'):
            print("Finished")
            quit()




def pantalla_principal(screen):

    pygame.display.flip()
    buttons = [[(255,0,0), [0, 20], [65, 200], 'Contour_Area', -250],
               [(0,255,0), [70, 20], [65, 200], 'Contour_Area', 250],]
    mouse = pygame.mouse.get_pos()

    conarstr = f'Contour Area: {Contour_Area}'
    historystr = f'History: {History}'
    dist2thresstr = f'Distance To Threshold: {Dist2Threshold}'

    for event in pygame.event.get():
        for color, coors, rect, var, val in buttons:
            #print(color)
            surface = pygame.Surface(rect)
            surface.fill(color)
            _rect = screen.blit(surface, coors)
                
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and _rect.collidepoint(mouse):
                #eval(f'{var}+={val}')
                globals()[var] += val
                print(globals()[var])


def main():
    #Creamos el video
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FOURCC, 0x32595559)
    cap.set(cv2.CAP_PROP_FPS, 25)


    (width, height) = (300, 300)
    screen = pygame.display.set_mode((width, height))

        #Llamada al detector de video
    
    mov = cv2.createBackgroundSubtractorKNN(history=History, dist2Threshold=Dist2Threshold, detectShadows=False)
    while True:    
        alarma(cap, mov)
        pantalla_principal(screen)   

main()


