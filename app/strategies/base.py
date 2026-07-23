from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class Strategy(ABC):
    """
    Base class for every trading strategy.
    """

    @abstractmethod
    def generate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals.

        Returns:
            DataFrame enriched with trading signals.
        """
        raise NotImplementedError