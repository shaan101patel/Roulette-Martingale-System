import pygame
import numpy as np

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


# Stepwise version for visualization; logic matches runSim but yields after each bet.
def runSim_stepwise(start, mins, Enviroment):
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

        yield {
            "time": time,
            "balance": currBAL,
            "bet": currBET,
            "won": lastWin,
            "iterations": numbIterations,
            "avg_bet_time": AvgBetTime,
        }


class MartingaleVisualizer:
    def __init__(self, runs=100, startBal=315, mins=60, env="quiet"):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 620))
        pygame.display.set_caption("Roulette Martingale Visualizer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.font_big = pygame.font.SysFont("consolas", 32)

        self.runs = runs
        self.startBal = startBal
        self.mins = mins
        self.env = env

        self.bg_color = (18, 18, 30)
        self.panel_color = (32, 34, 60)
        self.accent_win = (46, 204, 113)
        self.accent_loss = (231, 76, 60)
        self.accent_neutral = (52, 152, 219)

    def draw_text(self, text, pos, color=(230, 230, 230), big=False):
        font = self.font_big if big else self.font
        surface = font.render(text, True, color)
        self.screen.blit(surface, pos)

    def render_step(self, run_idx, total_runs, state, final=False, wins_so_far=0):
        self.screen.fill(self.bg_color)

        pygame.draw.rect(self.screen, self.panel_color, (20, 20, 960, 200), border_radius=8)
        pygame.draw.rect(self.screen, self.panel_color, (20, 240, 960, 360), border_radius=8)

        header = f"Run {run_idx} / {total_runs} | Env: {self.env}"
        self.draw_text(header, (32, 32), self.accent_neutral, big=True)

        balance_color = self.accent_win if state["balance"] > self.startBal else self.accent_loss
        self.draw_text(f"Balance: ${state['balance']:.2f}", (32, 80), balance_color, big=True)
        self.draw_text(f"Current Bet: ${state['bet']}", (32, 120))
        self.draw_text(f"Last Outcome: {'Win' if state['won'] else 'Loss'}", (32, 150), self.accent_win if state["won"] else self.accent_loss)

        self.draw_text(f"Bets this run: {state['iterations']}", (420, 80))
        self.draw_text(f"Elapsed table time (s): {state['time']}", (420, 110))
        self.draw_text(f"Avg spin wait (s): {state['avg_bet_time']}", (420, 140))
        self.draw_text(f"Wins so far: {wins_so_far}", (420, 170))

        progress = min(state["time"] / (self.mins * 60), 1.0)
        pygame.draw.rect(self.screen, (70, 70, 90), (32, 190, 916, 14), border_radius=6)
        pygame.draw.rect(self.screen, self.accent_neutral, (32, 190, int(916 * progress), 14), border_radius=6)

        pygame.draw.rect(self.screen, (26, 26, 40), (40, 270, 920, 300), border_radius=8)
        center_x = 500
        center_y = 420
        radius = 130
        pygame.draw.circle(self.screen, (60, 63, 90), (center_x, center_y), radius)
        pygame.draw.circle(self.screen, (30, 30, 45), (center_x, center_y), radius - 20)

        wedge_color = self.accent_win if state["won"] else self.accent_loss
        pygame.draw.circle(self.screen, wedge_color, (center_x, center_y), 18)

        self.draw_text("Spin Result", (center_x - 70, center_y + radius + 10))

        if final:
            banner_color = balance_color if state["balance"] >= self.startBal else self.accent_loss
            pygame.draw.rect(self.screen, banner_color, (680, 300, 240, 60), border_radius=10)
            result_text = "Run Up" if state["balance"] >= self.startBal else "Run Down"
            self.draw_text(result_text, (700, 315), (12, 12, 18), big=True)

        pygame.display.flip()

    def run(self):
        wins = 0
        for idx in range(1, self.runs + 1):
            last_state = None
            for state in runSim_stepwise(self.startBal, self.mins, self.env):
                last_state = state
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                self.render_step(idx, self.runs, state, final=False, wins_so_far=wins)
                self.clock.tick(64)  # 8x faster frame cadence during spins

            if last_state is None:
                last_state = {
                    "time": 0,
                    "balance": self.startBal,
                    "bet": 0,
                    "won": False,
                    "iterations": 0,
                    "avg_bet_time": 0,
                }

            # Per-run console log for quick tracking alongside the GUI.
            outcome = "WIN" if last_state["balance"] > self.startBal else "LOSS"
            print(
                f"Run {idx}/{self.runs} | outcome={outcome} | final_balance=${last_state['balance']:.2f} | "
                f"bets={last_state['iterations']} | elapsed_s={last_state['time']} | wins_so_far={wins}"
            )

            if last_state["balance"] > self.startBal:
                wins += 1

            for _ in range(18):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                self.render_step(idx, self.runs, last_state, final=True, wins_so_far=wins)
                self.clock.tick(96)  # 8x faster banner display cadence

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            end_state = {
                "time": self.mins * 60,
                "balance": last_state["balance"],
                "bet": last_state["bet"],
                "won": last_state["won"],
                "iterations": last_state["iterations"],
                "avg_bet_time": last_state["avg_bet_time"],
            }
            self.render_step(self.runs, self.runs, end_state, final=True, wins_so_far=wins)
            self.draw_text("Close window to exit", (32, 570), (180, 180, 180))
            self.clock.tick(10)


def main():
    viz = MartingaleVisualizer(runs=100, startBal=315, mins=60, env="quiet")
    viz.run()


if __name__ == "__main__":
    main()
