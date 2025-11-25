"""Portfolio repository interface."""

from abc import ABC, abstractmethod

from finance_ai.entities.portfolio import Portfolio


class PortfolioRepositoryInterface(ABC):
    """Interface for portfolio persistence."""

    @abstractmethod
    async def get_portfolio_by_id(self, portfolio_id: str) -> Portfolio | None:
        """Retrieve portfolio by ID.

        Args:
            portfolio_id: Unique portfolio identifier.

        Returns:
            Portfolio entity or None if not found.

        Raises:
            RepositoryError: If retrieval fails.
        """

    @abstractmethod
    async def get_user_portfolios(self, user_id: str) -> list[Portfolio]:
        """Get all portfolios for a user.

        Args:
            user_id: User identifier.

        Returns:
            List of user's portfolios.

        Raises:
            RepositoryError: If retrieval fails.
        """

    @abstractmethod
    async def save_portfolio(self, portfolio: Portfolio) -> str:
        """Save or update portfolio.

        Args:
            portfolio: Portfolio entity.

        Returns:
            Portfolio ID.

        Raises:
            RepositoryError: If save fails.
        """

    @abstractmethod
    async def delete_portfolio(self, portfolio_id: str) -> bool:
        """Delete a portfolio.

        Args:
            portfolio_id: Portfolio to delete.

        Returns:
            True if successful.

        Raises:
            RepositoryError: If deletion fails.
        """
