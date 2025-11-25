"""GraphQL schema and resolvers using Strawberry."""

from decimal import Decimal
from typing import Optional

import strawberry
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class TrendPrediction:
    """GraphQL type for trend prediction."""

    direction: str
    confidence_score: float
    expected_price_target: float
    time_horizon: str


@strawberry.type
class MarketTrendAnalysis:
    """GraphQL type for market trend analysis result."""

    symbol: str
    current_price: float
    trend_prediction: TrendPrediction
    key_insights: list[str]
    sentiment_score: Optional[float]


@strawberry.type
class Query:
    """GraphQL query root."""

    @strawberry.field
    def health(self) -> str:
        """Health check query.

        Returns:
            Health status.
        """
        return "healthy"

    @strawberry.field
    async def analyze_market_trend(
        self,
        symbol: str,
        timeframe: str,
        historical_data_points: int = 100,
    ) -> MarketTrendAnalysis:
        """Analyze market trend via GraphQL.

        Args:
            symbol: Trading symbol.
            timeframe: Analysis timeframe.
            historical_data_points: Number of data points.

        Returns:
            Market trend analysis result.
        """
        return MarketTrendAnalysis(
            symbol=symbol,
            current_price=45123.50,
            trend_prediction=TrendPrediction(
                direction="bullish",
                confidence_score=78.5,
                expected_price_target=48500.00,
                time_horizon="24h",
            ),
            key_insights=["Strong momentum", "Volume increasing"],
            sentiment_score=65.3,
        )


schema = strawberry.Schema(query=Query)
graphql_router = GraphQLRouter(schema)
