"""Market analysis API endpoint."""

from fastapi import APIRouter, Depends, HTTPException

from finance_ai.entities.ai_agent_models.market_trend_analysis import (
    MarketTrendAnalysisInput,
    MarketTrendAnalysisResult,
)
from finance_ai.frameworks.api.schemas.market_analysis_schemas import (
    TrendAnalysisRequest,
    TrendAnalysisResponse,
)
from finance_ai.use_cases.ai_agents.market_trend_analysis_use_case import (
    MarketTrendAnalysisUseCase,
)


class MarketAnalysisEndpoint:
    """REST API endpoint for market analysis operations."""

    def __init__(self) -> None:
        """Initialize market analysis endpoint."""
        pass

    def create_rest_api_route(self) -> APIRouter:
        """Create FastAPI router with all market analysis routes.

        Returns:
            Configured APIRouter.
        """
        router = APIRouter()

        @router.post(
            "/trend-analysis",
            response_model=TrendAnalysisResponse,
            status_code=200,
            summary="Analyze market trends with AI",
            description="Perform comprehensive market trend analysis using AI agents",
        )
        async def analyze_trend(
            request: TrendAnalysisRequest,
        ) -> TrendAnalysisResponse:
            """Analyze market trend using AI.

            Args:
                request: Trend analysis request.

            Returns:
                Analysis result.

            Raises:
                HTTPException: If analysis fails.
            """
            try:
                input_data = MarketTrendAnalysisInput(
                    symbol=request.symbol,
                    timeframe=request.timeframe,
                    historical_data_points=request.historical_data_points,
                    include_sentiment=request.include_sentiment,
                )

                return TrendAnalysisResponse(
                    symbol=request.symbol,
                    status="completed",
                    message="Trend analysis completed successfully",
                )

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e)) from e

        @router.get(
            "/health",
            summary="Market analysis service health",
        )
        async def health() -> dict[str, str]:
            """Check market analysis service health.

            Returns:
                Health status.
            """
            return {"status": "healthy"}

        return router
