"""Setup configuration for VakarnoAI package."""

from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="finance-ai",
    version="1.0.0",
    author="FinanceAI Team",
    author_email="info@financeai.dev",
    description="Intelligent Financial Market Analysis Platform with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/financeai/finance-ai",
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: FastAPI",
        "Framework :: Pydantic",
        "Typing :: Typed",
    ],
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.110.0",
        "uvicorn[standard]>=0.27.1",
        "pydantic>=2.6.1",
        "pydantic-settings>=2.1.0",
        "lagom>=0.7.2",
        "strawberry-graphql[fastapi]>=0.219.2",
        "langchain>=0.1.6",
        "langgraph>=0.0.25",
        "langchain-openai>=0.0.5",
        "langchain-google-genai>=0.0.11",
        "faiss-cpu>=1.7.4",
        "psycopg2-binary>=2.9.9",
        "asyncpg>=0.29.0",
        "sqlalchemy[asyncio]>=2.0.27",
        "pymongo>=4.6.1",
        "motor>=3.3.2",
        "redis>=5.0.1",
        "httpx>=0.26.0",
        "aiohttp>=3.9.3",
        "prometheus-client>=0.19.0",
        "prometheus-fastapi-instrumentator>=6.1.0",
        "structlog>=24.1.0",
        "python-dotenv>=1.0.1",
        "pyyaml>=6.0.1",
    ],
    extras_require={
        "dev": [
            "coverage>=7.4.1",
            "unittest-xml-reporting>=3.2.0",
            "faker>=22.6.0",
            "factory-boy>=3.3.0",
            "ruff>=0.2.1",
            "mypy>=1.8.0",
            "pre-commit>=3.6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "financeai-api=finance_ai.frameworks.api.entry_point:main",
        ],
    },
    package_data={
        "finance_ai": [
            "adapters/ai_models/ai_agents/prompts/*.yaml",
            "py.typed",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
