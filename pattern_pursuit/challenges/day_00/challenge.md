## Day 0: ML Baseline

### Problem Statement
Build baseline ML system to predict 5-day returns and classify into trading signals for S&P 500 stocks.

### Connection to Previous Days
Initial baseline establishment

### Features/Enhancements
* Price Features:
  - Returns (1,5,10,20 days)
  - Moving averages
  - Price momentum
* Volume Features:
  - Volume ratios
  - VWAP
* Technical Indicators:
  - RSI, MACD, BB

### Classification Framework
* Signal Categories:
  - Strong Buy (>2%)
  - Hold (-1% to 2%)
  - Strong Sell (<-1%)
* Basic confidence scoring
* Equal threshold weighting

### Model Validation
* Walk-forward validation
* Time-series CV
* Out-of-sample testing
* Feature importance stability

### Backtesting
* Transaction costs: 5bps
* T+1 execution
* Equal position sizing
* Basic portfolio rules

### Success Metrics
* Classification:
  - Overall accuracy: >52%
  - Per signal precision: >50%
  - F1 score baseline
* Trading:
  - Sharpe ratio: >0.8
  - Max drawdown: <15%

### Implementation Steps
1. Data Pipeline:
   - Data collection
   - Feature engineering
   - Preprocessing
2. Model Development:
   - ML model training
   - Classification setup
   - Initial validation
3. Trading Framework:
   - Signal generation
   - Basic backtesting
   - Performance tracking