from math import acos
from math import pi
from math import sqrt
import numpy as np


def length(vec):
    """
    Computes the norm of a 2 coordinates vector v
    :param vec: Point
    :return: norm
    """
    return sqrt(vec.x ** 2 + vec.y ** 2)


def dot_product(vec1, vec2):
    """
    Computes the dot scalar product of 2  2D vectors v and w
    :param vec1: Point
    :param vec2: Point
    :return: scalar product
    """
    return vec1.x * vec2.x + vec1.y * vec2.y


def determinant(vec1, vec2):
    """
    Computes the determinant product of 2 2D vectors v and w
    :param vec1: Point
    :param vec2: Point
    :return: determinant
    """
    return vec1.x * vec2.y - vec1.y * vec2.x


def inner_angle(vec1, vec2):
    """
    Computes the inner angle between 2 2D vectors v and w
    :param vec1: Point
    :param vec2: Point
    :return: inner angle (in degrees)
    """
    cosx = dot_product(vec1, vec2) / (length(vec1) * length(vec2))
    rad = acos(cosx)  # in radians
    return rad * 180 / pi  # returns degrees


def angle_clockwise(vec1, vec2):
    """
    Computes the oriented angle between 2 2D vectors v and w
    :param vec1: Point
    :param vec2: Point
    :return: oriented angle (in degrees)
    """
    res = None
    inner = inner_angle(vec1, vec2)
    det = determinant(vec1, vec2)
    if det < 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
        res = inner
    else:  # if the det > 0 then A is immediately clockwise of B
        res = -inner

    return res


class Point:
    """
    Point/Vector definition
    """

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

    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar)

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def norm(self):
        return np.sqrt(float(self.x) * float(self.x) + float(self.y) * float(self.y))
