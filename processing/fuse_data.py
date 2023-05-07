#!/usr/bin/env python3
"""Fuse raw tracking data into a single file and a video"""

import json
import sys
import os
import glob
from PIL import Image
from natsort import natsorted
import uuid
import numpy as np
import cv2

sys.path.append(os.path.join(sys.path[0], '../../msc_visualdata_wrangling/processing/'))
from decode import decode
    
if __name__ == "__main__":

    output_dir = "fuse"
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass

    path = "./"
    img_list = natsorted(glob.glob('./outimg*' + '*.json'))
    img_steps = [file_[18:-5] for file_ in img_list]
    step_list = natsorted(glob.glob('./trackkick*' + '*.json'))
    unique = str(uuid.uuid4().fields[-1])
    data_dict = {}
    FPS = 25

    kick_curr = -1
    count_kick = 0
    for count, name in enumerate(step_list):
        print(count+1, "/", len(step_list), "Timesteps processed")
        fuse_step_dict = {}

        with open(name, 'r') as input_file:
            step_dict = json.load(input_file)
        
        if step_dict['kick_no']==kick_curr:# and (count+1)<len(step_list):
            count_kick = count_kick + 1
        elif kick_curr == -1:
            kick_curr = step_dict['kick_no']
            frame_no = -1
            prefix = unique[:6-len(str(kick_curr))] + str(kick_curr)
            video = cv2.VideoWriter(path + output_dir + "/" + prefix + "_tracking_video.avi", cv2.VideoWriter_fourcc(*'MP42'),
                                    float(FPS), (480, 480))
        else:
            video.release()
            prefix = unique[:6-len(str(kick_curr))] + str(kick_curr)
            with open("./" + output_dir + "/" + prefix + "_tracking_data.json", 'w') as out_file:
                json.dump(data_dict, out_file, indent=4)

            count_kick = 0
            frame_no = -1
            data_dict = {}
            kick_curr = step_dict['kick_no']
            prefix = unique[:6-len(str(kick_curr))] + str(kick_curr)
            video = cv2.VideoWriter(path + output_dir + "/" + prefix + "_tracking_video.avi", cv2.VideoWriter_fourcc(*'MP42'),
                                    float(FPS), (480, 480))

        fuse_step_dict['time'] = step_dict['time']

        cycle_no = name[12:-5]
        if cycle_no in img_steps:
            with open(img_list[0][:18]+str(cycle_no)+'.json', 'r') as input_file:
                img_dict = json.load(input_file) 
                frame = decode(img_dict['img'], img_dict['h_img'], img_dict['w_img'])
                video.write(frame[:,:,::-1])
                frame_no = frame_no + 1
                fuse_step_dict['frame_no'] = frame_no
                fuse_step_dict['gt_ball_spherical'] = img_dict['ball_locate']
        else:
            fuse_step_dict['frame_no'] = None
            fuse_step_dict['gt_ball_spherical'] = None

        full_mat = np.array(step_dict['mat_l2g'])@np.array(step_dict['mat_cam2local'])
        fuse_step_dict['transform'] = full_mat.tolist()

        fuse_step_dict['see_ball_global'] = step_dict['see_ball_global']
        fuse_step_dict['gt_ball_global'] = step_dict['gt_ball_global']

        data_dict[count_kick] = fuse_step_dict
    
    prefix = unique[:6-len(str(kick_curr))] + str(kick_curr)
    with open("./" + output_dir + "/" + prefix + "_tracking_data.json", 'w') as out_file:
        json.dump(data_dict, out_file, indent=4)
    video.release()

    print("Processed", kick_curr+1, "kicks")
