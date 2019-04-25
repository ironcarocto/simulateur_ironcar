import pytest
from colour import Color, hex2rgb

def test_hex2rgb_convert_white_color_into_rgb_tuple():
    rgb = hex2rgb('#ffffff')
    assert rgb == (1.0, 1.0, 1.0)


def test_hex2rgb_raise_an_error_when_color_value_is_not_hexadecimal():
    with pytest.raises(ValueError, match="Invalid value '#ff' provided for rgb color."):
        hex2rgb('#ff')


def test_pattern_to_check_color_value_is_hexadecimal():
    value = '#fff'
    try:
        hex2rgb(value)
    except ValueError:
        # show error message here
        pytest.fail('color is not valid %s'.format(value))
