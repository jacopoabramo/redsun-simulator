"""Core simulators built using OpenWFS."""

import numpy as np
from astropy import units as u  # type: ignore[import-untyped]
from openwfs.core import Actuator  # type: ignore[import-untyped]


class SingleAxisStage(Actuator):
    """A simulated stage moving along a specified axis.

    Parameters
    ----------
    axis: str
        The axis of the stage.
    step_size : Quantity[u.um]
        Step size in micrometers.
    """

    def __init__(
        self,
        step_size: float,
        axis: str,
    ) -> None:
        super().__init__(duration=0 * u.ms, latency=0 * u.ms)
        self._step_size = step_size
        self._axis = axis
        self._position = 0.0

    @property
    def axis(self) -> str:
        """Axis of the stage."""
        return self._axis

    @property
    def step_size(self) -> float:
        """Step size in micrometers."""
        return self._step_size

    @step_size.setter
    def step_size(self, value: float):
        self._step_size = value

    @property
    def position(self) -> float:
        """Current position in micrometers."""
        return self._position

    @position.setter
    def position(self, value: float):
        self._position = self.step_size * np.round(value / self.step_size)

    def home(self):
        self._position = 0.0
