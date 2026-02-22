# Roulette Martingale System

## Overview
Simple American roulette Martingale simulator. Core logic lives in the notebook (`Roulette-R1.ipynb`) and is reused by the visualizers and batch tools without modification.

## Files
- `Roulette-R1.ipynb` — original logic and quick experiments.
- `visualizer.py` — pygame animation of live runs.
- `visualizer_v2.py` — backtesting view with plots and stats.
- `collect_runs.py` — batch runner that saves many simulations to `runs.csv`.
- `analyze_runs.py` — pandas/matplotlib analysis of `runs.csv` (plots to `reports/`).

## Setup
1) Activate venv (already present):
	 - Windows PowerShell: `C:/Users/shaan/Documents/Roulette/Roulette-Martingale-System/.venv/Scripts/Activate.ps1`
2) Install deps if needed: `pip install numpy pandas matplotlib pygame`

## Usage
- Animated visualizer: `python visualizer.py`
- Backtest view (plots + stats): `python visualizer_v2.py`
- Collect CSV for bulk analysis: `python collect_runs.py`
	- Outputs `runs.csv` with run_id, env, start_balance, final_balance, iterations, sim_seconds, mins_target, won, bankrupt.
- Analyze CSV and save plots: `python analyze_runs.py`
	- Saves charts to `reports/` (`final_balance_hist.png`, `final_balance_ecdf.png`, `iterations_hist.png`).

## Parameters to tweak
- Starting bankroll: `startBal` (defaults vary by script).
- Session length: `mins` (simulated minutes per run).
- Environment tempo: `env` in {`online`, `quiet`, `medium`, `busy`} controlling spin interval ranges.
- Number of runs: `runs` in the batch scripts/visualizers.

## Notes
- Backend betting logic is identical across tools: base bet 5, reset to base after any win, double after each loss, win prob 18/38, no stop-loss/stop-win.
- Visualizer `visualizer.py` is sped up (higher frame cadence) for quicker playback; logic unchanged.