"""Script to populate FAISS vector store with historical market analysis data.

This script demonstrates how to:
1. Load historical market analysis data
2. Generate embeddings using OpenAI
3. Store vectors in FAISS for similarity search
"""

import asyncio
from datetime import datetime
from decimal import Decimal

from finance_ai.adapters.ai_models.ai_service_adapter import AIServiceAdapter
from finance_ai.adapters.vector_stores.faiss_adapter import FAISSVectorStoreAdapter
from finance_ai.settings.app_settings import get_settings


# Sample historical data (in production, this should come from database)
HISTORICAL_ANALYSES = [
    {
        "id": "btc_analysis_20240110",
        "symbol": "BTC/USD",
        "date": "2024-01-10",
        "analysis_text": """
        BTC/USD Technical Analysis - January 10, 2024
        
        Price Action:
        - Current Price: $44,235
        - Strong breakout above $44,000 resistance
        - Higher highs and higher lows pattern
        
        Technical Indicators:
        - RSI: 72.3 (overbought but strong momentum)
        - MACD: Bullish crossover confirmed
        - Volume: 150% increase from average
        - Moving Averages: Price above 50-day and 200-day MA
        
        Market Sentiment:
        - Positive news about Bitcoin ETF approval
        - Institutional buying pressure
        - Fear & Greed Index: 78 (Extreme Greed)
        
        Pattern Recognition:
        - Bull flag formation completed
        - Target: $48,000 within 48 hours
        
        Outcome: Price reached $48,200 in 43 hours (Target achieved)
        """,
        "metadata": {
            "symbol": "BTC/USD",
            "date": "2024-01-10",
            "price_start": 44235.0,
            "price_end": 48200.0,
            "timeframe": "1h",
            "outcome": "bullish",
            "accuracy": 95.0,
            "rsi": 72.3,
            "volume_change": 150.0,
        },
    },
    {
        "id": "btc_analysis_20240215",
        "symbol": "BTC/USD",
        "date": "2024-02-15",
        "analysis_text": """
        BTC/USD Technical Analysis - February 15, 2024
        
        Price Action:
        - Current Price: $46,890
        - Double top formation at $47,000
        - Rejection at resistance level
        
        Technical Indicators:
        - RSI: 68.5 (near overbought, losing momentum)
        - MACD: Bearish divergence forming
        - Volume: Decreasing on upswings
        - Moving Averages: Price struggling to stay above 50-day MA
        
        Market Sentiment:
        - Profit-taking by short-term traders
        - Whale wallets moving BTC to exchanges (sell signal)
        - Fear & Greed Index: 45 (Neutral turning to Fear)
        
        Pattern Recognition:
        - Head and shoulders pattern developing
        - Target: $42,000 within 24-36 hours
        
        Outcome: Price dropped to $41,800 in 28 hours (Target achieved)
        """,
        "metadata": {
            "symbol": "BTC/USD",
            "date": "2024-02-15",
            "price_start": 46890.0,
            "price_end": 41800.0,
            "timeframe": "1h",
            "outcome": "bearish",
            "accuracy": 92.0,
            "rsi": 68.5,
            "volume_change": -30.0,
        },
    },
    {
        "id": "btc_analysis_20240320",
        "symbol": "BTC/USD",
        "date": "2024-03-20",
        "analysis_text": """
        BTC/USD Technical Analysis - March 20, 2024
        
        Price Action:
        - Current Price: $45,120
        - Consolidation phase between $44,800 - $45,400
        - Low volatility sideways movement
        
        Technical Indicators:
        - RSI: 52.1 (neutral territory)
        - MACD: Flat, no clear direction
        - Volume: Below average (30% lower than normal)
        - Moving Averages: Price between 50-day and 200-day MA
        
        Market Sentiment:
        - Uncertainty about Fed interest rate decision
        - Mixed signals from institutional investors
        - Fear & Greed Index: 50 (Neutral)
        
        Pattern Recognition:
        - Symmetrical triangle pattern
        - Waiting for breakout (direction unclear)
        - Low conviction from both bulls and bears
        
        Outcome: Price stayed in range $44,900-$45,300 for 72 hours (Sideways confirmed)
        """,
        "metadata": {
            "symbol": "BTC/USD",
            "date": "2024-03-20",
            "price_start": 45120.0,
            "price_end": 45180.0,
            "timeframe": "1h",
            "outcome": "sideways",
            "accuracy": 88.0,
            "rsi": 52.1,
            "volume_change": -30.0,
        },
    },
    {
        "id": "eth_analysis_20240405",
        "symbol": "ETH/USD",
        "date": "2024-04-05",
        "analysis_text": """
        ETH/USD Technical Analysis - April 5, 2024
        
        Price Action:
        - Current Price: $3,245
        - Strong upward momentum after Ethereum upgrade
        - Breaking multiple resistance levels
        
        Technical Indicators:
        - RSI: 78.9 (extremely overbought)
        - MACD: Strong bullish signal
        - Volume: 200% above average
        - Moving Averages: Golden cross (50-day crossed above 200-day)
        
        Market Sentiment:
        - Ethereum Shanghai upgrade successful
        - Staking yields attracting institutional money
        - Fear & Greed Index: 82 (Extreme Greed)
        
        Pattern Recognition:
        - Ascending channel with higher lows
        - Target: $3,600 within 36 hours
        
        Outcome: Price reached $3,580 in 32 hours (Target achieved)
        """,
        "metadata": {
            "symbol": "ETH/USD",
            "date": "2024-04-05",
            "price_start": 3245.0,
            "price_end": 3580.0,
            "timeframe": "1h",
            "outcome": "bullish",
            "accuracy": 94.0,
            "rsi": 78.9,
            "volume_change": 200.0,
        },
    },
    {
        "id": "btc_analysis_20240512",
        "symbol": "BTC/USD",
        "date": "2024-05-12",
        "analysis_text": """
        BTC/USD Technical Analysis - May 12, 2024
        
        Price Action:
        - Current Price: $43,650
        - Testing support at $43,500
        - Lower highs pattern forming
        
        Technical Indicators:
        - RSI: 35.2 (oversold)
        - MACD: Bearish crossover
        - Volume: Selling volume increasing
        - Moving Averages: Death cross forming (50-day crossing below 200-day)
        
        Market Sentiment:
        - FUD about regulatory crackdown
        - Major exchange facing liquidity issues
        - Fear & Greed Index: 22 (Extreme Fear)
        
        Pattern Recognition:
        - Descending triangle pattern (bearish)
        - Target: $40,000 if support breaks
        
        Outcome: Price crashed to $39,800 in 18 hours (Support failed, target exceeded)
        """,
        "metadata": {
            "symbol": "BTC/USD",
            "date": "2024-05-12",
            "price_start": 43650.0,
            "price_end": 39800.0,
            "timeframe": "1h",
            "outcome": "bearish",
            "accuracy": 96.0,
            "rsi": 35.2,
            "volume_change": 180.0,
        },
    },
]


