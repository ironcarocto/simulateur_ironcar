import pytest
from colour import Color, hex2rgb

def test_Color_constructor_parse_white_color_from_hexadecimal_value():
    c = Color('#ffffff')
    assert c.rgb == (1.0, 1.0, 1.0)


def test_Color_constructor_raise_an_error_when_color_value_is_invalid():
    with pytest.raises(AttributeError, match="'#ff' is not in web format. Need 3 or 6 hex digit."):
        Color('#ff')


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
        pytest.fail('color is not valid %s'.format(value))
