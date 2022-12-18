import pytest
from app import kelvinToCelcius, formatWindSpeed


def test_ktoc():
    assert kelvinToCelcius(1) == "-272°C"
    assert kelvinToCelcius(300) == "27°C"
    assert kelvinToCelcius(280.15) == "7°C"
    with pytest.raises(TypeError) as exp:
        assert kelvinToCelcius("A")


def test_format_wind_speed():
    with pytest.raises(TypeError) as exp:
        assert formatWindSpeed()
    assert formatWindSpeed(2.5) == "9 km/h"
    assert formatWindSpeed(8) == "29 km/h"
    with pytest.raises(TypeError) as exp:
        assert formatWindSpeed("fafa")


