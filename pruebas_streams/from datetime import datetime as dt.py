from datetime import datetime as dt
#Librería oficial de librealsense para la detección y manipulación de la cámara
import pyrealsense2 as rs
#Para convertir los frames de la cámara a numpy, que es la forma en la que cv puede trabajar con ellos para mostrarlos
import numpy as np
#Librería de opencv para la manipulación de imágenes y vídeos
import cv2

import os

pipe = rs.pipeline()
config = rs.config()
RUTA = "/AlzLab/"
RUTA_PLY = ""
RUTA_RAW = ""
RUTA_PNG =  ""
RUTA_CSV =  ""
RUTA_BIN =  ""
ruta_temp = ""


def definir_rutas():
    
    current_time = dt.now()
    ruta_grabacion = RUTA + str(current_time.timestamp()) + "/"

    try:
        if not os.path.exists(ruta_grabacion):
            os.makedirs(ruta_grabacion)
    
    except FileExistsError:
        print(f"La carpeta {ruta_grabacion} ya existe")

    RUTA_PLY = ruta_grabacion + "/PLY"
    RUTA_RAW = ruta_grabacion + "/RAW"
    RUTA_PNG =  ruta_grabacion + "/PNG"
    RUTA_CSV =  ruta_grabacion + "/CSV"
    RUTA_BIN =  ruta_grabacion + "/BIN"
    ruta_temp = RUTA + str(current_time.timestamp()) + ".bag"
    

    if not os.path.isdir(RUTA_PLY):
        
        try:
            os.mkdir(RUTA_PLY)
            print(f"Carpeta '{RUTA_PLY}' creada exitosamente")
                  
        except FileExistsError:
            print(f"La carpeta {RUTA_PLY} ya existe")

    if not os.path.isdir(RUTA_RAW):


        try:
            os.mkdir(RUTA_RAW)
            print(f"Carpeta '{RUTA_RAW}' creada exitosamente")
        except FileExistsError:
            print(f"La carpeta {RUTA_RAW} ya existe")



    if not os.path.isdir(RUTA_PNG):
        try:
            os.mkdir(RUTA_PNG)
            print(f"Carpeta '{RUTA_PNG}' creada exitosamente")
        except FileExistsError:
            print(f"La carpeta {RUTA_PNG} ya existe")

    if not os.path.isdir(RUTA_CSV):
        try:
            os.mkdir(RUTA_CSV)
            print(f"Carpeta '{RUTA_CSV}' creada exitosamente")
        except FileExistsError:
            print(f"La carpeta {RUTA_CSV} ya existe")

    if not os.path.isdir(RUTA_BIN):
        try:
            os.mkdir(RUTA_BIN)
            print(f"Carpeta '{RUTA_BIN}' creada exitosamente")
        except FileExistsError:
            print(f"La carpeta {RUTA_BIN} ya existe")
            
definir_rutas()