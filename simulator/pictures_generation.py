import json
import os
import subprocess

import cv2
import matplotlib.pyplot as plt
import numpy as np

from definitions import CONFIG_PATH, GROUND_PATH, PHOTOS_PATH
from simulator.image_creation import compute_command_arc, \
    draw_central_dashed_arc_on_ground, draw_lateral_complete_arcs_on_ground
from simulator.utils import Point

configuration = json.load(open(CONFIG_PATH))

# Configuration
origin_pool = np.arange(configuration['origin_pool_start'],
                        configuration['origin_pool_end'],
                        configuration['origin_pool_step'])
origin_pool = [(x, configuration['image_height']) for x in origin_pool]

end_pool_top = np.arange(configuration['end_pool_top_start'],
                         configuration['end_pool_top_end'],
                         configuration['end_pool_top_step'])
end_pool_top = [(x, 0) for x in end_pool_top]

end_pool_right = range(configuration['end_pool_right_start'],
                       configuration['end_pool_right_end'],
                       configuration['end_pool_right_step'])
end_pool_right = [(configuration['image_width'], x) for x in end_pool_right]

end_pool = end_pool_top + end_pool_right

radius_pool = range(configuration['radius_pool_start'],
                    configuration['radius_pool_end'],
                    configuration['radius_pool_step'])


# Handling ground images
ground_images = [x for x in os.listdir(GROUND_PATH) if 'JPG' in x]
grounds = [cv2.imread(GROUND_PATH + '/' + img) for img in ground_images]
grounds = [cv2.resize(x, (configuration['image_width'],
                          configuration['image_height'])) for x in grounds]


def right_direction(configuration):
    i = 0
    while True:
        origin_pt = origin_pool[np.random.choice(len(origin_pool))]
        end_pt = end_pool[np.random.choice(len(end_pool))]
        radius = radius_pool[np.random.choice(len(radius_pool))]
        origin = Point(origin_pt[0], origin_pt[1])
        end = Point(end_pt[0], end_pt[1])
        cmd = int(compute_command_arc(origin, end, radius))
        if int(cmd) <= 36:
            img = grounds[np.random.choice(range(3))]
            img_drawn = draw_central_dashed_arc_on_ground(img, origin, end, radius, (148, 252, 9))
            img_complete = draw_lateral_complete_arcs_on_ground(img_drawn, origin, end, radius, (255, 255, 255))
            img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
            img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete
            plt.imsave(PHOTOS_PATH + 'test.jpg', img_final)
            command = 'povray -Ipovray_test_cob.pov.j2 Height=176 Width=240 Output_File_Name={}_cmd_{}'.format(
                    int(cmd),
                    i)
            subprocess.run(command, shell=True, cwd=PHOTOS_PATH)

            # Mirroring the image
            img_complete = cv2.flip(img_complete, 1)
            img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
            img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete
            plt.imsave('test.jpg', img_final)
            plt.imsave(PHOTOS_PATH + 'test.jpg', img_final)
            command = 'povray -Ipovray_test_cob.pov.j2 Height=176 Width=240 Output_File_Name={}_cmd_{}'.format(
                    180 - int(cmd),
                    i)
            subprocess.run(command, shell=True, cwd=PHOTOS_PATH)
            i += 1
            if i == configuration['images_curve']:
                break



