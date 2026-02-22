import csv
import numpy as np
from pathlib import Path

# --- Backend logic (copied; unchanged rules) ---
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


# Same logic as runSim, but returns simulated time as well for logging.
def runSim_with_time(start, mins, Enviroment):
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

    return currBAL, numbIterations, time


def collect_runs(runs=5000, startBal=315, mins=60, env="quiet", out_path="runs.csv"):
    rows = []
    for idx in range(1, runs + 1):
        final_bal, iterations, sim_time = runSim_with_time(startBal, mins, env)
        rows.append(
            {
                "run_id": idx,
                "env": env,
                "start_balance": startBal,
                "final_balance": final_bal,
                "iterations": iterations,
                "sim_seconds": sim_time,
                "mins_target": mins,
                "won": int(final_bal > startBal),
                "bankrupt": int(final_bal <= 0),
            }
        )
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_id",
                "env",
                "start_balance",
                "final_balance",
                "iterations",
                "sim_seconds",
                "mins_target",
                "won",
                "bankrupt",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} runs to {path}")


def main():
    collect_runs(
        runs=5000,
        startBal=315,
        mins=60,
        env="quiet",
        out_path="runs.csv",
    )


if __name__ == "__main__":
    main()
