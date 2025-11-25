"""FastAPI application entry point - Simplified version for demo."""

from datetime import datetime
from typing import Dict, Any, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from finance_ai.settings.app_settings import get_settings
    settings = get_settings()
except Exception:
    settings = None


def create_application() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        Configured FastAPI application.
    """
    app = FastAPI(
        title="FinanceAI - Intelligent Financial Analysis Platform",
        description="AI-powered financial market analysis and prediction system",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root() -> Dict[str, Any]:
        """Root endpoint with API information.

        Returns:
            API information and available endpoints.
        """
        return {
            "service": "FinanceAI",
            "version": "1.0.0",
            "description": "Intelligent Financial Market Analysis Platform",
            "status": "running",
            "timestamp": datetime.utcnow().isoformat(),
            "endpoints": {
                "health": "/health",
                "docs": "/docs",
                "demo_market_data": "/api/v1/demo/market-data",
                "demo_analysis": "/api/v1/demo/analysis",
            }
        }

    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        """Health check endpoint.

        Returns:
            Health status.
        """
        return {
            "status": "healthy",
            "service": "financeai",
            "timestamp": datetime.utcnow().isoformat(),
        }

    @app.get("/api/v1/demo/market-data")
    async def get_demo_market_data() -> Dict[str, Any]:
        """Demo endpoint showing market data structure.

        Returns:
            Sample market data in FinanceAI format.
        """
        return {
            "symbol": "AAPL",
            "timeframe": "1D",
            "data_points": [
                {
                    "timestamp": "2024-11-20T09:30:00Z",
                    "open": 189.50,
                    "high": 191.20,
                    "low": 188.80,
                    "close": 190.75,
                    "volume": 52000000
                },
                {
                    "timestamp": "2024-11-21T09:30:00Z",
                    "open": 190.80,
                    "high": 192.50,
                    "low": 190.20,
                    "close": 191.90,
                    "volume": 48000000
                },
                {
                    "timestamp": "2024-11-22T09:30:00Z",
                    "open": 192.00,
                    "high": 193.80,
                    "low": 191.50,
                    "close": 193.20,
                    "volume": 55000000
                }
            ],
            "metrics": {
                "sma_20": 191.30,
                "rsi_14": 62.5,
                "volatility": 0.018
            }
        }

    @app.get("/api/v1/demo/analysis")
    async def get_demo_analysis() -> Dict[str, Any]:
        """Demo endpoint showing AI analysis structure.

        Returns:
            Sample AI market analysis result.
        """
        return {
            "analysis_id": "demo-analysis-001",
            "symbol": "AAPL",
            "timestamp": datetime.utcnow().isoformat(),
            "trend_prediction": {
                "direction": "bullish",
                "confidence": 0.78,
                "timeframe": "short_term",
                "reasoning": [
                    "Strong upward momentum with RSI at 62.5",
                    "Price broke resistance at $191",
                    "Volume increasing on up days"
                ]
            },
            "risk_assessment": {
                "level": "moderate",
                "score": 0.45,
                "factors": [
                    "Market volatility at 1.8%",
                    "Support level at $188",
                    "No major resistance until $195"
                ]
            },
            "trading_signals": [
                {
                    "type": "buy",
                    "strength": "strong",
                    "entry_price": 193.20,
                    "target_price": 198.00,
                    "stop_loss": 189.50
                }
            ],
            "ai_insights": {
                "model": "FinanceAI Multi-Agent System",
                "agents_consulted": ["Analyst", "Predictor", "Risk Evaluator"],
                "processing_time_ms": 245
            }
        }

    @app.get("/api/v1/architecture")
    async def get_architecture_info() -> Dict[str, Any]:
        """Endpoint showing Clean Architecture implementation.

        Returns:
            Architecture information and design patterns used.
        """
        return {
            "architecture": "Clean Architecture",
            "layers": {
                "entities": {
                    "description": "Core domain models",
                    "examples": ["MarketData", "TradingSignal", "Portfolio", "RiskAssessment"],
                    "principles": ["Pure business logic", "Framework independent", "Pydantic validation"]
                },
                "use_cases": {
                    "description": "Application business rules",
                    "examples": ["MarketTrendAnalysisUseCase", "RiskAssessmentUseCase"],
                    "principles": ["Interface-based", "Single Responsibility", "Dependency Inversion"]
                },
                "adapters": {
                    "description": "External service implementations",
                    "examples": ["AIServiceAdapter (LangChain)", "FAISSAdapter", "PostgresRepository"],
                    "principles": ["Implements use case interfaces", "Framework/library specific code"]
                },
                "frameworks": {
                    "description": "I/O layer",
                    "examples": ["FastAPI REST", "GraphQL", "Event handlers"],
                    "principles": ["User interface", "External communication", "API endpoints"]
                }
            },
            "tech_stack": {
                "backend": ["Python 3.11+", "FastAPI", "Strawberry GraphQL"],
                "ai_ml": ["LangGraph", "LangChain", "OpenAI", "Gemini"],
                "databases": ["PostgreSQL", "MongoDB", "Redis"],
                "vector_db": ["FAISS"],
                "observability": ["Prometheus", "Grafana", "Structlog"]
            },
            "design_patterns": [
                "Dependency Injection (Lagom)",
                "Repository Pattern",
                "Adapter Pattern",
                "Strategy Pattern (AI agents)"
            ]
        }

    return app


app = create_application()
