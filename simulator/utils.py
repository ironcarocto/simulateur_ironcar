from math import acos
from math import pi
from math import sqrt
import numpy as np


def length(v):
    """
    Computes the norm of a 2 coordinates vector v
    :param v: Point
    :return: norm
    """
    return sqrt(v.x ** 2 + v.y ** 2)


def dot_product(v, w):
    """
    Computes the dot scalar product of 2  2D vectors v and w
    :param v: Point
    :param w: Point
    :return: scalar product
    """
    return v.x * w.x + v.y * w.y


def determinant(v, w):
    """
    Computes the determinant product of 2 2D vectors v and w
    :param v: Point
    :param w: Point
    :return: determinant
    """
    return v.x * w.y - v.y * w.x


def inner_angle(v, w):
    """
    Computes the inner angle between 2 2D vectors v and w
    :param v: Point
    :param w: Point
    :return: inner angle (in degrees)
    """
    cosx = dot_product(v, w) / (length(v) * length(w))
    rad = acos(cosx)  # in radians
    return rad * 180 / pi  # returns degrees


def angle_clockwise(v, w):
    """
    Computes the oriented angle between 2 2D vectors v and w
    :param v: Point
    :param w: Point
    :return: oriented angle (in degrees)
    """
    inner = inner_angle(v, w)
    det = determinant(v, w)
    if det < 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else:  # if the det > 0 then A is immediately clockwise of B
        return -inner


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