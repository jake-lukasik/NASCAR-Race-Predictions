import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import pandas as pd
import numpy as np

# -- UTILITY PARMS -- #
TRACK_CSV_LINKS = {
    "Pocono": "https://raw.githubusercontent.com/jake-lukasik/NASCAR-Race-Predictions/refs/heads/main/Data/Pocono-2025/pocono-sim-ready-data.csv",
    "Dover": "https://raw.githubusercontent.com/jake-lukasik/NASCAR-Race-Predictions/refs/heads/main/Data/Dover-2025/dover-sim-ready-data.csv",
    "Indy": "https://raw.githubusercontent.com/jake-lukasik/NASCAR-Race-Predictions/refs/heads/main/Data/Indy-2025/indy-sim-ready-data.csv",
    "Iowa": "https://raw.githubusercontent.com/jake-lukasik/NASCAR-Race-Predictions/refs/heads/main/Data/Iowa-2025/iowa-sim-ready-data.csv"
}

# -- SIMULATION FUNCTIONS -- #
# existing simulation functions from before
def simulate_race(df, track_stat_wgt, season_stat_wgt):
    finish_positions = []
    for _, row in df.iterrows():
        # calculate a performance bonus to add a weight to drivers who have performed well
        # at track in categories other than avg. finish
        performance_bonus_scale = 0.5  # increase effect of bonuses

        track_bonus = (
            0.3 * row['Wins'] +
            0.15 * row['track_Laps Led Per Race'] +
            0.1 * row['Avg Rating'] +
            0.1 * row["Top 5's"]
        )

        season_bonus = (
            0.3 * row['szn_Wins'] +
            0.15 * row['szn_Laps Led Per Race'] +
            0.1 * row['szn_Avg Rating'] +
            0.1 * row["szn_Top 5's"]
        )

        # weighted performance bonus
        performance_bonus = track_stat_wgt * track_bonus + season_stat_wgt * season_bonus


        # apply bonus: decrease average finish (but not below 1)
        adjusted_avg_finish = max(
        1,
        (
            track_stat_wgt * row['Avg Finish'] +
            season_stat_wgt * row['szn_Avg Finish']
        ) - performance_bonus * performance_bonus_scale
        )

        # quick check for a DNF
        dnf = np.random.poisson(row['DNF_Prob']) >= 1

        # mod finish position based on events
        if dnf:
            finish_pos = np.random.randint(len(df) + 1, len(df) + 6)
        else:
            finish_pos = np.random.normal(loc=adjusted_avg_finish, scale=row['Std Dev'])
            finish_pos = max(1, min(len(df), finish_pos))
        finish_positions.append((row['Driver'], finish_pos, dnf))
    
    # convert the list to a dataframe to sort and view easier
    results = pd.DataFrame(finish_positions, columns=['Driver', 'Finish_Pos', 'DNF'])
    
    # sort by DNF first (non-DNF comes first), then finish position
    results = results.sort_values(by=['DNF', 'Finish_Pos'], ascending=[True, True]).reset_index(drop=True)
    
    # add relative finishing position column
    results['rel_pos'] = results.index + 1
    
    # driver in position 0 is the winner of that simulation
    # winner = results.iloc[0]['Driver'] # old method to just find the winner, instead now pull a whole df each sim for all finishing posns
    return results

