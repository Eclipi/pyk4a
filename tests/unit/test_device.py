from typing import Iterator

import pytest

from pyk4a import K4AException, PyK4A


DEVICE_ID = 0
DEVICE_ID_NOT_EXISTS = 99


@pytest.fixture()
def device(device_id_good: int) -> Iterator[PyK4A]:
    device = PyK4A(device_id=device_id_good)
    yield device
    # autoclose
    try:
        if device.opened:
            device.close()
    except K4AException:
        pass


@pytest.fixture()
def device_not_exists(device_id_not_exists: int) -> Iterator[PyK4A]:
    device = PyK4A(device_id=device_id_not_exists)
    yield device
    # autoclose
    try:
        if device.opened:
            device.close()
    except K4AException:
        pass


class TestOpenClose:
    @staticmethod
    def test_open_none_existing_device(device_not_exists: PyK4A):
        with pytest.raises(K4AException):
            device_not_exists.open()

    @staticmethod
    def test_open_existing_device(device: PyK4A):
        device.open()

    @staticmethod
    def test_open_twice(device: PyK4A):
        device.open()
        with pytest.raises(K4AException, match="Device already opened"):
            device.open()


class TestProperties:
    @staticmethod
    def test_sync_jack_status_on_closed_device(device: PyK4A):
        with pytest.raises(K4AException, match="Device is not opened"):
            assert device.sync_jack_status

    @staticmethod
    def test_sync_jack_status(device: PyK4A):
        device.open()
        jack_in, jack_out = device.sync_jack_status
        assert isinstance(jack_in, bool)
        assert isinstance(jack_out, bool)

    @staticmethod
    def test_color_property_on_closed_device(device: PyK4A):
        with pytest.raises(K4AException, match="Device is not opened"):
            assert device.brightness

    @staticmethod
    def test_color_property(device: PyK4A):
        device.open()
        assert device.brightness == 123
        assert device.contrast == 123
        assert device.saturation == 123
        assert device.sharpness == 123
        assert device.backlight_compensation == 123
        assert device.gain == 123
        assert device.powerline_frequency == 123
        assert device.exposure == 123
        assert device.exposure_mode_auto is False
        assert device.whitebalance == 123
        assert device.whitebalance_mode_auto is False

    @staticmethod
    def test_color_property_setter_on_closed_device(device: PyK4A):
        with pytest.raises(K4AException, match="Device is not opened"):
            device.brightness = 123

    @staticmethod
    def test_color_property_setter(device: PyK4A):
        device.open()
        device.brightness = 123
        device.contrast = 123
        device.saturation = 123
        device.sharpness = 123
        device.backlight_compensation = 123
        device.gain = 123
        device.powerline_frequency = 123
        device.exposure = 123
        device.exposure_mode_auto = False
        device.whitebalance = 123
        device.whitebalance_mode_auto = False
