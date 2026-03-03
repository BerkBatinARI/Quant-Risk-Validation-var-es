import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TICKER = "SPY"
ALPHA = 0.99  # 99% VaR


def main() -> None:
    print("RUNNING backtest_var_garch.py main()")
    os.makedirs("reports/figures", exist_ok=True)

    path = f"data/{TICKER}_garch_var.csv"
    df = pd.read_csv(path, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)

    # Keep rows where we actually have a forecast
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["log_return", "var_99_garch"]).copy()

    # One-sided 99% VaR breach: return < -VaR
    df["breach"] = df["log_return"] < (-df["var_99_garch"])

    n = int(len(df))
    breaches = int(df["breach"].sum())
    breach_rate = breaches / n if n > 0 else float("nan")

    print(f"Obs used: {n}")
    print(f"Breaches: {breaches}")
    print(f"Breach rate: {breach_rate:.4%}")

    # Plot: returns vs -VaR (so the threshold is on the same axis as returns)
    plt.figure()
    plt.plot(df["Date"], df["log_return"], label="log return")
    plt.plot(df["Date"], -df["var_99_garch"], label="-VaR(99%) GARCH")

    breach_df = df[df["breach"]]
    plt.scatter(breach_df["Date"], breach_df["log_return"], label="breaches", s=12)

    plt.title(f"{TICKER} GARCH(1,1) VaR(99%) Backtest")
    plt.xlabel("Date")
    plt.ylabel("Log return")
    plt.legend()

    fig_path = f"reports/figures/{TICKER}_var99_garch_backtest.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=200)
    plt.close()
    print(f"Saved {fig_path}")


if __name__ == "__main__":
    main()