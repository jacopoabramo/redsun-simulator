from __future__ import annotations

from time import sleep

import astropy.units as u  # type: ignore[import-untyped]
from astropy.units import Quantity
from openwfs import Actuator  # type: ignore[import-untyped]
from sunflare.engine import Status

from bluesky.protocols import Location

from .config import OpenWFSMotorInfo


class OpenWFSMotor(Actuator):
    """OpenWFSMotor model."""

    def __init__(self, name: str, model_info: OpenWFSMotorInfo) -> None:
        self._name = name
        self._model_info = model_info
        self._axis = model_info.axis
        self._step_size = model_info.step_size

        self._setpoint: dict[str, float] = {axis: 0.0 for axis in model_info.axis}
        self._readback: dict[str, float] = {axis: 0.0 for axis in model_info.axis}

        self._current_axis = model_info.axis[0]
        self._shutdown_time = model_info.shutdown_time
        self._setpoint_time = model_info.setpoint_time

        super().__init__(duration=0 * u.ms, latency=0 * u.ms)

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
        return Location(
            setpoint=self._setpoint[self.current_axis],
            readback=self._readback[self.current_axis],
        )

    @property
    def current_axis(self) -> str:
        """The current axis of the motor."""
        return self._current_axis

    @current_axis.setter
    def current_axis(self, axis: str) -> None:
        if axis not in self.model_info.axis:
            raise IndexError(f"Axis {axis} is not in {self.model_info.axis}")
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
        self.wait(up_to=Quantity(self.setpoint_time * 1000, u.ms))
        self._readback[self.current_axis] = self._setpoint[self.current_axis]

    @property
    def model_info(self) -> OpenWFSMotorInfo:
        """The model information."""
        return self._model_info

    @property
    def name(self) -> str:
        """The name of the motor."""
        return self._name

    @property
    def parent(self) -> None:
        return None
