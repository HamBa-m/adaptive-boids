# Flocking Simulation Repository

This repository provides a framework for simulating and analyzing flocking behavior (boids). It allows you to explore how different parameters influence collective dynamics through metrics such as polarization, angular variance, and kinetic energy.

---

## Repository Structure

```
.
├── bird.py              # Defines the Bird class, representing individual boids.
├── flock.py             # Defines the Flock class, managing the group of boids and their behaviors.
├── config.py            # Stores global parameters like screen size, weights, and simulation settings.
├── render.py            # Handles visualization of the flock's behavior in real time.
├── run_simulation.py    # Automates simulations, collects metrics, and runs experiments.
├── metrics_plot.py      # Plots metrics like polarization and variance to analyze simulation results.
```

---

## Metrics Used and Their Significance

1. **Polarization**:
   - **Definition**: A measure of global alignment in the flock.
   - **Formula**: 
     ```math
     \Phi = \frac{1}{N} \left| \sum_{i=1}^N \frac{\vec{v}_i}{|\vec{v}_i|} \right|
     ```
     where $ \vec{v}_i $ is the velocity vector of bird $ i $.
   - **Significance**: 
     - $ \Phi = 1 $: Perfect alignment.
     - $ \Phi \approx 0 $: Complete chaos.
     - Helps identify transitions between ordered and disordered states.

2. **Angular Variance**:
   - **Definition**: Measures the dispersion of movement directions in the flock.
   - **Formula**: 
     ```math
     \sigma_\theta^2 = \frac{1}{N} \sum_{i=1}^N (\theta_i - \bar{\theta})^2
     ```
     where $ \theta_i $ is the angle of the velocity vector of bird $ i $ and $ \bar{\theta} $ is the mean angle.
   - **Significance**: 
     - High variance: Disordered motion.
     - Low variance: Coordinated motion.

3. **Kinetic Energy**:
   - **Definition**: Represents the average energy of movement in the flock.
   - **Formula**: 
     ```math
     E_k = \frac{1}{N} \sum_{i=1}^N \frac{1}{2} |\vec{v}_i|^2
     ```
        where $ \vec{v}_i $ is the velocity vector of bird $ i $.
   - **Significance**: 
     - Indicates the level of activity and speed within the flock.
     - High kinetic energy: Fast and active flock.
     - Low kinetic energy: Slow and less active flock.

---

## How to Use the Repository

1. **Run Visualizations**:
   - Use `render.py` to observe the behavior of the flock in real time.

2. **Automate and Analyze Simulations**:
   - Use `run_simulation.py` to explore the impact of parameters like weights and neighbor settings.
   - Use `metrics_plot.py` to generate plots for metrics like polarization, angular variance, and kinetic energy.

3. **Configure Settings**:
   - Modify `config.py` to adjust parameters such as flock size, weights, and simulation duration.

---

## Requirements

Install the necessary dependencies:
```
pip install numpy matplotlib tqdm pygame
```