async def train_vector_store():
    """Populate FAISS vector store with historical analysis data."""
    settings = get_settings()
    
    # Initialize adapters
    ai_service = AIServiceAdapter(
        openai_api_key=settings.openai_api_key,
        gemini_api_key=settings.gemini_api_key,
    )
    
    faiss_adapter = FAISSVectorStoreAdapter(
        index_path=settings.faiss_index_path,
        dimension=settings.faiss_dimension,
        index_type=settings.faiss_index_type,
    )
    
    print("🚀 Starting FAISS Vector Store Training...")
    print(f"📂 Index Path: {settings.faiss_index_path}")
    print(f"📊 Dimension: {settings.faiss_dimension}")
    print(f"🔧 Index Type: {settings.faiss_index_type}\n")
    
    vectors_to_upsert = []
    
    for idx, analysis in enumerate(HISTORICAL_ANALYSES, 1):
        print(f"[{idx}/{len(HISTORICAL_ANALYSES)}] Processing: {analysis['id']}")
        print(f"   Symbol: {analysis['metadata']['symbol']}")
        print(f"   Date: {analysis['metadata']['date']}")
        print(f"   Outcome: {analysis['metadata']['outcome']}")
        
        try:
            # Generate embedding for the analysis text
            print(f"   ⚙️  Generating embedding...")
            embedding = await ai_service.generate_embeddings(analysis["analysis_text"])
            
            print(f"   ✅ Embedding generated: {len(embedding)} dimensions")
            
            # Prepare vector for upsert
            vectors_to_upsert.append({
                "id": analysis["id"],
                "values": embedding,
                "metadata": analysis["metadata"],
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
        
        print()
    
    # Upsert all vectors to FAISS
    if vectors_to_upsert:
        print(f"💾 Upserting {len(vectors_to_upsert)} vectors to FAISS...")
        result = await faiss_adapter.upsert_vectors(vectors_to_upsert)
        print(f"✅ Successfully upserted {result['upserted_count']} vectors")
    else:
        print("⚠️  No vectors to upsert")
    
    print("\n" + "="*60)
    print("🎉 Training Complete!")
    print("="*60)
    
    # Test similarity search
    print("\n📊 Testing Similarity Search...")
    print("-" * 60)
    
    test_query = """
    BTC/USD current situation:
    - Price: $45,123
    - RSI: 68.3 (near overbought)
    - Volume: Significant increase (140% from average)
    - Breaking resistance at $44,000
    - Bullish momentum detected
    """
    
    print("Test Query:")
    print(test_query)
    print()
    
    query_embedding = await ai_service.generate_embeddings(test_query)
    similar_patterns = await faiss_adapter.query_vectors(
        query_vector=query_embedding,
        top_k=3,
    )
    
    print(f"Found {len(similar_patterns)} similar patterns:\n")
    
    for i, pattern in enumerate(similar_patterns, 1):
        print(f"{i}. ID: {pattern['id']}")
        print(f"   Similarity Score: {pattern['score']:.4f}")
        print(f"   Symbol: {pattern['metadata']['symbol']}")
        print(f"   Date: {pattern['metadata']['date']}")
        print(f"   Outcome: {pattern['metadata']['outcome']}")
        print(f"   Price: ${pattern['metadata']['price_start']:.2f} → ${pattern['metadata']['price_end']:.2f}")
        print(f"   Accuracy: {pattern['metadata']['accuracy']:.1f}%")
        print()
    
    print("="*60)
    print("✅ All Done! FAISS vector store is ready to use.")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(train_vector_store())
