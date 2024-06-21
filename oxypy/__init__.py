"""

"""

__all__ = [
    "Either", "Option", "Result",
    "dbg", "Debug", "Default",
    "panic", "PartialEq", "PartialOrd",
]

__version_info__ = (1, 1, 0)
__version__ = "1.1.0"
__author__ = "Ross Morgan"
__email__ = "rmorgan512@protonmail.ch"

from .debug import Debug, dbg
from .default import Default
from .ops import PartialEq, PartialOrd
from .panic import panic

from .either import Either
from .option import Option
from .result import Result
