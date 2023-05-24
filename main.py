import numpy as np
import cv2
import matplotlib.pyplot as plt
from AICam import *

cam0 = CapCam()
cam1 = CapCam()


cam0.init_cam(id_cam=0, exp=-6)
cam1.init_cam(id_cam=1, exp=-7)
# cam0.init_video(r'C:\Users\Kamov\Downloads\WIN_20230330_camera 1.MP4')
# cam1.init_video(r'C:\Users\Kamov\Downloads\WIN_20230330_camera 2.MP4')
#
while True:
    cam0.get_frame()
    cv2.imshow('Cam0_m', cam0.main_func(inverse=False, qtile=0.2))
    cv2.imshow('cap0', cam0.green)
    #cv2.imshow('beam1', cam0.beam_mask)
    cam1.get_frame()
    cv2.imshow('Cam1_m', cam1.main_func(inverse=True, qtile=0.7))
    cv2.imshow('cap1', cam1.green)
#
    #cv2.imshow('beam0', cam1.beam_mask)
    # cv2.imshow('Cam2_m', cam1.main_func(beam_treshold=50, capillar_treshold=100, inverse=True)
#
#
    if len(cam0.shif_arr) > 5:
        plt.clf()
        plt.plot(cam0.shif_arr[-50:-1], label='cam0: %f ± %f' %(np.mean(cam0.shif_arr[-50:-1]) * cam0.k, np.std(cam0.shif_arr[-50:-1]) * cam0.k))
        plt.plot(cam1.shif_arr[-50:-1], label='cam1: %f ± %f' %(np.mean(cam1.shif_arr[-50:-1]) * cam1.k, np.std(cam0.shif_arr[-50:-1]) * cam1.k))
        plt.legend()
        plt.ylim([-20, 20])
        plt.grid()
        plt.pause(0.005)
#
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break