"""Integration tests for market analysis API endpoint."""

import asyncio
import unittest
from decimal import Decimal

import httpx


class TestMarketAnalysisIntegration(unittest.IsolatedAsyncioTestCase):
    """Integration tests for market analysis endpoints."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test class."""
        cls.base_url = "http://localhost:8000/api/v1/market-analysis"

    async def test_a_trend_analysis_endpoint_success(self) -> None:
        """Test trend analysis endpoint returns successful response."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30) as client:
            payload = {
                "symbol": "BTC/USD",
                "timeframe": "1h",
                "historical_data_points": 100,
                "include_sentiment": True,
            }

            response = await client.post("/trend-analysis", json=payload)

            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["symbol"], "BTC/USD")
            self.assertEqual(data["status"], "completed")

    async def test_a_trend_analysis_validation_error(self) -> None:
        """Test trend analysis with invalid input returns error."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30) as client:
            payload = {
                "symbol": "",
                "timeframe": "1h",
            }

            response = await client.post("/trend-analysis", json=payload)

            self.assertEqual(response.status_code, 422)

    async def test_a_health_endpoint(self) -> None:
        """Test health endpoint returns healthy status."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10) as client:
            response = await client.get("/health")

            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "healthy")

    async def test_a_concurrent_requests(self) -> None:
        """Test handling of concurrent requests."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30) as client:
            payload = {
                "symbol": "ETH/USD",
                "timeframe": "4h",
                "historical_data_points": 50,
            }

            tasks = [
                client.post("/trend-analysis", json=payload)
                for _ in range(10)
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            successful_requests = sum(
                1 for r in results
                if isinstance(r, httpx.Response) and r.status_code == 200
            )

            self.assertGreater(successful_requests, 0)


if __name__ == "__main__":
    unittest.main()
