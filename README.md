# 🏁 2025 Season NASCAR Race Win Prediction via Monte Carlo Simulation

<sub>Kind of... I started this in June.</sub>

A data-driven simulation tool to predict the winner of a NASCAR Cup Series race using Monte Carlo methods. This project uses historical driver data, DNF rates, and performance metrics to simulate thousands of race outcomes.

Read more about how a Monte Carlo simulation works [here](https://www.ibm.com/think/topics/monte-carlo-simulation)

For the full NASCAR Cup Series schedule, click [here](https://www.nascar.com/nascar-cup-series/2025/schedule/)

--- 

## Predictions and Evaluation By Track:

*Betting odds sourced from the Fanatics Sportsbook iPhone App, learn more [here](https://betfanatics.com/)*

*As the author of this project, I do not endorse sports betting in any form. I simply include betting odds to evaluate my model's predictive performance. If you choose to bet on sports, please do not use these predictions as your sole source of information. Gambling involves risk and should be approached responsibly. This project is intended for educational and analytical purposes only.*

### 🏔️ Pocono Raceway:

**Prediction:**

| 🥇 #1           | 🥈 #2           | 🥉 #3           |
|----------------|----------------|----------------|
| **#24** Byron  | **#11** Hamlin | **#5** Larson  |
|      +600 (T2)  |    +400 (1)   |    +600 (T2)   |

<sub>Odds updated 06/17/2025.</sub>

My Top 10:

<img src="Predictions/Pocono-2025/Pocono-2025-Predicted-Top-10.png" alt="Pocono 2025 Predicted Top 10" width="500"/>

My Personal Pick:

Kyle Larson has been completely out of luck since the debacle when he tried to perform the double. He's my top pick, along with Hamlin due to his dominance at Pocono, as well as Hocevar hopefully finally getting win No. 1. A late race skirmish between the 11 and the 5 like we saw in 2023 would not surprise me.

**Race Result:**

| 🥇 #1           | 🥈 #2           | 🥉 #3           |
|----------------|----------------|----------------|
|   |  |   |

---

Comments On Predictive Performance: 

**Be back on Sunday night!**

## 📂 Project Structure

*Structure subject to change as project evolves*

NASCAR-Race-Predictions/

├── Data/

│ ├── All track specific, season specific, and 'Master' data here, including driver roster and .png images of driver number logos

├── Code Notebooks/

│ └── Here you can find all the code I have run to produce predictions in ipynb files. I plan writing plain .py scripts in the future to allow more accesibility. 

├── Predictions/

│ └── Find all plots and visualizations I produce from my predictions here.

├── README.md


---

## 🧠 Methodology

1. **Data Collection**  
   Driver statistics (average finish, laps led, DNF count, etc.) sourced from [DriverAverages.com](https://www.driveraverages.com).

2. **Feature Engineering**  
   - Calculated `DNF_Prob` using custom logic based on past races and DNFs.
   - `Laps Led Per Race` to reflect dominance potential.
   - `Standard Deviation` for simulating finish variability.

3. **Simulation**  
   - Each race run using a Monte Carlo simulation.
   - DNF outcomes handled probabilistically.
   - Finished positions sampled from a normal distribution around each driver’s average with custom standard deviation.

4. **Results**  
   - Simulation run 10,000+ times.
   - Win probabilities estimated based on number of wins across simulations.

---

## 📊 Visualization

The top drivers' win probabilities are displayed using a horizontal bar chart, more visualization enhancements are planned.

---

## 🔁 Run the Simulation

### 💻 Requirements

The following libraries are required, run this line in your Python environment to install all of them

```bash
pip install pandas numpy matplotlib seaborn
```

*Once project is expanded upon, more info on running your own simulation will go here*

--- 

## 📈 Future Improvements

- Include pit crew performance metrics.

- Factor in qualifying position and starting grid.

- Extend to multiple tracks across the season.

- Add GUI dashboard (once a good base of tracks has been added).

- ~~Factor in non track-exclusive driver statistics~~

---

## 📚 Data Source

Driver data from: [DriverAverages.com](https://www.driveraverages.com/)

Driver number logo images from: [NASCAR Website](https://www.nascar.com/drivers/nascar-cup-series/)

---

## ❤️ Project Motivation

I have always been a massive NASCAR fan, and as I have begun working on projects within data science related to sports, I have seen the huge gap that is present in NASCAR with data utilization. While this project is a simple one, I think it is fascinating getting to use some concepts I am familiar with via school and industry work in a setting of a sport I love. I hope too that data science students just like me could find inspiration from this project.

---

## 🧑‍💻 Author
[Jacob Lukasik](https://www.linkedin.com/in/jacob-lukasik-00306826b/) | Penn State B.S. Data Science | Graduating Fall 2025
