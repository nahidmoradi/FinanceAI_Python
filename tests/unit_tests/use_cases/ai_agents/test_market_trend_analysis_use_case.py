"""Unit tests for MarketTrendAnalysisUseCase."""

import unittest
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

from finance_ai.entities.ai_agent_models.market_trend_analysis import (
    MarketTrendAnalysisInput,
    MarketTrendAnalysisResult,
)
from finance_ai.use_cases.ai_agents.market_trend_analysis_use_case import (
    MarketTrendAnalysisUseCase,
)


class TestMarketTrendAnalysisUseCase(unittest.IsolatedAsyncioTestCase):
    """Test suite for MarketTrendAnalysisUseCase."""

    async def asyncSetUp(self) -> None:
        """Set up test fixtures."""
        self.mock_prompt_catalog = AsyncMock()
        self.mock_ai_service = AsyncMock()
        self.mock_market_data_repo = AsyncMock()
        self.mock_vector_store = AsyncMock()

        self.use_case = MarketTrendAnalysisUseCase(
            prompt_catalog=self.mock_prompt_catalog,
            ai_service=self.mock_ai_service,
            market_data_repository=self.mock_market_data_repo,
            vector_store=self.mock_vector_store,
        )

    async def test_a_execute_returns_valid_result(self) -> None:
        """Test execute returns valid MarketTrendAnalysisResult."""
        input_data = MarketTrendAnalysisInput(
            symbol="BTC/USD",
            timeframe="1h",
            historical_data_points=100,
            include_sentiment=True,
        )

        self.mock_prompt_catalog.get_prompt.return_value = {
            "prompt": "Analyze {symbol}",
            "temperature": 0.3,
            "model_hint": "gemini-2.0-flash-exp",
        }

        self.mock_market_data_repo.get_latest_price.return_value = 45123.50

        self.mock_ai_service.generate_embeddings.return_value = [0.1] * 1536

        self.mock_vector_store.query_vectors.return_value = []

        self.mock_ai_service.process_prompt.return_value = {
            "prediction": {
                "direction": "bullish",
                "confidence": 78.5,
                "price_target": 48500.00,
                "time_horizon": "24h",
            },
            "insights": ["Strong momentum", "Volume increasing"],
            "technical_signals": {"rsi": "oversold", "macd": "bullish"},
            "sentiment_score": 65.3,
            "risk_factors": ["High volatility"],
        }

        result = await self.use_case.execute(input_data)

        self.assertIsInstance(result, MarketTrendAnalysisResult)
        self.assertEqual(result.symbol, "BTC/USD")
        self.assertEqual(result.current_price, Decimal("45123.50"))
        self.assertEqual(result.trend_prediction.direction, "bullish")
        self.assertGreater(len(result.key_insights), 0)

    async def test_a_execute_raises_on_missing_price(self) -> None:
        """Test execute raises ValueError when price not available."""
        input_data = MarketTrendAnalysisInput(
            symbol="INVALID/SYMBOL",
            timeframe="1h",
            historical_data_points=100,
        )

        self.mock_prompt_catalog.get_prompt.return_value = {"prompt": "test"}
        self.mock_market_data_repo.get_latest_price.return_value = None

        with self.assertRaises(ValueError) as context:
            await self.use_case.execute(input_data)

        self.assertIn("Price not available", str(context.exception))

    async def test_a_load_prompt_config_calls_catalog(self) -> None:
        """Test load_prompt_config retrieves prompt from catalog."""
        expected_config = {
            "prompt": "Test prompt",
            "temperature": 0.3,
        }

        self.mock_prompt_catalog.get_prompt.return_value = expected_config

        result = await self.use_case.load_prompt_config()

        self.assertEqual(result, expected_config)
        self.mock_prompt_catalog.get_prompt.assert_called_once()


if __name__ == "__main__":
    unittest.main()
