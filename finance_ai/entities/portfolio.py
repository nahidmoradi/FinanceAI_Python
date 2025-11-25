"""Portfolio entities for investment management."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class AssetType(str, Enum):
    """Types of financial assets."""

    CRYPTO = "crypto"
    STOCK = "stock"
    FOREX = "forex"
    COMMODITY = "commodity"
    INDEX = "index"
    BOND = "bond"
    ETF = "etf"


class Asset(BaseModel):
    """Individual asset in a portfolio."""

    asset_id: str = Field(
        description="Unique identifier for the asset",
        examples=["ast_btc_001"],
        min_length=1,
    )
    symbol: str = Field(
        description="Trading symbol",
        examples=["BTC/USD"],
        min_length=1,
        max_length=20,
    )
    asset_type: AssetType = Field(
        description="Type of the asset",
        examples=[AssetType.CRYPTO],
    )
    quantity: Decimal = Field(
        description="Quantity held",
        examples=[2.5],
        gt=0,
    )
    average_entry_price: Decimal = Field(
        description="Average purchase price",
        examples=[42000.00],
        gt=0,
    )
    current_price: Decimal = Field(
        description="Current market price",
        examples=[45123.50],
        gt=0,
    )
    total_value: Decimal = Field(
        description="Total value (quantity * current_price)",
        examples=[112808.75],
        gt=0,
    )
    unrealized_pnl: Decimal = Field(
        description="Unrealized profit/loss",
        examples=[7808.75],
    )
    unrealized_pnl_percentage: Decimal = Field(
        description="Unrealized P&L as percentage",
        examples=[7.44],
    )
    last_updated: datetime = Field(
        description="Last price update timestamp",
        examples=["2024-01-15T10:30:00Z"],
    )

    @field_validator("total_value")
    @classmethod
    def calculate_total_value(cls, value: Decimal, info: dict) -> Decimal:
        """Validate total value matches quantity * current price."""
        if "quantity" in info.data and "current_price" in info.data:
            expected = info.data["quantity"] * info.data["current_price"]
            if abs(value - expected) > Decimal("0.01"):
                return expected
        return value

    class Config:
        frozen = True


class PortfolioAllocation(BaseModel):
    """Asset allocation breakdown."""

    asset_type: AssetType = Field(
        description="Type of asset",
        examples=[AssetType.CRYPTO],
    )
    percentage: Decimal = Field(
        description="Percentage of total portfolio",
        examples=[45.5],
        ge=0,
        le=100,
    )
    value: Decimal = Field(
        description="Total value in this category",
        examples=[112808.75],
        ge=0,
    )

    class Config:
        frozen = True


class PortfolioPerformance(BaseModel):
    """Portfolio performance metrics."""

    total_return: Decimal = Field(
        description="Total return amount",
        examples=[15234.50],
    )
    total_return_percentage: Decimal = Field(
        description="Total return as percentage",
        examples=[13.5],
    )
    daily_return: Decimal = Field(
        description="Daily return percentage",
        examples=[0.8],
    )
    monthly_return: Decimal = Field(
        description="Monthly return percentage",
        examples=[5.2],
    )
    yearly_return: Decimal = Field(
        description="Yearly return percentage",
        examples=[42.5],
    )
    sharpe_ratio: Decimal = Field(
        description="Risk-adjusted return metric",
        examples=[1.8],
    )
    max_drawdown: Decimal = Field(
        description="Maximum portfolio drawdown percentage",
        examples=[-12.5],
        le=0,
    )
    volatility: Decimal = Field(
        description="Portfolio volatility percentage",
        examples=[15.3],
        ge=0,
    )

    class Config:
        frozen = True


class Portfolio(BaseModel):
    """Complete portfolio entity."""

    portfolio_id: str = Field(
        description="Unique portfolio identifier",
        examples=["pf_user123_001"],
        min_length=1,
    )
    user_id: str = Field(
        description="Owner user identifier",
        examples=["usr_123456"],
        min_length=1,
    )
    name: str = Field(
        description="Portfolio name",
        examples=["Crypto Growth Portfolio"],
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        description="Portfolio description",
        examples=["Long-term cryptocurrency investment strategy"],
        max_length=500,
    )
    assets: list[Asset] = Field(
        description="List of assets in portfolio",
        min_length=0,
    )
    total_value: Decimal = Field(
        description="Total portfolio value",
        examples=[248500.00],
        ge=0,
    )
    cash_balance: Decimal = Field(
        description="Available cash balance",
        examples=[25000.00],
        ge=0,
    )
    allocation: list[PortfolioAllocation] = Field(
        description="Asset allocation breakdown",
    )
    performance: PortfolioPerformance | None = Field(
        default=None,
        description="Performance metrics",
    )
    created_at: datetime = Field(
        description="Portfolio creation timestamp",
        examples=["2024-01-01T00:00:00Z"],
    )
    last_rebalanced: datetime | None = Field(
        default=None,
        description="Last rebalancing timestamp",
        examples=["2024-01-10T12:00:00Z"],
    )

    @field_validator("allocation")
    @classmethod
    def validate_allocation_sum(cls, value: list[PortfolioAllocation]) -> list[PortfolioAllocation]:
        """Ensure allocation percentages sum to approximately 100."""
        if value:
            total = sum(item.percentage for item in value)
            if abs(total - Decimal("100")) > Decimal("0.1"):
                msg = f"Allocation percentages must sum to 100, got {total}"
                raise ValueError(msg)
        return value

    class Config:
        frozen = True
