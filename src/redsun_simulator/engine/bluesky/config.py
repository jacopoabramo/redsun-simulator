from attrs import define, field
from sunflare.config import MotorInfo

__all__ = ["OpenWFSMotorInfo"]


@define
class OpenWFSMotorInfo(MotorInfo):
    # TODO: add link to main documentation
    """Configuration information for the OpenWFSMotor.

    See the following link_ for the base class.

    _link: https://redsun-acquisition.github.io/sunflare/api/config/#sunflare.config.MotorInfo

    Attributes
    ----------
    setpoint_time : ``float``, optional
        - Time required to simulate the motor moving to the setpoint in seconds.
        - Default is 0.1 seconds.
    shutdown_time : ``float``, optional
        - Time required to simulate the motor shutdown in seconds.
        - Default is 0.5 seconds.
    """

    setpoint_time: float = field(default=0.5)
    shutdown_time: float = field(default=0.5)
