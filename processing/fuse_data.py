#!/usr/bin/env python3
"""Fuse raw tracking data into a single file"""

import json
import sys
import os
import glob
from PIL import Image
from natsort import natsorted
import uuid
import numpy as np
    
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

    kick_curr = -1
    count_kick = 0
    for count, name in enumerate(step_list):
        print(count+1, "/", len(step_list), "Timesteps processed")
        fuse_step_dict = {}

        with open(name, 'r') as input_file:
            step_dict = json.load(input_file)
        
        # Check new kick
        if step_dict['kick_no']==kick_curr and (count+1)<len(step_list):
            count_kick = count_kick + 1
            pass
        elif kick_curr == -1:
            kick_curr = step_dict['kick_no']
        else:
            prefix = unique[:6-len(str(kick_curr))] + str(kick_curr)
            with open("./" + output_dir + "/" + prefix + "_tracking_data.json", 'w') as out_file:
                json.dump(data_dict, out_file, indent=4)

            kick_curr = step_dict['kick_no']
            count_kick = 0
            data_dict = {}

        # Check image data
        cycle_no = name[12:-5]
        if cycle_no in img_steps:
            with open(img_list[0][:18]+str(cycle_no)+'.json', 'r') as input_file:
                img_dict = json.load(input_file) 
        else:
            img_dict = None

        full_mat = np.array(step_dict['mat_l2g'])@np.array(step_dict['mat_cam2local'])

        fuse_step_dict['time'] = step_dict['time']
        fuse_step_dict['transform'] = full_mat.tolist()
        fuse_step_dict['see_ball_global'] = step_dict['see_ball_global']
        fuse_step_dict['gt_ball_global'] = step_dict['gt_ball_global']
        fuse_step_dict['img_data'] = img_dict

        data_dict[count_kick] = fuse_step_dict

    print("Processed", kick_curr+1, "kicks")
