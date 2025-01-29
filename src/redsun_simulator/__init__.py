from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("redsun_simulator")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .openwfs import OpenWFSCameraInfo, OpenWFSMotor, OpenWFSMotorInfo

__all__ = (
    "OpenWFSMotor",
    "OpenWFSMotorInfo",
    "OpenWFSCameraInfo",
)
