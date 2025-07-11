from datetime import datetime as dt
#Librería oficial de librealsense para la detección y manipulación de la cámara
import pyrealsense2 as rs
#Para convertir los frames de la cámara a numpy, que es la forma en la que cv puede trabajar con ellos para mostrarlos
import numpy as np
#Librería de opencv para la manipulación de imágenes y vídeos
import cv2
#Importa el modulo para trabajar con el sistema operativo. Necesario para crear las carpetas y extraer los datos de la cámara
import os

import subprocess

import threading

RUTA = "/AlzLab/"
RUTA_PLY = ""
RUTA_RAW = ""
RUTA_PNG =  ""
RUTA_CSV =  ""
RUTA_BIN =  ""
temp_rec_route = ""
RUTA_EXTRACTOR = r"C:\Program Files (x86)\Intel RealSense SDK 2.0\tools"


def definir_rutas():
    
    global temp_rec_route
    global RUTA_PLY
    global RUTA_RAW
    global RUTA_PNG
    global RUTA_CSV
    global RUTA_BIN 

    current_time = dt.now()
    current_time_stamp_str = str(current_time.timestamp())
    temp_rec_route = RUTA + current_time_stamp_str + "/"

    try:
        if not os.path.exists(temp_rec_route):
            os.makedirs(temp_rec_route)
    
    except FileExistsError:
        print(f"La carpeta {temp_rec_route} ya existe")

    RUTA_PLY = temp_rec_route + "/PLY"
    RUTA_RAW = temp_rec_route + "/RAW"
    RUTA_PNG =  temp_rec_route + "/PNG"
    RUTA_CSV =  temp_rec_route + "/CSV"
    RUTA_BIN =  temp_rec_route + "/BIN"
    temp_rec_route = RUTA + current_time_stamp_str + ".bag"
    
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

