import json
import logging
import shutil
import subprocess
import tempfile

import cv2
import matplotlib.pyplot as plt
import numpy as np
from decorator import contextmanager

from simulator.image_creation import ImageCreation
from simulator.utils import Point
import os

cwd = os.getcwd()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(cwd, 'configuration.json')
if not os.path.isfile(CONFIG_PATH): # pour garder la compatibilité avec les notebooks
    CONFIG_PATH = os.path.join(ROOT_DIR, 'profil_generation_template', 'configuration.json')

GROUND_PATH = os.path.join(cwd, 'grounds')
PHOTOS_PATH = os.path.join(cwd, 'photos')

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


mirror_pool = [False, True]

CADRAN = {
    0: [0, 36],
    1: [36,72],
    2: [72, 108],
    3: [108, 144],
    4: [144, 180]
}

# Handling ground images


def grounds(path):
    ground_images = [x for x in os.listdir(path) if 'jpg' in x]
    ground_list = [cv2.imread(path + '/' + img) for img in ground_images]
    ground_list = [cv2.resize(x, (DEFAULT_CONFIGURATION['image_width'],
                                  DEFAULT_CONFIGURATION['image_height'])) for x in ground_list]
    return ground_list

def generate_profile_for_cadran(configuration,
                                ground_path=GROUND_PATH,
                                photos_path=PHOTOS_PATH,
                                cadran_id=0):
    logger = logging.getLogger('simulateur_ironcar')

    with tmp_working_directory_directory() as tmp:

        i = 0
        ground_list = grounds(ground_path)
        cadran_start = CADRAN[cadran_id][0]
        cadran_end = CADRAN[cadran_id][1]
        while True:
            origin_pt = origin_pool[np.random.choice(len(origin_pool))]
            end_pt = end_pool[np.random.choice(len(end_pool))]
            radius = radius_pool[np.random.choice(len(radius_pool))]
            origin = Point(origin_pt[0], origin_pt[1])
            end = Point(end_pt[0], end_pt[1])
            mirror = mirror_pool[np.random.choice(len(mirror_pool))]

            logger.debug({'operation': 'generate_profile_for_cadran.inputs',
                          'origin': origin_pt,
                          'end': end_pt,
                          'radius': radius,
                          'road_orientation': mirror})

            try:
                angle = int(IMAGE_CREATION.compute_command_arc(origin, end, radius))
                if mirror:
                    angle = 180 - int(angle)
            except ValueError:
                logger.warning({'message': 'fail to compute compute_command_arc',
                                'operation': 'generate_profile_for_cadran.inputs',
                                'origin': origin_pt,
                                'end': end_pt,
                                'radius': radius,
                                'mirror': mirror})
                continue

            logger.debug({'operation': 'generate_profile_for_cadran.angle',
                          'angle': angle,
                          'cadran_ok': cadran_start <= angle < cadran_end})
            if cadran_start <= angle < cadran_end:
                povray_file_path = os.path.join(ROOT_DIR, 'povray.pov')
                img = ground_list[np.random.choice(range(len(ground_list)))]
                img_drawn = IMAGE_CREATION.draw_central_dashed_arc_on_ground(img, origin, end, radius, (148, 252, 9))
                img_complete = IMAGE_CREATION.draw_lateral_complete_arcs_on_ground(img_drawn, origin, end, radius,
                                                                                   (255, 255, 255))
                img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
                img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete

                if mirror:
                    img_complete = cv2.flip(img_complete, 1)
                    img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
                    img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete

                plt.imsave(tmp + '/test.jpg', img_final)

                dataset_id = configuration["dataset_id"]
                filename = 'cadran={}_angle={}_id={}_did={}'.format(cadran_id, angle, i, dataset_id)
                command = 'povray -D -I{} Height=176 Width=240 Output_File_Name={}/{}'.format(
                    povray_file_path,
                    photos_path,
                    filename)

                logger.debug({'operation': 'generate_profile_for_cadran.raytracing', 'command': command})
                subprocess.run(command, shell=True, cwd=tmp)

                i += 1
                if i == configuration['images_curve']:
                    break

@contextmanager
def tmp_working_directory_directory():
    working_directory = tempfile.mkdtemp(prefix='simulateur_ironcar_')
    previous_wd = os.getcwd()

    os.chdir(working_directory)
    yield working_directory
    shutil.rmtree(working_directory)
    os.chdir(previous_wd)
