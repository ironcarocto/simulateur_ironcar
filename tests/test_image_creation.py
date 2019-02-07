from simulator.image_creation import center_coordinates
from utils import Point


def test_center_coordinates_computation_is_correct():
    # Given
    expected = Point(172, 728)

    # When
    result = center_coordinates(Point(400, 400), Point(500, 500), 400)

    # Then
    assert result == expected



