"""``pytest`` test cases for the ``config`` module."""

import yaml
from redsun_simulator import OpenWFSMotorInfo

def test_motor_model_info(config_path: str) -> None:
    """Test the OpenWFSMotorInfo information model."""

    config: OpenWFSMotorInfo

    with open(config_path, "r") as file:
        config_dict = yaml.safe_load(file)
        for _, values in config_dict["motors"].items():
            config = OpenWFSMotorInfo(**values)

    assert config.model_name == "OpenWFSMotor"
    assert config.axes == ["X", "Y", "Z"]
    assert config.step_egu == "μm"
    assert config.step_size == 1.0
    assert config.return_home is False
    assert config.shutdown_time == 0.5
