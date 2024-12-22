# noqa: D104
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("redsun_simulator")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


from .engine.bluesky.model import OpenWFSMotor
from .engine.bluesky.config import OpenWFSMotorInfo

__all__ = (
    "OpenWFSMotor",
    "OpenWFSMotorInfo",
)
