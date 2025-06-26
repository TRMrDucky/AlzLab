import pyrealsense2 as rs
import numpy as np
import cv2

pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)


def video_callback(option, cfg):
    
    
    if (option == 1):
        pipe.start(cfg)

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

    if (option == 2):
        pipe.start(cfg)

        while True:

            frames = pipe.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_frame_data = np.asanyarray(color_frame.get_data())

            cv2.imshow('Color Frame', color_frame_data)

            if cv2.waitKey(1) == ord('q'):
                break

        pipe.stop()

    if (option == 3):
        pipe.start(cfg)

        while True:

            frames = pipe.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            depth_frame_data = np.asanyarray(depth_frame.get_data())
            depth_color_map = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame_data, 
                                                                    alpha=0.5), cv2.COLORMAP_JET)
            
            cv2.imshow('Depth Frame', depth_color_map)

            if cv2.waitKey(1) == ord('q'):
                break

        pipe.stop()

    

    

video_callback(1, config)