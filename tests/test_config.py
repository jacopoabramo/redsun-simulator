"""``pytest`` test cases for the ``config`` module."""
import yaml
from typing import Any

from redsun_simulator import OpenWFSMotorInfo


def test_motor_model_info(config_path: str) -> None:
    """Test the OpenWFSMotorInfo information model."""

    config: OpenWFSMotorInfo

    with open(config_path, "r") as file:
        config_dict: dict[str, Any] = yaml.safe_load(file)
        for _, values in config_dict["models"].items():
            config = OpenWFSMotorInfo(**values)

    assert config.model_name == "OpenWFSMotor"
    assert config.axis == ["X", "Y", "Z"]
    assert config.step_size == {"X": 1.0, "Y": 1.0, "Z": 1.0}
    assert config.egu == "um"
    assert config.shutdown_time == 0.5
