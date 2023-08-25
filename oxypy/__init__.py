"""

"""

__all__ = ["Either", "Debug", "Default", "Option", "Panic", "Result"]
__version__ = "1.0.1"
__version_info__ = (1, 0, 1)
__author__ = "Ross Morgan"
__email__ = "rmorgan512@protonmail.ch"

from .debug import Debug
from .default import Default
from .panic import Panic

from .either import Either
from .option import Option
from .result import Result
