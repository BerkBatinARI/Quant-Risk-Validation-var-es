import os
import pandas as pd
import matplotlib.pyplot as plt

TICKER = "SPY"

def main() -> None:
    os.makedirs("reports/figures", exist_ok=True)

    # Normal EWMA VaR
    df = pd.read_csv(f"data/{TICKER}_ewma_var_es.csv", parse_dates=["Date"])
    df = df.dropna(subset=["var_99", "log_return"]).copy()

    df["loss"] = -df["log_return"]
    df["breach"] = df["loss"] > df["var_99"]

    # Plot last ~6 years of breaches as vertical markers
    view = df.tail(1500).copy()

    fig, ax = plt.subplots()
    ax.plot(view["Date"], view["loss"], label="1-day loss (-log return)")
    ax.plot(view["Date"], view["var_99"], label="VaR 99% (EWMA, Normal)")

    breach_points = view[view["breach"]]
    ax.scatter(breach_points["Date"], breach_points["loss"], label="VaR breach", marker="x")

    ax.set_title(f"{TICKER} — VaR breaches (last 1500 trading days)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.legend()
    fig.tight_layout()

    out_path = f"reports/figures/{TICKER}_var99_breaches.png"
    fig.savefig(out_path, dpi=160)
    print(f"Saved {out_path} (breaches shown as x markers)")

if __name__ == "__main__":
    main()