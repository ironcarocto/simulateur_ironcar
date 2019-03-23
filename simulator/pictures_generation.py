import json
import os
import subprocess

import cv2
import matplotlib.pyplot as plt
import numpy as np

from simulator.image_creation import ImageCreation
from simulator.utils import Point
import os

cwd = os.getcwd()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'profil_generation_template/configuration.json')
GROUND_PATH = os.path.join(ROOT_DIR, 'profil_generation_template/grounds/')
PHOTOS_PATH = os.path.join(cwd + '/photos')
DEFAULT_CONFIGURATION = json.load(open(CONFIG_PATH))
IMAGE_CREATION = ImageCreation(configuration = DEFAULT_CONFIGURATION)

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


def grounds(path=GROUND_PATH):
    ground_images = [x for x in os.listdir(GROUND_PATH) if 'jpg' in x]
    ground_list = [cv2.imread(GROUND_PATH + '/' + img) for img in ground_images]
    ground_list = [cv2.resize(x, (DEFAULT_CONFIGURATION['image_width'],
                                  DEFAULT_CONFIGURATION['image_height'])) for x in ground_list]
    return ground_list


def right_direction(configuration,
                    ground_path=GROUND_PATH,
                    execution_dir_path=PHOTOS_PATH,
                    output_dir=PHOTOS_PATH):
    i = 0
    ground_list = grounds(ground_path)
    while True:
        origin_pt = origin_pool[np.random.choice(len(origin_pool))]
        end_pt = end_pool[np.random.choice(len(end_pool))]
        radius = radius_pool[np.random.choice(len(radius_pool))]
        origin = Point(origin_pt[0], origin_pt[1])
        end = Point(end_pt[0], end_pt[1])
        cmd = int(IMAGE_CREATION.compute_command_arc(origin, end, radius))
        if int(cmd) <= 36:
            povray_file_path = os.path.join(ROOT_DIR, 'povray_test_cob.pov')
            img = ground_list[np.random.choice(range(len(ground_list)))]
            img_drawn = IMAGE_CREATION.draw_central_dashed_arc_on_ground(img, origin, end, radius, (148, 252, 9))
            img_complete = IMAGE_CREATION.draw_lateral_complete_arcs_on_ground(img_drawn, origin, end, radius, (255, 255, 255))
            img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
            img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete
            plt.imsave(execution_dir_path + '/test.jpg', img_final)
            command = 'povray -D -I{} Height=176 Width=240 Output_File_Name={}/{}_cmd_{}'.format(
                povray_file_path,
                output_dir,
                int(cmd),
                i)
            subprocess.run(command, shell=True, cwd=execution_dir_path)

            # Mirroring the image
            img_complete = cv2.flip(img_complete, 1)
            img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
            img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete
            plt.imsave(execution_dir_path + '/test.jpg', img_final)
            command = 'povray -D -I{} Height=176 Width=240 Output_File_Name={}/{}_cmd_{}'.format(
                povray_file_path,
                output_dir,
                180 - int(cmd),
                i)
            subprocess.run(command, shell=True, cwd=execution_dir_path)
            i += 1
            if i == configuration['images_curve']:
                break
