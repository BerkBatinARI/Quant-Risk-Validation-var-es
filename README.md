# Time Series Risk Engine (Volatility → VaR/ES)

> Work in progress — I’m building this incrementally and checking everything with walk-forward tests.  
> Last updated: 2026-03-02

This repo is a small risk engine that turns a volatility forecast into 1-day **VaR** / **Expected Shortfall (ES)** estimates, then checks whether those risk numbers actually hold up in a simple backtest.

The goal is not “one perfect model”, but a clean comparison of sensible baselines (EWMA, GARCH, different return distributions) with transparent evaluation.

## Results so far (SPY, 1-day 99% VaR)

- **EWMA + Normal VaR** breaches: **2.36%** (expected ~1.00%) → underestimates tail risk.
- **EWMA + Student-t (df=6) VaR** breaches: **1.77%** → improved, still higher than expected.
- Kupiec unconditional coverage test (df=1):  
  - EWMA + Normal: **LR = 70.80** (rejects correct 99% coverage)  
  - EWMA + Student-t: **LR = 25.48** (still rejects, but closer)

### Diagnostics plots
The plots below show the EWMA Normal-VaR threshold against realised 1-day losses, and highlight when the model is breached (loss exceeds VaR).

#### VaR backtest (EWMA, 99%)
![SPY VaR backtest](reports/figures/SPY_var99_backtest.png)

#### Breach timeline (EWMA, 99%)
Markers indicate VaR exceptions (days where realised loss exceeds the predicted 99% VaR threshold).
![SPY VaR breaches](reports/figures/SPY_var99_breaches.png)