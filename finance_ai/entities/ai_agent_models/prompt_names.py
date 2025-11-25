"""AI agent models and prompt entities."""

from enum import Enum


class PromptNames(str, Enum):
    """Central registry of all AI agent prompt IDs."""

    MARKET_TREND_ANALYSIS = "market_trend_analysis"
    RISK_ASSESSMENT_ANALYSIS = "risk_assessment_analysis"
    TRADING_SIGNAL_GENERATION = "trading_signal_generation"
    PORTFOLIO_OPTIMIZATION = "portfolio_optimization"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    TECHNICAL_INDICATOR_ANALYSIS = "technical_indicator_analysis"
