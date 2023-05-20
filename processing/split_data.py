#!/usr/bin/env python3
"""Split json data into train, validation, test datasets"""

import json
import os
import glob
import numpy as np
import shutil

output_dir1 = "train"
try:
    os.makedirs(output_dir1)
except FileExistsError:
    pass

output_dir2 = "validation"
try:
    os.makedirs(output_dir2)
except FileExistsError:
    pass

output_dir3 = "test"
try:
    os.makedirs(output_dir3)
except FileExistsError:
    pass

kick_list = glob.glob(os.path.join('./',"*.json"))
sort_order = np.arange(len(kick_list))
np.random.shuffle(sort_order)

train_split = 0.6
valid_split = 0.2
test_split = 1-train_split-valid_split

train_idx = int(train_split*len(kick_list))
test_idx = int(test_split*len(kick_list))

for count, name in enumerate(kick_list):
    print(count+1, "/", len(kick_list), "Kicks processed")

    with open(name, 'r') as input_file:
        img_dict = json.load(input_file)
    
    if count in sort_order[:train_idx]:
        with open("./" + output_dir1 + "/" + name[2:], 'w') as out_file:
            json.dump(img_dict, out_file)
        shutil.copy2(name[:-9]+'video.avi', "./" + output_dir1 + name[1:-9]+'video.avi')

    elif count in sort_order[-(test_idx+1):]:
        with open("./" + output_dir3 + "/" + name[2:], 'w') as out_file:
            json.dump(img_dict, out_file)
        shutil.copy2(name[:-9]+'video.avi', "./" + output_dir3 + name[1:-9]+'video.avi')

    else:
        with open("./" + output_dir2 + "/" + name[2:], 'w') as out_file:
            json.dump(img_dict, out_file)
        shutil.copy2(name[:-9]+'video.avi', "./" + output_dir2 + name[1:-9]+'video.avi')