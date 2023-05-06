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
from decode import decode, add_bb_frmcamsph

def videofromtrack(set, outname = 'video_out', FPS = 25, add_bboxes = False):

    with open(set, 'r') as input_file:
        track_dict = json.load(input_file)

    num_steps = int(list(track_dict.keys())[-1])+1
    video = cv2.VideoWriter(output_dir + outname + '.avi', cv2.VideoWriter_fourcc(*'MP42'),
                        float(FPS), (480, 480))
    
    for frame in range(num_steps):
        print("Process step:", frame+1, "of", num_steps)
        if track_dict[str(frame)]['img_data'] is not None:
            img_dict = track_dict[str(frame)]['img_data']
            output_img = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])

            if add_bboxes:
                add_bb_frmcamsph(output_img, img_dict['ball_locate'])

            video.write(output_img[:,:,::-1])

    video.release()

if __name__ == "__main__":

    add_bboxes = True

    output_dir = "videos"
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

    for kick_no, set in enumerate(data_list):
        print("Start kick", kick_no+1, "of", len(data_list))
        videofromtrack(set, outname = '/video_' + str(kick_no), add_bboxes = add_bboxes)

    print("Complete")