# Stochastic Pricing Model for Baseball Game States

## Objective
This project utilizes a Markov Chain transition matrix to calculate the mathematical expected run value of every possible pitch count in a Major League Baseball at-bat. 

By treating a baseball plate appearance as a memoryless stochastic process, this model calculates the exact probability of transitioning from one state (e.g., a 0-0 count) to any future state, ultimately converging on absorbing states (events that end the plate appearance, such as a strikeout or home run).

## Methodology
The model was built using pitch-by-pitch MLB Statcast data. 
1. **State Space:** Defined by the current pitch count (Balls-Strikes).
2. **Transition Matrix ($P$):** Calculated the conditional probability of transitioning from state $S_t$ to $S_{t+1}$.
3. **Value Iteration:** Assigned standard linear weights to absorbing states and iterated through the transition matrix to solve for the expected value of all transient states using the following Bellman-style equation:

$$V(s) = \sum_{s'} P(s \to s') \cdot V(s')$$

## Results: Expected Run Value by Count
Applying this model to early 2024 MLB data yields the following mathematical valuations for pitch counts, proving that a 3-0 count holds the highest expected run value, while an 0-2 count severely disadvantages the hitter.

* **3-0:** +0.176 runs
* **3-1:** +0.138 runs
* **2-0:** +0.088 runs
* **3-2:** +0.055 runs
* **2-1:** +0.036 runs
* **1-0:** +0.030 runs
* **0-0:** -0.006 runs
* **1-1:** -0.014 runs
* **0-1:** -0.044 runs
* **2-2:** -0.049 runs
* **1-2:** -0.086 runs
* **0-2:** -0.107 runs
