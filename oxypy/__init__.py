"""

"""

__all__ = [
    "Either", "Option", "Result",
    "dbg", "Debug", "Default", "Panic",
    "PartialEq", "PartialOrd",
]
__version__ = "1.0.1"
__version_info__ = (1, 0, 1)
__author__ = "Ross Morgan"
__email__ = "rmorgan512@protonmail.ch"

from .debug import Debug, dbg
from .default import Default
from .ops import PartialEq, PartialOrd
from .panic import Panic

from .either import Either
from .option import Option
from .result import Result
