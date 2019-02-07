import json
import os
import re
import subprocess
import uuid

import cv2
import jinja2
import matplotlib.pyplot as plt
import numpy as np

from definitions import CONFIG_PATH, GROUND_PATH, PHOTOS_PATH
from simulator.image_creation import compute_command_arc, \
    draw_central_dashed_arc_on_ground, draw_lateral_complete_arcs_on_ground
from simulator.utils import Point

configuration = json.load(open(CONFIG_PATH))

# Handling ground images
ground_images = [x for x in os.listdir(GROUND_PATH) if 'JPG' in x]
grounds = [cv2.imread(GROUND_PATH + '/' + img) for img in ground_images]
grounds = [cv2.resize(x, (configuration['image_width'],
                          configuration['image_height'])) for x in grounds]


def points_selection(configuration):
    # Configuration to generate random points
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

    # Point selection
    origin_pt = origin_pool[np.random.choice(len(origin_pool))]
    end_pt = end_pool[np.random.choice(len(end_pool))]
    radius = radius_pool[np.random.choice(len(radius_pool))]

    return Point(origin_pt[0], origin_pt[1]), Point(end_pt[0], end_pt[1]), radius


def straight(configuration):
    i = 0
    while True:
        origin, end, radius = points_selection(configuration)
        angle = int(compute_command_arc(origin, end, radius))

        if 72 < angle and angle >= 108:
            img = grounds[np.random.choice(range(3))]
            img_drawn = draw_central_dashed_arc_on_ground(img, origin, end, radius, (148, 252, 9))
            img_complete = draw_lateral_complete_arcs_on_ground(img_drawn, origin, end, radius, (255, 255, 255))
            img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
            img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete
            file_name = uuid.uuid4().hex
            plt.imsave(PHOTOS_PATH + file_name + '.jpg', img_final)
            img = povraytize(file_name)[80:]
            plt.imsave(PHOTOS_PATH + '{}_angle_{}'.format(angle, i), img)

            # # Mirroring the image
            # img_complete = cv2.flip(img_complete, 1)
            # img_final = 255 * np.ones((3 * img.shape[0], 4 * img.shape[1], 3), dtype='uint8')
            # img_final[2 * img.shape[0]:, img.shape[1]:2 * img.shape[1], :] = img_complete[80:]
            # file_name = uuid.uuid4().hex
            # plt.imsave(PHOTOS_PATH + file_name + '.jpg', img_final)
            # img = povraytize(file_name, i)[80:]
            # plt.imsave(PHOTOS_PATH + '{}_cmd_{}'.format(180 - angle, i))
            # i += 1
            if i >= int(configuration['images_curve'] / 2):
                break


def povraytize(file_name, height=176, width=240):
    templateLoader = jinja2.FileSystemLoader(searchpath=PHOTOS_PATH)
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "template.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(image_name=file_name + '.jpg')
    print(outputText)
    with open(PHOTOS_PATH + file_name + '.pov.j2', "w") as out:
        out.write(outputText)

    command = ['povray', '-I' + file_name + '.pov.j2', 'Height=' + str(height), 'Width=' + str(width), 'Output_File_Type=P',
               '-O-']
    print(command)

    process = subprocess.Popen(command, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, cwd=PHOTOS_PATH)

    os.remove(PHOTOS_PATH+file_name + '.pov.j2')
    os.remove(PHOTOS_PATH + file_name + '.jpg')

    out, err = process.communicate()
    print(out)
    #image_to_return = ppm_to_numpy(buffer=out)
    #return image_to_return


def ppm_to_numpy(filename=None, buffer=None, byteorder='>', numpy_found=True):
    """Return image data from a raw PGM/PPM file as numpy array.
    Format specification: http://netpbm.sourceforge.net/doc/pgm.html
    """

    if not numpy_found:
        raise IOError("Function ppm_to_numpy requires numpy installed.")

    if buffer is None:
        with open(filename, 'rb') as f:
            buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P\d\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PPM/PGM file: '%s'" % filename)

    cols_per_pixels = 1 if header.startswith(b"P5") else 3

    dtype = 'uint8' if int(maxval) < 256 else byteorder + 'uint16'
    arr = np.frombuffer(buffer, dtype=dtype,
                        count=int(width) * int(height) * 3,
                        offset=len(header))

    return arr.reshape((int(height), int(width), 3))
