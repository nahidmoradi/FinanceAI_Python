"""Use case interfaces following Clean Architecture principles."""

from finance_ai.use_cases.interfaces.ai_service_interface import AIServiceInterface
from finance_ai.use_cases.interfaces.market_data_repository_interface import (
    MarketDataRepositoryInterface,
)
from finance_ai.use_cases.interfaces.portfolio_repository_interface import (
    PortfolioRepositoryInterface,
)
from finance_ai.use_cases.interfaces.prompt_catalog_interface import (
    PromptCatalogInterface,
)
from finance_ai.use_cases.interfaces.risk_assessment_repository_interface import (
    RiskAssessmentRepositoryInterface,
)
from finance_ai.use_cases.interfaces.trading_signal_repository_interface import (
    TradingSignalRepositoryInterface,
)
from finance_ai.use_cases.interfaces.vector_store_interface import VectorStoreInterface

__all__ = [
    "AIServiceInterface",
    "PromptCatalogInterface",
    "MarketDataRepositoryInterface",
    "TradingSignalRepositoryInterface",
    "PortfolioRepositoryInterface",
    "RiskAssessmentRepositoryInterface",
    "VectorStoreInterface",
]
