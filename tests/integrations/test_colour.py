import pytest
from colour import Color, hex2rgb

def test_parsing_white_color_from_hexadecimal_value():
    c = Color('#ffffff')
    assert c.rgb == (1.0, 1.0, 1.0)


def test_Color_parsing_wrong_value_raise_error():
    with pytest.raises(AttributeError, match="'#ff' is not in web format. Need 3 or 6 hex digit."):
        Color('#ff')


def test_parsing_white_color_to_rgb_tuple_directly():
    rgb = hex2rgb('#ffffff')
    assert rgb == (1.0, 1.0, 1.0)


def test_hex2rgb_parsing_wrong_value_raise_error():
    with pytest.raises(ValueError, match="Invalid value '#ff' provided for rgb color."):
        hex2rgb('#ff')


def test_color_value_is_hexadecimal():
    value = '#fff'
    try:
        hex2rgb(value)
    except ValueError:
        pytest.fail('color is not valid %s'.format(value))
