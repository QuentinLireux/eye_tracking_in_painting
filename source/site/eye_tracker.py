import argparse
import pathlib
import numpy as np
import cv2
import time

import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import transforms
import torch.backends.cudnn as cudnn
import torchvision

from PIL import Image
from PIL import Image, ImageOps

from face_detection import RetinaFace

from l2cs import select_device, draw_gaze, getArch, render,find_border_points,Pipeline


CWD = pathlib.Path.cwd()

class Eye_tracker:

    cam = cv2.VideoCapture(0)

    width, height = 0,0

    points = [[], [], [], []]

    border_points = []

    frame = None
    
    gaze_pipeline = Pipeline(
        weights=CWD / 'models' / 'L2CSNet_gaze360.pkl',
        arch='ResNet50',
        device = select_device('0', batch_size=1)
    )
    
    run = False
    
    transform_eye_calib = (0, 0)
    
    def __init__(self):
        
        if self.is_model_loaded(self.gaze_pipeline):
            print("Le modèle a été chargé avec succès.")
        else:
            print("Erreur lors du chargement du modèle.")


    def is_model_loaded(self,pipe):
        return hasattr(pipe, 'model') and pipe.model is not None

    def initialisation(self,width,height):
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

        self.width,self.height = width,height
        
        if not self.cam.isOpened():
            raise IOError("Cannot open webcam")


    def boucle(self):        
        with torch.no_grad():
            self.border_points = find_border_points(self.points,method="avg")

            try:
                with open('coor.txt', 'w') as fichier:
                    fichier.write(f"{0},{0}\n")
            except Exception as e:
                print(f"Erreur : {e}")
            while self.run:
                try:
                    success, self.frame = self.cam.read()

                    self.frame = cv2.flip(self.frame, 1)
                    
                    results = self.gaze_pipeline.step(self.frame)
                    self.frame, _,_ = render(self.frame, results, self.width, self.height, self.border_points, False, self)
                except Exception as e:
                    print (e)
                    break
                
                success,self.frame = self.cam.read()
    
    def set_transform_eye_calib(self,point):
        self.transform_eye_calib = point
        self.write_coor(self.transform_eye_calib)

    def write_coor(self,point):
        try:
            with open('coor.txt', 'a') as fichier:
                fichier.write(f"{point[0]},{point[1]}\n")
        except Exception as e:
            print(f"Erreur : {e}")

    def add_callibration(self, i):

        calibration_step_time = 8
        instruction_time = 12

        start_time = time.time()
        while time.time() - start_time < (instruction_time + calibration_step_time):
            success, self.frame = self.cam.read()
            if not success:
                print("Failed to obtain frame")
                time.sleep(0.1)
                continue 

            self.frame = cv2.flip(self.frame, 1)
            results = self.gaze_pipeline.step(self.frame)
            _,dx,dy = render(self.frame, results, self.width, self.height, [], True,self)
            self.points[i].append([dx, dy])
        
        return True