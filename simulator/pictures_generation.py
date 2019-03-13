import json
import os
import subprocess

import cv2
import matplotlib.pyplot as plt
import numpy as np

from definitions import CONFIG_PATH, GROUND_PATH, PHOTOS_PATH, ROOT_DIR
from simulator.image_creation import compute_command_arc, \
    draw_central_dashed_arc_on_ground, draw_lateral_complete_arcs_on_ground
from simulator.utils import Point

DEFAULT_CONFIGURATION = json.load(open(CONFIG_PATH))

# Configuration
origin_pool = np.arange(DEFAULT_CONFIGURATION['origin_pool_start'],
                        DEFAULT_CONFIGURATION['origin_pool_end'],
                        DEFAULT_CONFIGURATION['origin_pool_step'])
origin_pool = [(x, DEFAULT_CONFIGURATION['image_height']) for x in origin_pool]

end_pool_top = np.arange(DEFAULT_CONFIGURATION['end_pool_top_start'],
                         DEFAULT_CONFIGURATION['end_pool_top_end'],
                         DEFAULT_CONFIGURATION['end_pool_top_step'])
end_pool_top = [(x, 0) for x in end_pool_top]

end_pool_right = range(DEFAULT_CONFIGURATION['end_pool_right_start'],
                       DEFAULT_CONFIGURATION['end_pool_right_end'],
                       DEFAULT_CONFIGURATION['end_pool_right_step'])
end_pool_right = [(DEFAULT_CONFIGURATION['image_width'], x) for x in end_pool_right]

end_pool = end_pool_top + end_pool_right

radius_pool = range(DEFAULT_CONFIGURATION['radius_pool_start'],
                    DEFAULT_CONFIGURATION['radius_pool_end'],
                    DEFAULT_CONFIGURATION['radius_pool_step'])


# Handling ground images
ground_images = [x for x in os.listdir(GROUND_PATH) if 'JPG' in x]
grounds = [cv2.imread(GROUND_PATH + '/' + img) for img in ground_images]
grounds = [cv2.resize(x, (DEFAULT_CONFIGURATION['image_width'],
                          DEFAULT_CONFIGURATION['image_height'])) for x in grounds]


def right_direction(configuration, execution_dir_path=PHOTOS_PATH, output_dir=PHOTOS_PATH):
    i = 0
    while True:
        origin_pt = origin_pool[np.random.choice(len(origin_pool))]
        end_pt = end_pool[np.random.choice(len(end_pool))]
        radius = radius_pool[np.random.choice(len(radius_pool))]
        origin = Point(origin_pt[0], origin_pt[1])
        end = Point(end_pt[0], end_pt[1])
        cmd = int(compute_command_arc(origin, end, radius))
        if int(cmd) <= 36:
            povray_file_path = os.path.join(ROOT_DIR, 'simulator', 'povray_test_cob.pov')
            img = grounds[np.random.choice(range(len(ground_images)))]
            img_drawn = draw_central_dashed_arc_on_ground(img, origin, end, radius, (148, 252, 9))
            img_complete = draw_lateral_complete_arcs_on_ground(img_drawn, origin, end, radius, (255, 255, 255))
            img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
            img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete
            plt.imsave(execution_dir_path + 'test.jpg', img_final)
            command = 'povray -I{} Height=176 Width=240 Output_File_Name={}/{}_cmd_{}'.format(
                    povray_file_path,
                    output_dir,
                    int(cmd),
                    i)
            subprocess.run(command, shell=True, cwd=execution_dir_path)

            # Mirroring the image
            img_complete = cv2.flip(img_complete, 1)
            img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
            img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete
            plt.imsave('test.jpg', img_final)
            plt.imsave(execution_dir_path + 'test.jpg', img_final)
            command = 'povray -I{} Height=176 Width=240 Output_File_Name={}/{}_cmd_{}'.format(
                    povray_file_path,
                    output_dir,
                    180 - int(cmd),
                    i)
            subprocess.run(command, shell=True, cwd=execution_dir_path)
            i += 1
            if i == configuration['images_curve']:
                break