def run_simulations(df, num_simulations=10000, weight_lst=[0.5, 0.5], progress_callback=None):
    # quick check to make sure weight_lst adds to 1
    if sum(weight_lst) != 1:
        raise Exception("Make sure weight params add to 1")

    # init tracking dictionaries
    results_tracker = {driver: [] for driver in df['Driver']}
    win_counts = {driver: 0 for driver in df['Driver']}
    dnf_counts = {driver: 0 for driver in df['Driver']}

    # do n simulations of race results and then track stats
    for i in range(num_simulations):
        race_result = simulate_race(df, weight_lst[0], weight_lst[1])
        for idx, row in race_result.iterrows():
            driver = row['Driver']
            pos = row["rel_pos"]
            results_tracker[driver].append(pos)
            if row["DNF"]:
                dnf_counts[driver] += 1
        winner = race_result.iloc[0]['Driver']
        win_counts[winner] += 1

        if progress_callback and i % 100 == 0:  # update every 100 iterations for speed
            progress_callback(i + 1, num_simulations)
    # combine everything into final results, including statistics like avg finish and standard deviation of all finishes
    final_data = []
    for driver in df['Driver']:
        finishes = results_tracker[driver]
        avg_finish = np.mean(finishes)
        std_dev = np.std(finishes)
        wins = win_counts[driver]
        dnfs = dnf_counts[driver]
        win_prob = wins / num_simulations
        final_data.append((driver, wins, win_prob, avg_finish, std_dev, dnfs))

    # build final dataframe
    win_probs = pd.DataFrame(final_data, columns=['Driver', 'Wins', 'Win_Prob', 'Avg_Finish', 'Finish_StdDev', 'DNFs'])
    win_probs = win_probs.sort_values(by=['Wins', 'Avg_Finish'], ascending=[False, True]).reset_index(drop=True)
    return win_probs

# -- GUI CLASS -- #
### !!!!!! DISCLAIMER: !!!!!! ###
# I am a data scientist, I know absolutely nothing about front
# end, user interfacing programming. For a LOT of this section to build
# the GUI I used ChatGPT's GPT-4o model to assist me with building the
# general framework. With that being said, tkinter is a very cool library, 
# and as I add on to this GUI in the future, I plan on integrating different
# features independently so I can learn more about it. Thanks!

# setting up the GUI
class RaceSimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Race Simulation GUI")

        # track dropdown
        track_frame = tk.Frame(root)
        track_frame.pack(pady=5)
        tk.Label(track_frame, text="Select Track:").pack(side=tk.LEFT)
        self.track_var = tk.StringVar(value=list(TRACK_CSV_LINKS.keys())[0])
        self.track_menu = tk.OptionMenu(track_frame, self.track_var, *TRACK_CSV_LINKS.keys())
        self.track_menu.pack(side=tk.LEFT)

        # num simulations input
        sim_frame = tk.Frame(root)
        sim_frame.pack(pady=5)
        tk.Label(sim_frame, text="Number of Simulations:").pack(side=tk.LEFT)
        self.num_sim_entry = tk.Entry(sim_frame, width=10)
        self.num_sim_entry.insert(0, "10000")
        self.num_sim_entry.pack(side=tk.LEFT)

        # weight slider
        weight_frame = tk.Frame(root)
        weight_frame.pack(pady=5)
        tk.Label(weight_frame, text="Weight on Track-Specific Performance:").pack(side=tk.LEFT)
        self.weight_slider = tk.Scale(weight_frame, from_=0, to=1, resolution=0.01,
                                      orient=tk.HORIZONTAL, length=200)
        self.weight_slider.set(0.5)  # default value
        self.weight_slider.pack(side=tk.LEFT)

        # run sim button
        self.run_btn = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        self.run_btn.pack(pady=10)

        # progress bar
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=5)

        # results area
        self.results_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.results_text.pack(padx=10, pady=10)
    
    def run_simulation(self):
        track_name = self.track_var.get()
        url = TRACK_CSV_LINKS.get(track_name)

        try:
            df = pd.read_csv(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data for {track_name}:\n{e}")
            return

        try:
            num_simulations = int(self.num_sim_entry.get())
            if num_simulations <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Input", "Enter a valid positive number of simulations.")
            return

        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, f"Running {num_simulations} simulations for {track_name}...\n")
        self.root.update()

        def update_progress(current, total):
            percent = int((current / total) * 100)
            self.progress['value'] = percent
            self.root.update_idletasks()

        try:
            track_weight = self.weight_slider.get()
            season_weight = 1 - track_weight
            results_df = run_simulations(df, num_simulations, weight_lst=[track_weight, season_weight], progress_callback=update_progress)
            self.progress['value'] = 100
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed:\n{e}")
            return
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, results_df.to_string(index=False))

# -- MAIN RUN --
if __name__ == "__main__":
    root = tk.Tk()
    app = RaceSimApp(root)
    root.mainloop()