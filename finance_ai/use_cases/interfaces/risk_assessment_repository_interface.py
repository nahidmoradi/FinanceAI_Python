"""Risk assessment repository interface."""

from abc import ABC, abstractmethod
from datetime import datetime

from finance_ai.entities.risk_assessment import RiskAssessment


class RiskAssessmentRepositoryInterface(ABC):
    """Interface for risk assessment persistence."""

    @abstractmethod
    async def save_assessment(self, assessment: RiskAssessment) -> str:
        """Save a risk assessment.

        Args:
            assessment: Risk assessment entity.

        Returns:
            Assessment ID.

        Raises:
            RepositoryError: If save fails.
        """

    @abstractmethod
    async def get_assessment_by_id(self, assessment_id: str) -> RiskAssessment | None:
        """Retrieve assessment by ID.

        Args:
            assessment_id: Unique assessment identifier.

        Returns:
            Risk assessment or None if not found.

        Raises:
            RepositoryError: If retrieval fails.
        """

    @abstractmethod
    async def get_portfolio_assessments(
        self,
        portfolio_id: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[RiskAssessment]:
        """Get all assessments for a portfolio.

        Args:
            portfolio_id: Portfolio identifier.
            start_date: Optional start date filter.
            end_date: Optional end date filter.

        Returns:
            List of risk assessments.

        Raises:
            RepositoryError: If retrieval fails.
        """

    @abstractmethod
    async def get_latest_assessment(self, portfolio_id: str) -> RiskAssessment | None:
        """Get the most recent assessment for a portfolio.

        Args:
            portfolio_id: Portfolio identifier.

        Returns:
            Latest risk assessment or None.

        Raises:
            RepositoryError: If retrieval fails.
        """
