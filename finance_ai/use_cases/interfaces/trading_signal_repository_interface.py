"""Trading signal repository interface."""

from abc import ABC, abstractmethod
from datetime import datetime

from finance_ai.entities.trading_signal import SignalType, TradingSignal


class TradingSignalRepositoryInterface(ABC):
    """Interface for trading signal persistence."""

    @abstractmethod
    async def save_signal(self, signal: TradingSignal) -> str:
        """Save a trading signal.

        Args:
            signal: Trading signal entity.

        Returns:
            Signal ID.

        Raises:
            RepositoryError: If save fails.
        """

    @abstractmethod
    async def get_signal_by_id(self, signal_id: str) -> TradingSignal | None:
        """Retrieve signal by ID.

        Args:
            signal_id: Unique signal identifier.

        Returns:
            Trading signal or None if not found.

        Raises:
            RepositoryError: If retrieval fails.
        """

    @abstractmethod
    async def get_active_signals(
        self,
        symbol: str | None = None,
        signal_type: SignalType | None = None,
    ) -> list[TradingSignal]:
        """Get all active trading signals with optional filters.

        Args:
            symbol: Optional symbol filter.
            signal_type: Optional signal type filter.

        Returns:
            List of active signals.

        Raises:
            RepositoryError: If retrieval fails.
        """

    @abstractmethod
    async def deactivate_signal(self, signal_id: str) -> bool:
        """Mark a signal as inactive.

        Args:
            signal_id: Signal to deactivate.

        Returns:
            True if successful.

        Raises:
            RepositoryError: If update fails.
        """
