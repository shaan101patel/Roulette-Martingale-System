import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Backend logic (unchanged) ---
def simulation(bet):
    chance = 18 / 38
    win = 0
    low = 0.0
    high = 1.0

    flip = np.random.uniform(low, np.nextafter(high, np.inf))

    if flip <= chance:
        win = bet * 2

    return win


def runSim(start, mins, Enviroment):
    start = start
    currBAL = start
    currBET = 5
    numbIterations = 0

    lastWin = False

    time = 0

    while time < mins * 60:
        if lastWin == True:
            currBET = 5
        else:
            currBET = currBET * 2

        currBAL = currBAL - currBET

        if currBAL > 0:
            win = simulation(currBET)

            if win > 0:
                currBAL += win
                lastWin = True
            else:
                lastWin = False

        key = {"online": [36, 60], "quiet": [120, 180], "medium": [160, 180], "busy": [180, 300]}

        rng = np.random.default_rng()

        low = key[Enviroment][0]
        high = key[Enviroment][1]

        AvgBetTime = rng.integers(low=low, high=high)

        time += AvgBetTime
        numbIterations += 1

    return currBAL, numbIterations


def runSim_trace(start, mins, Enviroment):
    # Same logic as runSim but records per-spin state for visualization.
    start = start
    currBAL = start
    currBET = 5
    numbIterations = 0

    lastWin = False

    time = 0
    trace = []

    while time < mins * 60:
        if lastWin == True:
            currBET = 5
        else:
            currBET = currBET * 2

        currBAL = currBAL - currBET

        if currBAL > 0:
            win = simulation(currBET)

            if win > 0:
                currBAL += win
                lastWin = True
            else:
                lastWin = False

        key = {"online": [36, 60], "quiet": [120, 180], "medium": [160, 180], "busy": [180, 300]}

        rng = np.random.default_rng()

        low = key[Enviroment][0]
        high = key[Enviroment][1]

        AvgBetTime = rng.integers(low=low, high=high)

        time += AvgBetTime
        numbIterations += 1

        trace.append(
            {
                "time": time,
                "balance": currBAL,
                "bet": currBET,
                "won": lastWin,
                "iterations": numbIterations,
                "avg_bet_time": AvgBetTime,
            }
        )

    return trace, currBAL, numbIterations, time


def batch_simulate(runs, startBal, mins, env):
    finals = []
    iters = []
    for _ in range(runs):
        bal, n_iter = runSim(startBal, mins, env)
        finals.append(bal)
        iters.append(n_iter)
    finals = np.array(finals)
    iters = np.array(iters)
    return finals, iters


def summarize(finals, iters, startBal):
    series = pd.Series(finals)
    stats = {
        "runs": len(finals),
        "win_rate": (series > startBal).mean(),
        "bankrupt_rate": (series <= 0).mean(),
        "mean_final": series.mean(),
        "median_final": series.median(),
        "p10": series.quantile(0.10),
        "p90": series.quantile(0.90),
        "best": series.max(),
        "worst": series.min(),
        "avg_iters": np.mean(iters),
    }
    return stats


def plot_results(finals, iters, trace, startBal, mins, env):
    plt.style.use("seaborn-v0_8")
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # Sample path
    ax = axes[0, 0]
    times = [0] + [p["time"] for p in trace]
    balances = [startBal] + [p["balance"] for p in trace]
    ax.plot(times, balances, marker="o", linewidth=1.2, markersize=3, label="balance")
    ax.axhline(startBal, color="gray", linestyle="--", linewidth=1, label="start balance")
    ax.set_title(f"Sample run path ({env}, {mins} mins)")
    ax.set_xlabel("Simulated seconds")
    ax.set_ylabel("Balance")
    ax.legend()

    # Final balance histogram
    ax = axes[0, 1]
    ax.hist(finals, bins=40, color="#3b82f6", alpha=0.75, edgecolor="black")
    ax.axvline(startBal, color="gray", linestyle="--", linewidth=1, label="start balance")
    ax.set_title("Distribution of final balances")
    ax.set_xlabel("Final balance")
    ax.set_ylabel("Count")
    ax.legend()

    # ECDF of final balances
    ax = axes[1, 0]
    sorted_final = np.sort(finals)
    y = np.linspace(0, 1, len(sorted_final), endpoint=False)
    ax.plot(sorted_final, y, color="#10b981", linewidth=1.5)
    ax.axvline(startBal, color="gray", linestyle="--", linewidth=1, label="start balance")
    ax.set_title("ECDF of final balances")
    ax.set_xlabel("Final balance")
    ax.set_ylabel("Cumulative probability")
    ax.legend()

    # Iteration distribution summary
    ax = axes[1, 1]
    ax.hist(iters, bins=30, color="#f97316", alpha=0.75, edgecolor="black")
    ax.set_title("Spins per run")
    ax.set_xlabel("Iterations (spins)")
    ax.set_ylabel("Count")

    fig.tight_layout()
    plt.show()


def main():
    # Backtest-style defaults
    startBal = 315
    mins = 60
    env = "quiet"
    runs = 5000

    # Run a sample traced path for visualization
    trace, _, _, _ = runSim_trace(startBal, mins, env)

    finals, iters = batch_simulate(runs, startBal, mins, env)
    stats = summarize(finals, iters, startBal)

    print("Backtest summary:")
    print(f" runs: {stats['runs']}")
    print(f" win_rate: {stats['win_rate']:.3f}")
    print(f" bankrupt_rate: {stats['bankrupt_rate']:.3f}")
    print(f" mean_final: {stats['mean_final']:.2f}")
    print(f" median_final: {stats['median_final']:.2f}")
    print(f" p10_final: {stats['p10']:.2f}")
    print(f" p90_final: {stats['p90']:.2f}")
    print(f" best_final: {stats['best']:.2f}")
    print(f" worst_final: {stats['worst']:.2f}")
    print(f" avg_spins_per_run: {stats['avg_iters']:.1f}")

    plot_results(finals, iters, trace, startBal, mins, env)


if __name__ == "__main__":
    main()
