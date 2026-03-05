import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TICKER = "SPY"
ALPHA = 0.99  # 99% VaR


def main() -> None:
    print("RUNNING backtest_var.py main()")
    os.makedirs("reports/figures", exist_ok=True)

    path = f"data/{TICKER}_ewma_var_es.csv"
    df = pd.read_csv(path, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)

    # Keep rows where we actually have a VaR estimate
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["log_return", "var_99"]).copy()

    # One-sided 99% VaR breach: return < -VaR
    df["breach"] = df["log_return"] < (-df["var_99"])

    n = int(len(df))
    breaches = int(df["breach"].sum())
    breach_rate = breaches / n if n > 0 else float("nan")

    print(f"Obs: {n}")
    print(f"VaR(99%) breaches: {breaches} ({breach_rate:.3%})  | expected ~{(1-ALPHA):.3%}")

    # Plot: returns vs -VaR (threshold on same axis as returns)
    plt.figure()
    plt.plot(df["Date"], df["log_return"], label="log return")
    plt.plot(df["Date"], -df["var_99"], label="-VaR(99%) EWMA")

    breach_df = df[df["breach"]]
    plt.scatter(breach_df["Date"], breach_df["log_return"], label="breaches", s=12)

    plt.title(f"{TICKER} EWMA VaR(99%) Backtest")
    plt.xlabel("Date")
    plt.ylabel("Log return")
    plt.legend()

    fig_path = f"reports/figures/{TICKER}_var99_backtest.png"
    plt.tight_layout()
    plt.savefig(fig_path, dpi=200)
    plt.close()
    print(f"Saved {fig_path}")


if __name__ == "__main__":
    main()