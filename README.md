La última versión del script, que incluye vista previa, grabado y exportado se encuentra dentro de la carpeta pruebas_streams/grabacion_y_exportacion.

Es necesario tener instalado el SDK2.0, que se encuentra en esta misma ubicación bajo el nombre: Intel.RealSense.SDK-WIN10-2.55.1.6486.exe
Esto para que el exportado funcione de manera correcta, debido a que se utilizan scripts contenidos en "C:\Program Files (x86)\Intel RealSense SDK 2.0\tools" en una instalación normal.

Es necesario tener instalado python, la biblioteca pyrealsense2, panda y la librería de OpenCV:

pip install panda 
pip install numpy
pip install pyrealsense2 
pip install opencv-python

Si todo sale bien, solo queda conectar la cámara y correr el script.
La primer ventana que nos abre es la vista previa, al presionar "s" se comenzaría la grabación, o "q" para finalizar el programa. Lo mismo para cuando
se está grabando el video.

Por defecto, la vista previa y la grabación tienen la siguiente configuración:
- Video en profundidad y color. En pantalla solo se muestra el video a color.
- Resolución de 640 x 480
- Video a 30 FPS
