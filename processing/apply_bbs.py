#!/usr/bin/env python3
"""Decode tracking data to video"""

import json
import sys
import os
import glob
from PIL import Image
import numpy as np
import cv2

sys.path.append(os.path.join(sys.path[0], '../../msc_visualdata_wrangling/processing/'))
from decode import add_bb_frmcamsph

if __name__ == "__main__":

    FPS = 25

    output_dir = "bb_videos"
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

    for count, set in enumerate(data_list):
        print("Process kick", count+1, "of", len(data_list))
        prefix = set[-25:-9]
        cap = cv2.VideoCapture(prefix+'video.avi')
        video = cv2.VideoWriter(output_dir + '/' + prefix + 'bb.avi', cv2.VideoWriter_fourcc(*'MP42'),
                                float(FPS), (480, 480))

        with open(set, 'r') as input_file:
            track_dict = json.load(input_file)

        for count, step_dict in enumerate(track_dict.values()):
            #print('Process step', count+1, 'of', len(track_dict.values()))
            if step_dict['frame_no'] is not None:
                _, frame = cap.read()
                add_bb_frmcamsph(frame, step_dict['gt_ball_spherical'], color=(0,0,255))
                video.write(frame)

        cap.release()
        video.release()

    print("Complete")