"""FinanceAI package initialization."""

__version__ = "1.0.0"
__author__ = "FinanceAI Team"
__description__ = "Intelligent Financial Market Analysis Platform"

from finance_ai.entities import (
    MarketData,
    Portfolio,
    RiskAssessment,
    TradingSignal,
)

__all__ = [
    "MarketData",
    "TradingSignal",
    "Portfolio",
    "RiskAssessment",
]
