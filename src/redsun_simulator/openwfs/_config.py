from attrs import converters, define, field, setters, validators
from sunflare.config import ModelInfo

__all__ = ["OpenWFSMotorInfo", "OpenWFSCameraInfo"]


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
    setpoint_time: float = field(default=0.1)
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


@define
class Specimen:
    """Container for specimen information.

    It is used in conjunction with
    :class:``openwfs.simulation.StaticSource``
    to generate a fake moving sample.

    Parameters
    ----------
    resolution: ``tuple[int, int]``
        Specimen resolution in pixels (height, width).
    pixel_size: ``float``
        Pixel size in nanometers.
    magnification: ``int``
        # Magnification from object plane to camera.
    numerical_aperture: ``float``
        Numerical aperture of the microscope objective.
    wavelength: ``float``
        Wavelength of the light source in nanometers.

    """

    resolution: tuple[int, int] = field(
        converter=tuple[int, int], on_setattr=setters.frozen
    )
    pixel_size: float = field(
        validator=validators.instance_of(float), on_setattr=setters.frozen
    )
    magnification: int = field(validator=validators.instance_of(int))
    numerical_aperture: float = field(validator=validators.instance_of(float))
    wavelength: float = field(validator=validators.instance_of(float))


@define(kw_only=True)
class OpenWFSCameraInfo(ModelInfo):
    """Configuration information for the OpenWFSCamera.

    See the following link_ for the base class.

    _link: https://redsun-acquisition.github.io/sunflare/api/config/#sunflare.config.MotorInfo

    Attributes
    ----------
    specimen: ``Specimen``
        Information about the specimen.
    sensor_shape : ``tuple[int, int]``
        Shape of the detector sensor.
    pixel_size : ``tuple[float, float, float]``
        Detector pixel size.

    """

    specimen: Specimen = field(
        converter=converters.pipe(
            # if input is already a Specimen, return as is
            lambda x: x if isinstance(x, Specimen) else Specimen(**x)
        )
    )
    sensor_shape: tuple[int, int] = field(
        converter=tuple[int, int], on_setattr=setters.frozen
    )
    pixel_size: tuple[float, float, float] = field(
        converter=tuple[float, float, float], on_setattr=setters.frozen
    )

    @sensor_shape.validator
    def _validate_sensor_shape(
        self, _: tuple[int, ...], value: tuple[int, ...]
    ) -> None:
        if not all(isinstance(val, int) for val in value):
            raise ValueError("All values in the tuple must be integers.")
        if len(value) != 2:
            raise ValueError("The tuple must contain exactly two values.")

    @pixel_size.validator
    def _validate_pixel_size(
        self, _: tuple[float, ...], value: tuple[float, ...]
    ) -> None:
        if not all(isinstance(val, float) for val in value):
            raise ValueError("All values in the tuple must be floats.")
        if len(value) != 3:
            raise ValueError("The tuple must contain exactly three values.")
