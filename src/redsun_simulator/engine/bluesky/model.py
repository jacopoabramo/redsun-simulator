from __future__ import annotations

import astropy.units as u # type: ignore[import-untyped]
from astropy.units import Quantity

from time import sleep
from typing import Any, Optional

from sunflare.engine import MotorModel, Status
from sunflare.types import Location

from .config import OpenWFSMotorInfo

from ._core import SingleAxisStage


class OpenWFSMotor(MotorModel[OpenWFSMotorInfo]):
    """OpenWFSMotor model."""

    def __init__(self, name: str, model_info: OpenWFSMotorInfo) -> None:
        
        self._motors: dict[str, SingleAxisStage] = {
            axis: SingleAxisStage(model_info.step_size, axis)
            for axis in model_info.axes
        }

        self._setpoint: dict[str, float] = {axis: 0.0 for axis in model_info.axes}
        self._readback: dict[str, float] = {axis: 0.0 for axis in model_info.axes}

        self._current_axis = model_info.axes[0]
        self._shutdown_time = model_info.shutdown_time
        self._setpoint_time = model_info.setpoint_time

        super().__init__(name, model_info)

    def shutdown(self) -> None:
        """Shutdown the motor.

        Simulates a waiting time for the motor to shutdown.
        """
        sleep(self.model_info.shutdown_time)

    def set(self, value: float) -> Status:
        """Start moving the motor to the setpoint.
        
        The axis along which to move is determined by the ``current_axis`` attribute.
        A ``Status`` object is returned to track the movement; this has a callback
        to simulate the setpoint being reached.

        Parameters
        ----------
        value : AxisLocation[float]
            The location to move to.
        
        Returns
        -------
        status : Status
            The status of the movement
        """
        s = Status()
        s.add_callback(self._wait_readback)
        self._setpoint[self.current_axis] = value
        s.set_finished()
        return s

    def locate(self) -> Location[float]:
        """Return the current location of a Device.

        While a ``Readable`` reports many values, a ``Movable`` will have the
        concept of location. This is where the Device currently is, and where it
        was last requested to move to. This protocol formalizes how to get the
        location from a ``Movable``.

        The axis associated with the returned ``Location`` is determined by the
        ``current_axis`` attribute.

        Returns
        -------
        location : AxisLocation[float]
            The current location of the Device.
        """
        return Location(setpoint=self._setpoint[self.current_axis], readback=self._readback[self.current_axis])
    
    @property
    def current_axis(self) -> str:
        """The current axis of the motor."""
        return self._current_axis
    
    @current_axis.setter
    def current_axis(self, axis: str) -> None:
        if axis not in self.model_info.axes:
            raise IndexError(f"Axis {axis} is not in {self.model_info.axes}")
        self._current_axis = axis

    @property
    def shutdown_time(self) -> float:
        """The time required to simulate the motor shutdown in seconds."""
        return self.model_info.shutdown_time

    @property
    def setpoint_time(self) -> float:
        """The time required to simulate the motor moving to the setpoint in seconds."""
        return self.model_info.setpoint_time

    def _wait_readback(self, _: Status) -> None:
        """Simulate the motor moving to the setpoint via a callback.
        
        Parameters
        ----------
        s : Status
            The status object (not used).
        """
        self._motors[self.current_axis].wait(up_to=Quantity(self.setpoint_time * 1000, u.ms))
        self._readback[self.current_axis] = self._setpoint[self.current_axis]
    
    @property
    def parent(self) -> Optional[Any]:
        # TODO: how to get rid of this?
        #       or alternatively, how to make it useful?
        return None

