# noqa: D104
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("redsun_simulator")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


from .config import OpenWFSMotorInfo
from .model import OpenWFSMotor

__all__ = (
    "OpenWFSMotor",
    "OpenWFSMotorInfo",
)
