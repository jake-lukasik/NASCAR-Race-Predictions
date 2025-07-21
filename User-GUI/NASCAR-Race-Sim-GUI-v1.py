import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
import numpy as np

# -- UTILITY PARMS -- #
TRACK_CSV_LINKS = {
    "Pocono": "https://raw.githubusercontent.com/jake-lukasik/NASCAR-Race-Predictions/refs/heads/main/Data/Pocono-2025/pocono-sim-ready-data.csv",
    "Dover": "https://raw.githubusercontent.com/jake-lukasik/NASCAR-Race-Predictions/refs/heads/main/Data/Dover-2025/dover-sim-ready-data.csv"
}

# -- SIMULATION FUNCTIONS -- #
# existing simulation functions from before
def simulate_race(df):
    finish_positions = []
    
    for _, row in df.iterrows():
        performance_bonus = (
            0.40 * row['Wins'] +                         
            0.20 * row['szn_Wins'] +                    
            0.10 * row['track_Laps Led Per Race'] +     
            0.10 * row['szn_Laps Led Per Race'] +       
            0.05 * row['Avg Rating'] +                  
            0.05 * row['szn_Avg Rating'] +              
            0.05 * row['Top 5\'s'] +                    
            0.05 * row['szn_Top 5\'s']                  
        )
        adjusted_avg_finish = max(1, (row['Avg Finish'] + (0.5 * row['szn_Avg Finish']))/2 - performance_bonus * 0.25)
        dnf = np.random.rand() < row['DNF_Prob']
        if dnf:
            finish_pos = np.random.randint(len(df) + 1, len(df) + 6)
        else:
            finish_pos = np.random.normal(loc=adjusted_avg_finish, scale=row['Std Dev'])
            finish_pos = max(1, min(len(df), finish_pos))
        finish_positions.append((row['Driver'], finish_pos, dnf))
    results = pd.DataFrame(finish_positions, columns=['Driver', 'Finish_Pos', 'DNF'])
    results = results.sort_values(by=['DNF', 'Finish_Pos'], ascending=[True, True]).reset_index(drop=True)
    return results

def run_simulations(df, num_simulations=10000):
    results_tracker = {driver: [] for driver in df['Driver']}
    win_counts = {driver: 0 for driver in df['Driver']}
    for _ in range(num_simulations):
        race_result = simulate_race(df)
        for idx, row in race_result.iterrows():
            driver = row['Driver']
            pos = row['Finish_Pos']
            results_tracker[driver].append(pos)
        winner = race_result.iloc[0]['Driver']
        win_counts[winner] += 1
    final_data = []
    for driver in df['Driver']:
        finishes = results_tracker[driver]
        avg_finish = np.mean(finishes)
        std_dev = np.std(finishes)
        wins = win_counts[driver]
        win_prob = wins / num_simulations
        final_data.append((driver, wins, win_prob, avg_finish, std_dev))
    win_probs = pd.DataFrame(final_data, columns=['Driver', 'Wins', 'Win_Prob', 'Avg_Finish', 'Finish_StdDev'])
    win_probs = win_probs.sort_values(by='Win_Prob', ascending=False).reset_index(drop=True)
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

        # run sim button
        self.run_btn = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        self.run_btn.pack(pady=10)

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

        try:
            results_df = run_simulations(df, num_simulations)
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