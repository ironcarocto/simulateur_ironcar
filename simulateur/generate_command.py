import numpy as np
from PIL import ImageDraw


class RoadLine:
    '''
        This is a RoadLine. In fact, a RoadLine is not a real line (except when
        the road is straight). A RoadLine represents the line of the center of
        the road. Like this, it is easier to create the 2 real lines that
        constitute the borders of the road.
    '''

    def __init__(self, x0, y0, x1, y1, radius, thickness=10, color=(255, 255, 255)):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.radius = radius
        self.thickness = thickness
        self.color = color

    def copy(self):
        new_line = RoadLine(self.x0, self.y0, self.x1, self.y1, self.radius,
                            thickness=self.thickness, color=self.color)
        return new_line

    def __add__(self, scalar):
        return RoadLine(self.x0 + scalar, self.y0, self.x1 + scalar, self.y1,
                        self.radius, thickness=self.thickness, color=self.color)

    def __sub__(self, scalar):
        return RoadLine(self.x0 - scalar, self.y0, self.x1 - scalar, self.y1,
                        self.radius, thickness=self.thickness, color=self.color)

    def print_line(self):
        print(' point0 : ', self.x0, self.y0, ' point1: ', self.x1, self.y1,
              ' radius: ', self.radius, ' color: ', self.color,
              ' thickness: ', self.thickness)


def middleline2drawing(img, line, width=55, right_turn=True, color_range=None):
    # Real lines
    line1 = line.copy()
    line2 = line.copy()
    middle_line = line.copy()

    draw = ImageDraw.Draw(img)

    draw_line(draw, line1 - int(width / 2), right_turn=right_turn)
    draw_line(draw, line2 + int(width / 2), right_turn=right_turn)
    # draw_line(draw, middle_line, right_turn=right_turn)
    return img


def draw_circle(draw, circle):
    thickness = circle.thickness
    color = circle.color

    x0 = circle.center.x - circle.radius
    y0 = circle.center.y - circle.radius
    x1 = circle.center.x + circle.radius
    y1 = circle.center.y + circle.radius

    start = 0
    end = 360

    if circle.empty == 0:
        for i in range(0, thickness):
            diff = i - int(thickness / 2)
            xy = [x0 + diff, y0, x1 + diff, y1]
            draw.arc(xy, start, end, fill=color)
    else:
        plain_angle = float(circle.plain) / circle.radius
        empty_angle = float(circle.empty) / circle.radius
        for i in range(0, thickness):
            diff = i - int(thickness / 2)
            xy = [x0 + diff, y0, x1 + diff, y1]
            for angle in range(0, int(2 * np.pi / (plain_angle + empty_angle))):
                start = angle * (plain_angle + empty_angle)
                end = start + plain_angle
                draw.arc(xy, start * (180 / np.pi), end * (180 / np.pi), fill=color)


def draw_line(draw, line, right_turn=True, plain=1, empty=0):
    if line.y1 > line.y0:
        x0, y0 = line.x1, line.y1
        x1, y1 = line.x0, line.y0
    else:
        x0, y0 = line.x0, line.y0
        x1, y1 = line.x1, line.y1

    if x0 == x1:
        draw.line([x0, y0, x1, y1], fill=line.color, width=line.thickness)
    else:
        radius = line.radius
        pt0 = Point(x0, y0)
        pt1 = Point(x1, y1)
        center = pts2center(pt0, pt1, radius, right_turn=right_turn)
        thickness = line.thickness
        color = line.color

        circle1 = Circle(center, radius, thickness=thickness, color=color)

        if empty != 0:
            circle1.plain = plain
            circle1.empty = empty

        draw_circle(draw, circle1)


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, pt):
        return Point(self.x + pt.x, self.y + pt.y)

    def __sub__(self, pt):
        return Point(self.x - pt.x, self.y - pt.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def norm(self):
        return np.sqrt(float(self.x) * float(self.x) + float(self.y) * float(self.y))


def pts2center(pt1, pt2, radius, right_turn=True):
    vect = pt2 - pt1
    vect_orthog = Point(-vect.y, vect.x)

    vect_orthog = vect_orthog * (1 / vect_orthog.norm())
    middle = (pt1 + pt2) * 0.5

    triangle_height = np.sqrt(radius * radius - (vect.norm() * 0.5 * vect.norm() * 0.5))
    center = middle + vect_orthog * triangle_height

    # make sure the center is on the correct side of the points
    # it is on the right by default
    symmetry = True
    if center.x > middle.x:
        symmetry = False
    if not right_turn: symmetry = not symmetry
    # if not, take the symmetric point with respect to the middle
    if symmetry:
        center = 2 * middle - center
    return center


class Circle:

    def __init__(self, center, radius, thickness=10, color=(255, 255, 255),
                 plain=300, empty=0):

        if thickness <= 0:
            raise ValueError('thickness must be stricly positive (not {})'.format(thickness))
        if color is None:
            raise ValueError('color must be different from None')

        self.center = center
        self.radius = radius
        self.thickness = thickness
        self.color = color
        self.plain = plain
        self.empty = empty
