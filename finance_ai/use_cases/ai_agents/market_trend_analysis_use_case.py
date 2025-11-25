"""Market trend analysis use case using AI agents."""

from datetime import datetime, timezone
from decimal import Decimal

from finance_ai.entities.ai_agent_models.market_trend_analysis import (
    MarketTrendAnalysisInput,
    MarketTrendAnalysisResult,
    TrendPrediction,
)
from finance_ai.entities.ai_agent_models.prompt_names import PromptNames
from finance_ai.use_cases.base_ai_agent_use_case import BaseAIAgentUseCase
from finance_ai.use_cases.interfaces.ai_service_interface import AIServiceInterface
from finance_ai.use_cases.interfaces.market_data_repository_interface import (
    MarketDataRepositoryInterface,
)
from finance_ai.use_cases.interfaces.prompt_catalog_interface import PromptCatalogInterface
from finance_ai.use_cases.interfaces.vector_store_interface import VectorStoreInterface


class MarketTrendAnalysisUseCase(BaseAIAgentUseCase):
    """Analyze market trends using AI agents and historical data."""

    def __init__(
        self,
        prompt_catalog: PromptCatalogInterface,
        ai_service: AIServiceInterface,
        market_data_repository: MarketDataRepositoryInterface,
        vector_store: VectorStoreInterface,
    ) -> None:
        """Initialize market trend analysis use case.

        Args:
            prompt_catalog: Prompt catalog for loading AI prompts.
            ai_service: AI service for agentic processing.
            market_data_repository: Repository for market data access.
            vector_store: Vector store for semantic search.
        """
        super().__init__(prompt_catalog, ai_service)
        self.prompt_name = PromptNames.MARKET_TREND_ANALYSIS
        self.market_data_repository = market_data_repository
        self.vector_store = vector_store

    async def execute(
        self,
        input_data: MarketTrendAnalysisInput,
        prompt_version: str | None = None,
    ) -> MarketTrendAnalysisResult:
        """Execute market trend analysis using AI agents.

        Args:
            input_data: Analysis input parameters.
            prompt_version: Optional specific prompt version.

        Returns:
            Trend analysis result with predictions and insights.

        Raises:
            UseCaseError: If analysis fails.
        """
        prompt_config = await self.load_prompt_config(prompt_version)
        current_price = await self._get_current_price(input_data.symbol)
        historical_context = await self._get_historical_context(input_data)
        similar_patterns = await self._find_similar_patterns(input_data.symbol)

        prompt_variables = self.build_prompt_variables(
            symbol=input_data.symbol,
            timeframe=input_data.timeframe,
            current_price=float(current_price),
            historical_context=historical_context,
            similar_patterns=similar_patterns,
            include_sentiment=input_data.include_sentiment,
        )

        ai_response = await self.ai_service.process_prompt(
            prompt_template=prompt_config["prompt"],
            input_variables=prompt_variables,
            model_config={
                "temperature": prompt_config.get("temperature", 0.3),
                "model_hint": prompt_config.get("model_hint", "gemini-2.0-flash"),
            },
        )

        return self._parse_analysis_result(
            symbol=input_data.symbol,
            current_price=current_price,
            ai_response=ai_response,
        )

    async def _get_current_price(self, symbol: str) -> Decimal:
        """Get current price for symbol from repository.

        Args:
            symbol: Trading symbol.

        Returns:
            Current price as Decimal.

        Raises:
            DataNotFoundError: If price not available.
        """
        price = await self.market_data_repository.get_latest_price(symbol)
        if price is None:
            msg = f"Price not available for symbol: {symbol}"
            raise ValueError(msg)
        return Decimal(str(price))

    async def _get_historical_context(self, input_data: MarketTrendAnalysisInput) -> dict:
        """Build historical context from market data.

        Args:
            input_data: Analysis input parameters.

        Returns:
            Historical context dictionary.
        """
        return {
            "data_points": input_data.historical_data_points,
            "timeframe": input_data.timeframe,
        }

    async def _find_similar_patterns(self, symbol: str) -> list[dict]:
        """Find similar historical patterns using vector search.

        Args:
            symbol: Trading symbol.

        Returns:
            List of similar pattern matches.
        """
        query_text = f"market trend analysis for {symbol}"
        embedding = await self.ai_service.generate_embeddings(query_text)

        similar_vectors = await self.vector_store.query_vectors(
            query_vector=embedding,
            top_k=5,
            filter_metadata={"symbol": symbol},
        )

        return [{"pattern": v.get("metadata", {})} for v in similar_vectors]

    def _parse_analysis_result(
        self,
        symbol: str,
        current_price: Decimal,
        ai_response: dict,
    ) -> MarketTrendAnalysisResult:
        """Parse AI response into structured result.

        Args:
            symbol: Trading symbol.
            current_price: Current market price.
            ai_response: Raw AI response.

        Returns:
            Structured analysis result.
        """
        prediction_data = ai_response.get("prediction", {})
        trend_prediction = TrendPrediction(
            direction=prediction_data.get("direction", "sideways"),
            confidence_score=Decimal(str(prediction_data.get("confidence", 50))),
            expected_price_target=Decimal(str(prediction_data.get("price_target", current_price))),
            time_horizon=prediction_data.get("time_horizon", "24h"),
        )

        return MarketTrendAnalysisResult(
            symbol=symbol,
            current_price=current_price,
            trend_prediction=trend_prediction,
            key_insights=ai_response.get("insights", []),
            technical_signals=ai_response.get("technical_signals", {}),
            sentiment_score=Decimal(str(ai_response.get("sentiment_score", 0)))
            if ai_response.get("sentiment_score")
            else None,
            risk_factors=ai_response.get("risk_factors", []),
            analyzed_at=datetime.now(tz=timezone.utc),
        )
