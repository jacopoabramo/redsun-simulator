from attrs import define, field, setters, validators
from sunflare.config import ModelInfo

__all__ = ["OpenWFSMotorInfo"]


@define(kw_only=True)
class OpenWFSMotorInfo(ModelInfo):
    """Configuration information for the OpenWFSMotor.

    See the following link_ for the base class.

    _link: https://redsun-acquisition.github.io/sunflare/api/config/#sunflare.config.MotorInfo

    Attributes
    ----------
    axis : ``list[str]``
        - List of axis names.
    step_size : ``dict[str, float]``
        - Dictionary of axis names and their step sizes.
    egu : ``str``
        - Engineering units for the motor.
    setpoint_time : ``float``, optional
        - Time required to simulate the motor moving to the setpoint in seconds.
        - Default is 0.1 seconds.
    shutdown_time : ``float``, optional
        - Time required to simulate the motor shutdown in seconds.
        - Default is 0.5 seconds.

    """

    axis: list[str] = field(factory=list, on_setattr=setters.frozen)
    step_size: dict[str, float] = field(factory=dict)
    egu: str = field(validator=validators.instance_of(str), on_setattr=setters.frozen)
    setpoint_time: float = field(default=0.5)
    shutdown_time: float = field(default=0.5)

    @axis.validator
    def _validate_axis(self, _: str, value: list[str]) -> None:
        if not all(isinstance(val, str) for val in value):
            raise ValueError("All values in the list must be strings.")
        if len(value) == 0:
            raise ValueError("The list must contain at least one element.")

    @step_size.validator
    def _validate_step_size(self, _: str, value: dict[str, float]) -> None:
        if not all(isinstance(val, float) for val in value.values()):
            raise ValueError("All values in the dictionary must be floats.")
        if len(value) == 0:
            raise ValueError("The dictionary must contain at least one element.")
