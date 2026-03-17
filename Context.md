# Portfolio Dashboard — Project Context

## What This Is
A Streamlit-based interactive portfolio dashboard built in Python.
Designed to demonstrate practical knowledge of statistics, portfolio
construction, optimization, and Monte Carlo modeling for a finance
job application.

## Tech Stack
- Streamlit — app framework
- yfinance — price and fundamental data from Yahoo Finance
- pandas / numpy — data manipulation and math
- scipy — optimization
- plotly — interactive charts

## App Structure
- app.py — single file containing the entire app
- Five tabs: Overview, Optimization, Monte Carlo, Risk Metrics, Fundamentals

## Tab Summary
1. Overview — normalized price chart with SPY benchmark overlay,
   return/volatility table, correlation heatmap
2. Optimization — efficient frontier (3,000 simulations), max-Sharpe
   and min-volatility portfolios side by side
3. Monte Carlo — 1,000 simulation fan chart, goal probability metric,
   outcome distribution histogram
4. Risk Metrics — Sharpe, Sortino, VaR, CVaR, max drawdown,
   rolling Sharpe chart
5. Fundamentals — key stats table, sector breakdown pie + bar chart,
   allocation vs valuation bubble chart

## Known Issues / Quirks
- yfinance returns a DataFrame for single tickers (SPY) so we use
  isinstance check and iloc[:,0] to extract the series
- Dividend yield from Yahoo Finance comes pre-scaled, no *100 needed
- Crypto tickers work using format BTC-USD, ETH-USD but show N/A
  for fundamentals

## Sidebar Inputs
- Tickers (comma separated)
- Start / end date
- Initial investment
- Monte Carlo horizon (years)
- Goal target value ($)