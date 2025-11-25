"""Market data repository interface."""

from abc import ABC, abstractmethod
from datetime import datetime

from finance_ai.entities.market_data import MarketData, TimeFrame


class MarketDataRepositoryInterface(ABC):
    """Interface for market data persistence."""

    @abstractmethod
    async def get_market_data(
        self,
        symbol: str,
        timeframe: TimeFrame,
        start_time: datetime,
        end_time: datetime,
    ) -> MarketData | None:
        """Retrieve market data for a symbol and timeframe.

        Args:
            symbol: Trading symbol.
            timeframe: Time frame for data.
            start_time: Start of date range.
            end_time: End of date range.

        Returns:
            Market data entity or None if not found.

        Raises:
            RepositoryError: If retrieval fails.
        """

    @abstractmethod
    async def save_market_data(self, market_data: MarketData) -> str:
        """Save market data to storage.

        Args:
            market_data: Market data entity to persist.

        Returns:
            Unique identifier of saved data.

        Raises:
            RepositoryError: If save operation fails.
        """

    @abstractmethod
    async def get_latest_price(self, symbol: str) -> float | None:
        """Get the latest price for a symbol.

        Args:
            symbol: Trading symbol.

        Returns:
            Latest price or None if not available.

        Raises:
            RepositoryError: If retrieval fails.
        """
