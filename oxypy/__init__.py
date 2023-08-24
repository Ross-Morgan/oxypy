"""

"""

__all__ = ["Either", "Default", "Option", "Panic", "Result"]
__version__ = "0.1.0"
__version_info__ = (0, 1, 0)
__author__ = "Ross Morgan"
__email__ = "rmorgan512@protonmail.ch"

from .default import Default
from .panic import Panic

from .either import Either
from .option import Option
from .result import Result