def exportar_datos_ply():
    directorio_original = os.getcwd() 
    
    try:
        os.chdir(RUTA_EXTRACTOR)
        print(f"Cambiado al directorio: {os.getcwd()}")

        comando = [
            "rs-convert.exe",
            "-i",
            temp_rec_route,
            "-l",
            RUTA_PLY + "/PLY"
        ]
        
        print(f"Ejecutando comando: {' '.join(comando)}")

        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        
        print("\n--- Extracción finalizada ---")
        if resultado.stdout:
            print("Salida de rs-convert.exe:")
            print(resultado.stdout)
        if resultado.stderr:
            print("Errores (stderr) de rs-convert.exe:")
            print(resultado.stderr)

    except FileNotFoundError:
        print(f"Error: No se encontró 'rs-convert.exe' en '{RUTA_EXTRACTOR}'. Asegúrate de que la ruta es correcta.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar rs-convert.exe. Código de salida: {e.returncode}")
        print(f"Salida estándar (stdout): {e.stdout}")
        print(f"Salida de error (stderr): {e.stderr}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        os.chdir(directorio_original)
        print(f"Vuelto al directorio original: {os.getcwd()}")

def exportar_datos_raw():
    
    directorio_original = os.getcwd() 
    
    try:
        os.chdir(RUTA_EXTRACTOR)
        print(f"Cambiado al directorio: {os.getcwd()}")

        comando = [
            "rs-convert.exe",
            "-i",
            temp_rec_route,
            "-r",
            RUTA_RAW + "/RAW"
        ]
        
        print(f"Ejecutando comando: {' '.join(comando)}")

        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        
        print("\n--- Extracción finalizada ---")
        if resultado.stdout:
            print("Salida de rs-convert.exe:")
            print(resultado.stdout)
        if resultado.stderr:
            print("Errores (stderr) de rs-convert.exe:")
            print(resultado.stderr)

    except FileNotFoundError:
        print(f"Error: No se encontró 'rs-convert.exe' en '{RUTA_EXTRACTOR}'. Asegúrate de que la ruta es correcta.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar rs-convert.exe. Código de salida: {e.returncode}")
        print(f"Salida estándar (stdout): {e.stdout}")
        print(f"Salida de error (stderr): {e.stderr}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        os.chdir(directorio_original)
        print(f"Vuelto al directorio original: {os.getcwd()}")

def exportar_datos_png():
    directorio_original = os.getcwd() 
    
    try:
        os.chdir(RUTA_EXTRACTOR)
        print(f"Cambiado al directorio: {os.getcwd()}")

        comando = [
            "rs-convert.exe",
            "-i",
            temp_rec_route,
            "-p",
            RUTA_PNG + "/PNG"
        ]
        
        print(f"Ejecutando comando: {' '.join(comando)}")

        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        
        print("\n--- Extracción finalizada ---")
        if resultado.stdout:
            print("Salida de rs-convert.exe:")
            print(resultado.stdout)
        if resultado.stderr:
            print("Errores (stderr) de rs-convert.exe:")
            print(resultado.stderr)

    except FileNotFoundError:
        print(f"Error: No se encontró 'rs-convert.exe' en '{RUTA_EXTRACTOR}'. Asegúrate de que la ruta es correcta.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar rs-convert.exe. Código de salida: {e.returncode}")
        print(f"Salida estándar (stdout): {e.stdout}")
        print(f"Salida de error (stderr): {e.stderr}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        os.chdir(directorio_original)
        print(f"Vuelto al directorio original: {os.getcwd()}")

def exportar_datos_csv():
    directorio_original = os.getcwd() 
    
    try:
        os.chdir(RUTA_EXTRACTOR)
        print(f"Cambiado al directorio: {os.getcwd()}")

        comando = [
            "rs-convert.exe",
            "-i",
            temp_rec_route,
            "-v",
            RUTA_CSV + "/CSV"
        ]
        
        print(f"Ejecutando comando: {' '.join(comando)}")

        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        
        print("\n--- Extracción finalizada ---")
        if resultado.stdout:
            print("Salida de rs-convert.exe:")
            print(resultado.stdout)
        if resultado.stderr:
            print("Errores (stderr) de rs-convert.exe:")
            print(resultado.stderr)

    except FileNotFoundError:
        print(f"Error: No se encontró 'rs-convert.exe' en '{RUTA_EXTRACTOR}'. Asegúrate de que la ruta es correcta.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar rs-convert.exe. Código de salida: {e.returncode}")
        print(f"Salida estándar (stdout): {e.stdout}")
        print(f"Salida de error (stderr): {e.stderr}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        # Siempre vuelve al directorio original para no afectar el resto del script
        os.chdir(directorio_original)
        print(f"Vuelto al directorio original: {os.getcwd()}")

def exportar_datos_bin():
    directorio_original = os.getcwd() 
    
    try:
        os.chdir(RUTA_EXTRACTOR)
        print(f"Cambiado al directorio: {os.getcwd()}")

        comando = [
            "rs-convert.exe",
            "-i",
            temp_rec_route,
            "-b",
            RUTA_BIN + "/BIN"
        ]
        
        print(f"Ejecutando comando: {' '.join(comando)}")
        
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        
        print("\n--- Extracción finalizada ---")
        if resultado.stdout:
            print("Salida de rs-convert.exe:")
            print(resultado.stdout)
        if resultado.stderr:
            print("Errores (stderr) de rs-convert.exe:")
            print(resultado.stderr)

    except FileNotFoundError:
        print(f"Error: No se encontró 'rs-convert.exe' en '{RUTA_EXTRACTOR}'. Asegúrate de que la ruta es correcta.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar rs-convert.exe. Código de salida: {e.returncode}")
        print(f"Salida estándar (stdout): {e.stdout}")
        print(f"Salida de error (stderr): {e.stderr}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        # Siempre vuelve al directorio original para no afectar el resto del script
        os.chdir(directorio_original)
        print(f"Vuelto al directorio original: {os.getcwd()}")
    
def exportar_datos():
    hilos = []
    hilos.append(threading.Thread(target=exportar_datos_bin))
    hilos.append(threading.Thread(target=exportar_datos_csv))
    hilos.append(threading.Thread(target=exportar_datos_ply))
    hilos.append(threading.Thread(target=exportar_datos_raw))
    hilos.append(threading.Thread(target=exportar_datos_png))

    for hilo in hilos:
        hilo.start()
        print(f"Hilo iniciado para exportar datos: {hilo.name}")

    for hilo in hilos:
        hilo.join()

    print("Datos exportados exitosamente")

def prueba():
    global temp_rec_route 
    global RUTA_BIN
    global RUTA_CSV
    global RUTA_PLY
    global RUTA_RAW
    global RUTA_PNG 

    temp_rec_route= RUTA + "1750998774.785851" + "/"

    try:
        if not os.path.exists(temp_rec_route):
            os.makedirs(temp_rec_route)
    
    except FileExistsError:
        print(f"La carpeta {temp_rec_route} ya existe")

    RUTA_PLY = temp_rec_route + "/PLY"
    RUTA_RAW = temp_rec_route + "/RAW"
    RUTA_PNG =  temp_rec_route + "/PNG"
    RUTA_CSV =  temp_rec_route + "/CSV"
    RUTA_BIN =  temp_rec_route + "/BIN"
    temp_rec_route = RUTA + "1750998774.785851" + ".bag"
    

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

    threading.Thread(target=exportar_datos).start()


prueba()