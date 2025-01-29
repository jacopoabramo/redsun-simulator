"""``pytest`` test cases for the ``model`` module."""

import time
from typing import Tuple

import bluesky.plan_stubs as bps
import numpy as np
import pytest
import yaml
from typing import Any
from bluesky.protocols import Location
from bluesky.run_engine import RunEngine
from bluesky.utils import MsgGenerator

from redsun_simulator import OpenWFSMotor, OpenWFSMotorInfo


@pytest.fixture
def motor_config(motor_config_path: str) -> dict[str, OpenWFSMotorInfo]:
    """Return the motors configuration."""

    motors: dict[str, OpenWFSMotorInfo] = {}

    with open(motor_config_path, "r") as file:
        config_dict: dict[str, Any] = yaml.safe_load(file)
        for name, values in config_dict["models"].items():
            config = OpenWFSMotorInfo(**values)
            motors[name] = config
    return motors

@pytest.fixture
def RE() -> RunEngine:
    """Return a ``RunEngine`` instance."""
    return RunEngine()

def test_motor_construction(motor_config: dict[str, OpenWFSMotorInfo]) -> None:
    """Test the motor object construction."""

    for name, info in motor_config.items():
        motor = OpenWFSMotor(name, info)
        assert motor.name == name
        assert motor.model_info.axis == info.axis
        assert motor.model_info.egu == info.egu
        assert motor.model_info.step_size == info.step_size
        assert motor.model_info.shutdown_time == info.shutdown_time

def test_motor_configurable_protocol(motor_config: dict[str, OpenWFSMotorInfo]) -> None:
    for name, info in motor_config.items():
        motor = OpenWFSMotor(name, info)
        cfg = motor.read_configuration()
        assert cfg == {
            "vendor": {"value": "N/A", "timestamp": 0},
            "serial_number": {"value": "N/A", "timestamp": 0},
            "plugin_name": {"value": "N/A", "timestamp": 0},
            "repository": {"value": "N/A", "timestamp": 0},
            "axis": {"value": info.axis, "timestamp": 0},
            "step_size": {"value": info.step_size, "timestamp": 0},
            "egu": {"value": info.egu, "timestamp": 0},
            "setpoint_time": {"value": info.setpoint_time, "timestamp": 0},
            "shutdown_time": {"value": info.shutdown_time, "timestamp": 0},
        }

def test_motor_properties(motor_config: dict[str, OpenWFSMotorInfo]) -> None:
    """Test changing properties.
    
    Only valid for properties that implement ``@property.setter``.
    """
    
    for name, info in motor_config.items():
        motor = OpenWFSMotor(name, info)

        # change axis
        axis = "Y"
        assert motor.current_axis == info.axis[0]
        motor.current_axis = axis
        assert motor.current_axis == info.axis[1]
        axis = "Z"
        motor.current_axis = axis
        assert motor.current_axis == info.axis[2]

def test_motor_set_direct(motor_config: dict[str, OpenWFSMotorInfo]) -> None:
    """Test the motor movement via direct invocation of the ``set`` method.
    
    The test moves the motor to position 100 and then to position 200.
    It evaluates that after ``set`` is called, the motor is at the new position,
    the ``Status`` is marked as done and successful, and the ``locate`` method
    returns the new position with the readback value set to the previous position.
    """

    for name, info in motor_config.items():
        motor = OpenWFSMotor(name, info)
        # attempting to move a motor along an axis
        # that does not exist should raise an error
        with pytest.raises(IndexError):
            # actual axis are X, Y, Z
            # maybe generate randomly?
            motor.current_axis = "A"

        for axis in motor.model_info.axis:
            motor.current_axis = axis
            status = motor.set(100)
            status.wait()
            assert status.done
            assert status.success
            assert motor.locate() == Location(setpoint=100.0, readback=100.0)

            status = motor.set(200)
            status.wait()
            assert status.done
            assert status.success
            assert motor.locate() == Location(setpoint=200.0, readback=200.0)

def test_motor_shutdown(motor_config: dict[str, OpenWFSMotorInfo]) -> None:
    """Test the motor shutdown.
    
    Inject a shutdown time of 0.5 and 1.0 seconds and evaluate that the
    motor takes the expected time to shutdown.
    """
    
    shutdown_times: list[float] = [t for t in np.arange(0, 1.5, 0.5)]

    for name, info in motor_config.items():
        for t in shutdown_times:
            info.shutdown_time = t
            motor = OpenWFSMotor(name, info)
            start = time.time()
            motor.shutdown()
            end = time.time()
            assert end - start == pytest.approx(t, abs=0.2)

def test_motor_plan_absolute(motor_config: dict[str, OpenWFSMotorInfo], RE: RunEngine) -> None:
    """Test motor execution in a ``RunEngine`` plan.
    
    Motors will move based on absolute positions.

    - first move to position 100;
    - then move to position 200.
    """
    def moving_plan(motors: Tuple[OpenWFSMotor, ...]) -> MsgGenerator:
        """Move the motor to position 100 and then to position 200."""
        for m in motors:
            yield from bps.mv(m, 100)
            yield from bps.mv(m, 200)
            assert m.locate() == Location(setpoint=200.0, readback=200.0)
    
    motors = tuple([OpenWFSMotor(name, info) for name, info in motor_config.items()])
    RE(moving_plan(motors))

def test_motor_plan_relative(motor_config: dict[str, OpenWFSMotorInfo], RE: RunEngine) -> None:
    """Test motor execution in a ``RunEngine`` plan.
    
    Motors will move based on relative positions.

    - first move of 100;
    - then move of 200.
    """
    def moving_plan(motors: Tuple[OpenWFSMotor, ...]) -> MsgGenerator:
        """Move the motor of 100 steps and then of 200 steps."""
        for m in motors:
            yield from bps.mvr(m, 100)
            yield from bps.mvr(m, 200)
            assert m.locate() == Location(setpoint=300.0, readback=300.0)
    
    motors = tuple([OpenWFSMotor(name, info) for name, info in motor_config.items()])
    RE(moving_plan(motors))
