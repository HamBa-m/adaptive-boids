import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from flock import Flock
from config import MAX_SPEED, K_NEAREST, ALIGNMENT_WEIGHT, COHESION_WEIGHT, SEPARATION_WEIGHT

class SimulationAutomator:
    """
    Automates simulations by varying parameters and collects metrics.
    """

    def __init__(self, num_steps=100):
        self.num_steps = num_steps

    def run_simulation(self, k_neighbors, alignment_weight, cohesion_weight, separation_weight):
        """
        Run a single simulation with specified parameters.
        """
        # Update global parameters dynamically
        global K_NEAREST, ALIGNMENT_WEIGHT, COHESION_WEIGHT, SEPARATION_WEIGHT
        K_NEAREST = k_neighbors
        ALIGNMENT_WEIGHT = alignment_weight
        COHESION_WEIGHT = cohesion_weight
        SEPARATION_WEIGHT = separation_weight

        # Initialize the flock
        flock = Flock()
        polarization_values = []
        angular_variance_values = []
        kinetic_energy_values = []

        # Run the simulation for num_steps
        for _ in range(self.num_steps):
            flock.update()
            polarization_values.append(flock.calculate_polarization())
            angular_variance_values.append(flock.calculate_angular_variance())
            kinetic_energy_values.append(flock.calculate_kinetic_energy())

        # Return averages of metrics
        return (
            np.mean(polarization_values),
            np.mean(angular_variance_values),
            np.mean(kinetic_energy_values),
        )

    def automate(self, k_range, weight_combinations):
        """
        Automates simulations by varying K-nearest neighbors and weight combinations.
        """
        results = []
        for k_neighbors in tqdm(k_range, desc="Varying K"):
            for weights in tqdm(weight_combinations, desc="Testing weight combinations", leave=False):
                polarization, variance, energy = self.run_simulation(
                    k_neighbors=k_neighbors,
                    alignment_weight=weights[0],
                    cohesion_weight=weights[1],
                    separation_weight=weights[2],
                )
                results.append({
                    "K": k_neighbors,
                    "Alignment": weights[0],
                    "Cohesion": weights[1],
                    "Separation": weights[2],
                    "Polarization": polarization,
                    "Variance": variance,
                    "Energy": energy,
                })
        return results

    @staticmethod
    def plot_results(results, param="K", metric="Polarization"):
        """
        Plots a heatmap for a given parameter and metric.
        """
        import pandas as pd
        import seaborn as sns

        # Convert results to DataFrame for easier plotting
        df = pd.DataFrame(results)

        # Create a pivot table for heatmap
        heatmap_data = df.pivot_table(
            index="Alignment",
            columns=param,
            values=metric,
            aggfunc=np.mean
        )

        plt.figure(figsize=(10, 6))
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="viridis")
        plt.title(f"{metric} as a function of {param} and Alignment Weight")
        plt.xlabel(param)
        plt.ylabel("Alignment Weight")
        plt.show()


if __name__ == "__main__":
    # Define ranges for parameters
    K_RANGE = range(2, 20, 2)  # K-nearest neighbors
    WEIGHT_RANGE = np.linspace(0.5, 2.5, 5)  # Weight values for alignment, cohesion, and separation
    WEIGHT_COMBINATIONS = [(a, c, s) for a in WEIGHT_RANGE for c in WEIGHT_RANGE for s in WEIGHT_RANGE]

    # Initialize simulation automator
    automator = SimulationAutomator(num_steps=50)

    # Run automated simulations
    results = automator.automate(K_RANGE, WEIGHT_COMBINATIONS)

    # Plot results for Polarization as a function of K and Alignment Weight
    automator.plot_results(results, param="K", metric="Polarization")

    # Example: Plot Angular Variance
    automator.plot_results(results, param="K", metric="Variance")