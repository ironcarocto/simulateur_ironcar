from simulateur.picture_generation import Point
from simulateur.picture_generation import compute_command_arc


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
