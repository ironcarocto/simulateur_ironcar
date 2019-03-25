import logging

import cv2
import numpy as np


from simulator.utils import angle_clockwise, Point


class ImageCreation:

    def __init__(self, configuration : dict):
        self.configuration = configuration
        self.logger = logging.getLogger('simulateur_ironcar')

    def center_coordinates(self, start_point, end_point, radius):
        """
        Computes the coordinates for the center point associated with 2 points and a radius
        :param start_point: np.array with two values (vector)
        :param end_point: np.array with two values (vector)
        :param radius: real positive value
        :return: center coordinates: np.array with two values (vector)
        """
        vector = end_point - start_point
        normal_vector = Point(-vector.y, vector.x)
        normal_unitary_vector = normal_vector / normal_vector.norm()
        middle = (start_point + end_point) / 2
        center = middle + normal_unitary_vector * (np.sqrt(radius ** 2 - (vector.norm() / 2) ** 2))

        center.x = int(round(center.x))
        center.y = int(round(center.y))
        return center


    def draw_central_dashed_arc_on_ground(self, img, start_point, end_point, radius, color):
        """
        Plot central dashed arc (curved line). See configuration file for line specifications
        :param img: numpy.ndarray, image opened with OpenCV
        :param start_point: Point
        :param end_point: Point
        :param radius: int
        :param color: RGB numpy.array (3 colors between 0 & 255)
        :return: numpy.ndarray drawn image
        """
        configuration = self.configuration
        img_drawn = img.copy()
        center = self.center_coordinates(start_point, end_point, radius)

        alpha = round(180 * (configuration['dash_length_cm'] / configuration['conversion_pixel_to_cm']) / (np.pi * radius))
        start_angles = np.arange(0, 360, alpha)
        end_angles = np.arange(alpha, 361, alpha)

        for i, couple in enumerate(zip(start_angles, end_angles)):
            if i % 2 == 0:
                cv2.ellipse(img_drawn, (center.x, center.y), (radius, radius), 0, couple[0], couple[1], color,
                            thickness=int(configuration['line_width_cm'] / configuration['conversion_pixel_to_cm']))
        return img_drawn


    def draw_lateral_complete_arcs_on_ground(self, img, start_point, end_point, radius, color):
        """
        Plot lateral complete arcs (curved lines). See configuration file for line specifications
        :param img: numpy.ndarray, image opened with OpenCV
        :param start_point: Point
        :param end_point: Point
        :param radius: int
        :param color: RGB numpy.array (3 colors between 0 & 255)
        :return: numpy.ndarray drawn image
        """
        configuration = self.configuration
        img_drawn = img.copy()
        center = self.center_coordinates(start_point, end_point, radius)

        radius_left = radius + int(configuration['line_spread_cm'] / configuration['conversion_pixel_to_cm'])
        cv2.ellipse(img_drawn, (center.x, center.y), (radius_left, radius_left), 0, 0, 360, color,
                    thickness=int(configuration['line_width_cm'] / configuration['conversion_pixel_to_cm']))

        radius_right = radius - int(configuration['line_spread_cm'] / configuration['conversion_pixel_to_cm'])
        cv2.ellipse(img_drawn, (center.x, center.y), (radius_right, radius_right), 0, 0, 360, color,
                    thickness=int(configuration['line_width_cm'] / configuration['conversion_pixel_to_cm']))
        return img_drawn


    def draw_central_dashed_line_on_ground(self, img, start_point, end_point, color):
        """
        Plot central dashed line. See configuration file for line specifications
        :param img: numpy.ndarray, image opened with OpenCV
        :param start_point: Point
        :param end_point: Point
        :param color: RGB numpy.array (3 colors between 0 & 255)
        :return: numpy.ndarray drawn image
        """
        configuration = self.configuration
        img_drawn = img.copy()
        vector = end_point - start_point
        vector_normalized = vector / vector.norm()
        segment_number = int(vector.norm() // (configuration['dash_length_cm'] / configuration['conversion_pixel_to_cm']))
        segments_points = [start_point + i * (configuration['dash_length_cm'] / configuration['conversion_pixel_to_cm'])
                           * vector_normalized for i in range(segment_number + 1)]
        for i, couple in enumerate(zip(segments_points[:-1], segments_points[1:])):
            if i % 2 == 0:
                cv2.line(img_drawn, (int(round(couple[0].x)), int(round(couple[0].y))),
                         (int(round(couple[1].x)), int(round(couple[1].y))),
                         color, thickness=int(configuration['line_width_cm'] / configuration['conversion_pixel_to_cm']))
        return img_drawn


    def draw_lateral_complete_lines_on_ground(self, img, start_point, end_point, color):
        """
        Plot lateral complete line. See configuration file for line specifications
        :param img: numpy.ndarray, image opened with OpenCV
        :param start_point: Point
        :param end_point: Point
        :param color: RGB numpy.array (3 colors between 0 & 255)
        :return: numpy.ndarray drawn image
        """
        configuration = self.configuration
        img_drawn = img.copy()
        vector = end_point - start_point
        vector_normalized = vector / vector.norm()
        vector_normalized_othogonal = Point(-vector_normalized.y, vector_normalized.x)
        width = int(configuration['line_spread_cm'] / configuration['conversion_pixel_to_cm'])
        left_point = start_point + width * vector_normalized_othogonal
        left_constant = left_point.y - left_point.x * vector.y / vector.x

        right_point = start_point - width * vector_normalized_othogonal
        right_constant = right_point.y - right_point.x * vector.y / vector.x

        img_height = img.shape[1]
        img_width = img.shape[0]

        cv2.line(img_drawn, (int((img_height - right_constant) * vector.x / vector.y), img_height),
                 (img_width, int(img_width * vector.y / vector.x + right_constant)),
                 color, thickness=int(configuration['line_width_cm'] / configuration['conversion_pixel_to_cm']))

        cv2.line(img_drawn, (int((img_height - left_constant) * vector.x / vector.y), img_height),
                 (img_width, int(img_width * vector.y / vector.x + left_constant)),
                 color, thickness=int(configuration['line_width_cm'] / configuration['conversion_pixel_to_cm']))

        return img_drawn

    def compute_command_arc(self, start_point, end_point, radius):
        """
        Computes the angular command associated with an arc. Camera position is in bottom, right in the middle

        :param start_point: Point, starting point for the arc
        :param end_point: Point, end point for the arc
        :param radius: real positive value
        :return: angular command in degrees (signed, clockwise)
        """
        configuration = self.configuration
        center = self.center_coordinates(start_point, end_point, radius)
        # self.logger.debug({'operation': 'compute_command_arc.center', 'x': center.x, 'y': center.y})

        y, x = np.ogrid[0: configuration['image_width'], 0: configuration['image_height']]
        epsilon = 2
        mask = np.abs(np.sqrt((center.x - x) ** 2 + (center.y - y) ** 2) - radius) <= epsilon
        y_arc, x_arc = np.where(mask == True)

        # computes the projection on line
        car_position_x, car_position_y = (int(configuration['image_width'] / 2), configuration['image_height'])
        dists_from_ligne = list(((x_arc - car_position_x) ** 2 + (y_arc - car_position_y) ** 2))
        index_projection = dists_from_ligne.index(min(dists_from_ligne))  # output the first index, enough
        projection_y = y_arc[index_projection]
        projection_x = x_arc[index_projection]

        # self.logger.debug({'operation': 'compute_command_arc.projection', 'x': projection_x, 'y': projection_y})

        # computes the destination point
        dists = np.sqrt((x_arc - projection_x) ** 2 + (y_arc - projection_y) ** 2)
        points_to_consider = \
            np.where(dists <= configuration['command_distance_cm'] / configuration['conversion_pixel_to_cm'])[0]

        command_x = x_arc[min(points_to_consider)]
        command_y = y_arc[min(points_to_consider)]

        destination = Point(command_x, command_y) - \
                      Point(x_arc[-1], y_arc[-1])

        # self.logger.debug({'operation': 'compute_command_arc.commande', 'x': destination.x, 'y': destination.y})

        vector_base = Point(1, 0)  # Computing the angle from the base
        angular_command = angle_clockwise(vector_base, destination)
        return angular_command


    def compute_command_line(self, start_point, end_point):
        configuration = self.configuration
        y, x = np.ogrid[0: configuration['image_width'], 0: configuration['image_height']]
        epsilon = 1000
        line_orientation = end_point - start_point
        mask = np.abs((x - start_point.x) * (line_orientation.y) - (y - start_point.y) * (line_orientation.x)) <= epsilon
        y_line, x_line = np.where(mask == True)

        # computes the projection on line
        car_position_x, car_position_y = (int(configuration['image_width'] / 2), configuration['image_height'])
        dists_from_ligne = list(((x_line - car_position_x) ** 2 + (y_line - car_position_y) ** 2))
        index_projection = dists_from_ligne.index(min(dists_from_ligne))  # output the first index, enough
        projection_y = y_line[index_projection]
        projection_x = x_line[index_projection]

        # computes the destination point
        dists = np.sqrt((x_line - projection_x) ** 2 + (y_line - projection_y) ** 2)
        points_to_consider = \
            np.where(dists <= configuration['command_distance_cm'] / configuration['conversion_pixel_to_cm'])[0]

        command_x = x_line[min(points_to_consider)]
        command_y = y_line[min(points_to_consider)]

        destination = Point(command_x, command_y) - \
                      Point(x_line[-1], y_line[-1])

        vector_base = Point(1, 0)  # Computing the angle from the base
        angular_command = angle_clockwise(vector_base, destination)

        return angular_command
