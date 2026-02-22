import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

plt.style.use("seaborn-v0_8")


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df


def summarize(df):
    stats = {
        "runs": len(df),
        "win_rate": (df["final_balance"] > df["start_balance"]).mean(),
        "bankrupt_rate": (df["final_balance"] <= 0).mean(),
        "mean_final": df["final_balance"].mean(),
        "median_final": df["final_balance"].median(),
        "p10": df["final_balance"].quantile(0.10),
        "p90": df["final_balance"].quantile(0.90),
        "best": df["final_balance"].max(),
        "worst": df["final_balance"].min(),
        "avg_iters": df["iterations"].mean(),
    }
    return stats


def plot_final_balance(df, startBal, outdir):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df["final_balance"], bins=40, color="#3b82f6", alpha=0.75, edgecolor="black")
    ax.axvline(startBal, color="gray", linestyle="--", linewidth=1, label="start balance")
    ax.set_title("Distribution of final balances")
    ax.set_xlabel("Final balance")
    ax.set_ylabel("Count")
    ax.legend()
    out_path = outdir / "final_balance_hist.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_ecdf(df, startBal, outdir):
    fig, ax = plt.subplots(figsize=(7, 4))
    sorted_final = np.sort(df["final_balance"].values)
    y = np.linspace(0, 1, len(sorted_final), endpoint=False)
    ax.plot(sorted_final, y, color="#10b981", linewidth=1.5)
    ax.axvline(startBal, color="gray", linestyle="--", linewidth=1, label="start balance")
    ax.set_title("ECDF of final balances")
    ax.set_xlabel("Final balance")
    ax.set_ylabel("Cumulative probability")
    ax.legend()
    out_path = outdir / "final_balance_ecdf.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_iterations(df, outdir):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df["iterations"], bins=30, color="#f97316", alpha=0.75, edgecolor="black")
    ax.set_title("Spins per run")
    ax.set_xlabel("Iterations (spins)")
    ax.set_ylabel("Count")
    out_path = outdir / "iterations_hist.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def main():
    csv_path = Path("runs.csv")
    if not csv_path.exists():
        raise SystemExit("runs.csv not found; run collect_runs.py first.")

    df = load_data(csv_path)
    startBal = df["start_balance"].iloc[0]
    outdir = Path("reports")
    outdir.mkdir(parents=True, exist_ok=True)

    stats = summarize(df)
    print("Summary:")
    for k, v in stats.items():
        if isinstance(v, float):
            print(f" {k}: {v:.4f}")
        else:
            print(f" {k}: {v}")

    plot_final_balance(df, startBal, outdir)
    plot_ecdf(df, startBal, outdir)
    plot_iterations(df, outdir)


if __name__ == "__main__":
    main()
