import os
import numpy as np
import pandas as pd
from arch import arch_model

TICKER = "SPY"
ALPHA = 0.99
WINDOW_MIN = 500  # start GARCH after enough history
Z_99 = 2.326347874  # Normal 99% quantile (one-sided)

def main() -> None:
    print("RUNNING risk_garch.py main()")
    os.makedirs("data", exist_ok=True)

    df = pd.read_csv("data/returns.csv", parse_dates=["Date"])
    df = df[df["ticker"] == TICKER].sort_values("Date").reset_index(drop=True)

    # keep only finite returns (GARCH can't handle NaN/inf)
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["log_return"]).copy()
    df = df.reset_index(drop=True)

    # Use percent returns for GARCH stability
    r = (df["log_return"] * 100.0).to_numpy(dtype=float)

    sigma = np.full_like(r, np.nan, dtype=float)

    # Walk-forward: refit on an expanding window
    for t in range(WINDOW_MIN, len(r)):
        train = r[:t]
        am = arch_model(train, vol="Garch", p=1, q=1, dist="normal", mean="zero")
        res = am.fit(disp="off")
        f = res.forecast(horizon=1, reindex=False)

        var1 = float(f.variance.values[-1, 0])  # %^2
        sigma[t] = np.sqrt(var1) / 100.0        # back to log-return units

        if t % 250 == 0:
            print(f"Fitted up to t={t}/{len(r)}")

    var_99 = Z_99 * sigma

    out = df[["Date", "ticker", "log_return"]].copy()
    out["garch_sigma"] = sigma
    out["var_99_garch"] = var_99

    out_path = f"data/{TICKER}_garch_var.csv"
    out.to_csv(out_path, index=False)
    print(f"Saved {out_path} ({len(out)} rows)")

if __name__ == "__main__":
    main()