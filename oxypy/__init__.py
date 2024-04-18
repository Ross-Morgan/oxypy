"""

"""

__all__ = [
    "Either", "Option", "Result",
    "dbg", "Debug", "Default",
    "PartialEq", "PartialOrd",
]

__version_info__ = (1, 0, 1)
__version__ = ".".join(__version_info__)
__author__ = "Ross Morgan"
__email__ = "rmorgan512@protonmail.ch"

from .debug import Debug, dbg
from .default import Default
from .ops import PartialEq, PartialOrd
from .panic import panic

from .either import Either
from .option import Option
from .result import Result
