"""Risk assessment entities for portfolio risk management."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk level classifications."""

    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"


class RiskFactor(BaseModel):
    """Individual risk factor in assessment."""

    factor_name: str = Field(
        description="Name of the risk factor",
        examples=["Market Volatility"],
        min_length=1,
        max_length=100,
    )
    category: str = Field(
        description="Risk category",
        examples=["Market Risk", "Liquidity Risk", "Concentration Risk"],
        min_length=1,
    )
    score: Decimal = Field(
        description="Risk score (0-100)",
        examples=[72.5],
        ge=0,
        le=100,
    )
    weight: Decimal = Field(
        description="Weight in overall risk calculation",
        examples=[0.25],
        ge=0,
        le=1,
    )
    description: str = Field(
        description="Detailed risk factor description",
        examples=["High volatility detected in cryptocurrency holdings"],
        min_length=10,
    )
    mitigation_suggestions: list[str] = Field(
        description="Suggested mitigation strategies",
        examples=[["Increase diversification", "Add stable assets"]],
    )

    class Config:
        frozen = True


class RiskMetrics(BaseModel):
    """Quantitative risk metrics."""

    value_at_risk_95: Decimal = Field(
        description="Value at Risk at 95% confidence (USD)",
        examples=[-12500.00],
        le=0,
    )
    value_at_risk_99: Decimal = Field(
        description="Value at Risk at 99% confidence (USD)",
        examples=[-18750.00],
        le=0,
    )
    conditional_var_95: Decimal = Field(
        description="Conditional VaR (Expected Shortfall) at 95%",
        examples=[-15000.00],
        le=0,
    )
    beta: Decimal = Field(
        description="Portfolio beta relative to market",
        examples=[1.35],
    )
    correlation_with_market: Decimal = Field(
        description="Correlation coefficient with market index",
        examples=[0.78],
        ge=-1,
        le=1,
    )
    maximum_drawdown: Decimal = Field(
        description="Maximum historical drawdown percentage",
        examples=[-22.5],
        le=0,
    )
    stress_test_result: Decimal = Field(
        description="Portfolio loss in stress scenario (%)",
        examples=[-35.0],
        le=0,
    )

    class Config:
        frozen = True


class RiskAssessment(BaseModel):
    """Complete risk assessment for a portfolio."""

    assessment_id: str = Field(
        description="Unique assessment identifier",
        examples=["risk_pf123_20240115"],
        min_length=1,
    )
    portfolio_id: str = Field(
        description="Portfolio being assessed",
        examples=["pf_user123_001"],
        min_length=1,
    )
    overall_risk_level: RiskLevel = Field(
        description="Overall risk classification",
        examples=[RiskLevel.MODERATE],
    )
    risk_score: Decimal = Field(
        description="Composite risk score (0-100)",
        examples=[58.3],
        ge=0,
        le=100,
    )
    risk_factors: list[RiskFactor] = Field(
        description="Individual risk factors analyzed",
        min_length=1,
    )
    risk_metrics: RiskMetrics = Field(
        description="Quantitative risk measurements",
    )
    concentration_risk: Decimal = Field(
        description="Concentration risk score (0-100)",
        examples=[45.0],
        ge=0,
        le=100,
    )
    liquidity_risk: Decimal = Field(
        description="Liquidity risk score (0-100)",
        examples=[30.0],
        ge=0,
        le=100,
    )
    market_risk: Decimal = Field(
        description="Market risk score (0-100)",
        examples=[65.0],
        ge=0,
        le=100,
    )
    ai_analysis: str = Field(
        description="AI-generated risk analysis summary",
        examples=["Portfolio shows moderate risk with high crypto exposure..."],
        min_length=50,
    )
    recommendations: list[str] = Field(
        description="Risk mitigation recommendations",
        examples=[["Reduce crypto allocation", "Add bonds", "Increase cash buffer"]],
        min_length=1,
    )
    assessed_at: datetime = Field(
        description="Assessment timestamp",
        examples=["2024-01-15T10:30:00Z"],
    )
    next_assessment_due: datetime = Field(
        description="When next assessment is recommended",
        examples=["2024-01-22T10:30:00Z"],
    )

    class Config:
        frozen = True
