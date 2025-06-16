# 🏁 NASCAR Race Win Prediction via Monte Carlo Simulation

A data-driven simulation tool to predict the winner of a NASCAR Cup Series race using Monte Carlo methods. This project is focused on the upcoming race at Pocono Raceway, using historical driver data, DNF rates, and performance metrics to simulate thousands of race outcomes.

---

## 📂 Project Structure

NASCAR-Race-Predictions/
├── Pocono-Driver-Data/
│ ├── pocono-sim-ready-data.csv # Main dataset with Avg Finish, DNF %, Std Dev, etc.
│ └── cup_roster.csv # Contains driver names and car numbers
├── images/
│ └── driver_numbers/ # PNGs of driver numbers used in plots
├── simulations/
│ └── monte_carlo_simulation.py # Core simulation logic
├── plots/
│ └── win_probabilities.png # Output visualizations
├── README.md


---

## 📊 Methodology

1. **Data Sourcing**
   - Historical Pocono stats from [DriverAverages.com](https://www.driveraverages.com/)
   - Current season stats, DNF counts, and average finishes

2. **Monte Carlo Simulation**
   - Each simulation randomly samples a finishing position based on:
     - Driver's average Pocono finish
     - Standard deviation (performance variance)
     - DNF probability
   - Races are run thousands of times (`N=10,000`) to estimate win probabilities

3. **Assumptions**
   - If a driver has no Pocono history, they are assigned average estimates with higher variance.
   - DNFs finish near the back randomly.

---

## 🔁 Run the Simulation

### 🧠 Requirements
```bash
pip install pandas numpy matplotlib seaborn
```



Data sourced from driveraverages.com
