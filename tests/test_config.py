"""``pytest`` test cases for the ``config`` module."""
import yaml
from typing import Any

from redsun_simulator import OpenWFSMotorInfo, OpenWFSCameraInfo
from redsun_simulator.openwfs._config import Specimen


def test_motor_model_info(motor_config_path: str) -> None:
    """Test the OpenWFSMotorInfo information model."""

    config: OpenWFSMotorInfo

    with open(motor_config_path, "r") as file:
        config_dict: dict[str, Any] = yaml.safe_load(file)
        for _, values in config_dict["models"].items():
            config = OpenWFSMotorInfo(**values)

    assert config.model_name == "OpenWFSMotor"
    assert config.axis == ["X", "Y", "Z"]
    assert config.step_size == {"X": 100.0, "Y": 100.0, "Z": 100.0}
    assert config.egu == "um"
    assert config.shutdown_time == 0.5
    assert config.setpoint_time == 0.1

def test_camera_model_info(camera_config_path: str) -> None:
    config: OpenWFSCameraInfo
    
    specimen_truth = Specimen(
        resolution=[1024, 1024],
        pixel_size=float(60),
        magnification=40,
        numerical_aperture=0.85,
        wavelength=532.8
    )

    with open(camera_config_path, "r") as file:
        config_dict: dict[str, Any] = yaml.safe_load(file)
        for _, values in config_dict["models"].items():
            config = OpenWFSCameraInfo(**values)

    assert config.model_name == "OpenWFSCamera"
    assert config.specimen == specimen_truth
    assert config.sensor_shape == (256, 256)
    assert config.pixel_size == (8.5, 8.5, 8.5)
