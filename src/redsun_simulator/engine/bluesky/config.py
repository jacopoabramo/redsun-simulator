from typing import ClassVar

from psygnal import SignalGroupDescriptor
from pydantic import Field
from sunflare.config import MotorModelInfo

__all__ = ["OpenWFSMotorInfo"]


class OpenWFSMotorInfo(MotorModelInfo):
    # TODO: add link to main documentation
    """Configuration information for the OpenWFSMotor.

    Attributes
    ----------
    setpoint_time : ``float``, optional
        - Time required to simulate the motor moving to the setpoint in seconds.
        - Default is 0.1 seconds.
    
    shutdown_time : ``float``, optional
        - Time required to simulate the motor shutdown in seconds.
        - Default is 0.5 seconds.
    """

    setpoint_time: float = Field(
        default=0.1,
        title="Setpoint time",
        description="Time required to simulate the motor moving to the setpoint in seconds.",
    )
    shutdown_time: float = Field(
        default=0.5,
        title="Shutdown time",
        description="Time required to simulate the motor shutdown in seconds.",
    )
    events: ClassVar[SignalGroupDescriptor] = SignalGroupDescriptor()
