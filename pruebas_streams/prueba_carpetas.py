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
temp_rec_route = ""


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
    temp_rec_route = RUTA + str(current_time.timestamp()) + ".bag"
    

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



def grabar_datos():
    pipe = rs.pipeline()
    config = rs.config()

    definir_rutas()

    config.enable_record_to_file(temp_rec_route)

    config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    pipe.start(config)

    while True:
        frames = pipe.wait_for_frames()
        
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        color_frame_data = np.asanyarray(color_frame.get_data())
        depth_frame_data = np.asanyarray(depth_frame.get_data())   
        depth_color_map = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame_data, 
                                                                alpha=0.5), cv2.COLORMAP_JET) 
        
        cv2.imshow('Color Frame', color_frame_data)
        cv2.imshow('Depth Frame', depth_color_map)

        if cv2.waitKey(1) == ord('q'):
            break
    pipe.stop()



def mostrar_datos():
    pipe = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    pipe.start(config)

    while True:
        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        color_frame_data = np.asanyarray(color_frame.get_data())
        depth_frame_data = np.asanyarray(depth_frame.get_data())   
        depth_color_map = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame_data, 
                                                                alpha=0.5), cv2.COLORMAP_JET) 
        
        cv2.imshow('Color Frame', color_frame_data)
        cv2.imshow('Depth Frame', depth_color_map)

            
        if cv2.waitKey(1) == ord('q'):
            break    
    pipe.stop()


