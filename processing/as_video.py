#!/usr/bin/env python3
"""Decode base64 encoded images"""

from base64 import decodebytes
import json
import sys
import os
import glob
from PIL import Image
import numpy as np
import cv2

sys.path.append(os.path.join(sys.path[0], '../../msc_visualdata_wrangling/processing/'))
from decode import decode #, spherical2cartesiantransform_camsph2bb, transform_cambb2sph, add_bb_frmcamsph

if __name__ == "__main__":

    output_dir = "video_out"
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass

    data_list = []
    if len(sys.argv)==1:  # No added arguments
        album = True
    else:
        album = False

    if not album:
        data_list.append(sys.argv[1])

    elif album:
        data_list = glob.glob(os.path.join('./', "*.json"))

    FPS = 25 # Capture rate
    for set in data_list:    

        with open(set, 'r') as input_file:
            track_dict = json.load(input_file)

        num_steps = int(list(track_dict.keys())[-1])+1
        video = cv2.VideoWriter(output_dir +'/video_out.avi', cv2.VideoWriter_fourcc(*'MP42'),
                            float(FPS), (480, 480))
        
        for frame in range(num_steps):
            print("Process step: " + str(frame+1), "of", num_steps)
            if track_dict[str(frame)]['img_data'] is not None:
                img_dict = track_dict[str(frame)]['img_data']
                output_img = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])
                video.write(output_img[:,:,::-1])

        video.release()
        print("Complete")