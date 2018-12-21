from simulateur.picture_generation import Point
from simulateur.picture_generation import compute_command_line


def test_first_to_fail():
    # Given
    # Where
    # Then
    assert False


def test_compute_angle():
    origin = Point(500, 1000)
    end = Point(800, 0)
    radius = 2000
    compute_command_arc(origin, end, radius)



def test_compute_line():
    origin = Point(500, 1000)
    end = Point(600, 0)
    compute_command_line(origin, end)

