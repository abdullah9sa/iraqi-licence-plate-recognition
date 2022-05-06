import os
import cv2
from base_camera import BaseCamera
import detect_plate
import numpy as np
from flask import json

class Camera(BaseCamera):
    video_source = ""#http://192.168.137.200:8080/video"#ip#"http://192.168.137.151:8080/video"#0

    ret = False
    def __init__(self,ip):

        self.set_video_source(str(ip))

        # if os.environ.get('OPENCV_CAMERA_SOURCE'):
        #     Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))

        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        if(source == "0"):
            Camera.video_source = 0
        else:
            Camera.video_source = str(source)
            

    @staticmethod
    def retry():
        print("being clakledel ++++++++++++++++++++++++++")
        Camera.ret = True
    


    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        counter = 0
        while True:
            # read current frame
            _, img = camera.read()
            
            if(Camera.ret):
                camera.release()
                return
            if(counter > 15):
                result,data = detect_plate.Detect_Plate_video(img , True)
                json_object = json.dumps(data,ensure_ascii = True)
                with open("./sample.json", "w") as outfile:
                    outfile.write(json_object)
                counter = 0
                yield cv2.imencode('.jpg', result)[1].tobytes()


            # image_array = np. array(result)
            counter = counter + 1
            yield cv2.imencode('.jpg', img)[1].tobytes()
