from datetime import datetime as dt
#Librería oficial de librealsense para la detección y manipulación de la cámara
import pyrealsense2 as rs
#Para convertir los frames de la cámara a numpy, que es la forma en la que cv puede trabajar con ellos para mostrarlos
import numpy as np
#Librería de opencv para la manipulación de imágenes y vídeos
import cv2

#Crear u
pipe = rs.pipeline()
config = rs.config()

current_time = dt.now()
grabacion = "C:/Users/52644/Documents/GitHub/AlzLab/" + str(current_time.timestamp()) + ".bag"

config.enable_record_to_file(grabacion)


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