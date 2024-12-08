import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from flock import Flock
from config import MAX_SPEED, K_NEAREST, ALIGNMENT_WEIGHT, COHESION_WEIGHT, SEPARATION_WEIGHT
import copy  # Import the copy module

class SimulationAutomator:
    """
    Automates simulations by varying parameters and collects metrics.
    """

    def __init__(self, num_steps=100):
        self.num_steps = num_steps

    def run_simulation(self, k_neighbors, alignment_weight, cohesion_weight, separation_weight , flock):
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
        #flock = Flock()
        polarization_values = []
        angular_variance_values = []
        kinetic_energy_values = []
        flock_barcenter_values = []

        # Run the simulation for num_steps
        for _ in range(self.num_steps):
            polarization_values.append(flock.calculate_polarization())
            angular_variance_values.append(flock.calculate_angular_variance())
            kinetic_energy_values.append(flock.calculate_kinetic_energy())
            flock_barcenter_values.append(flock.flock_barycenter())
            flock.update()

        # Return averages of metrics
        return (
            np.mean(polarization_values),
            np.mean(angular_variance_values),
            np.mean(kinetic_energy_values),
            flock_barcenter_values
        )

    def automate(self, k_range, weight_combinations):
        """
        Automates simulations by varying K-nearest neighbors and weight combinations.
        """
        results = []
        barycenter_data = []  # To store barycenter values for plotting
        flock_VI = Flock()
        for k_neighbors in tqdm(k_range, desc="Varying K"):
            for weights in tqdm(weight_combinations, desc="Testing weight combinations", leave=False):
                flock = copy.deepcopy(flock_VI)
                #flock = Flock()
                polarization, variance, energy , flock_barycenter = self.run_simulation(
                    k_neighbors=k_neighbors,
                    alignment_weight=weights[0],
                    cohesion_weight=weights[1],
                    separation_weight=weights[2],
                    flock=flock
                )
                results.append({
                    "K": k_neighbors,
                    "Alignment": weights[0],
                    "Cohesion": weights[1],
                    "Separation": weights[2],
                    "Polarization": polarization,
                    "Variance": variance,
                    "Energy": energy,
                    "Flock_Barycenter": flock_barycenter
                })
                barycenter_data.append({
                "K": k_neighbors,
                "Weight": weights,
                "Barycenter": flock_barycenter
            })
              
        return results,barycenter_data
    
    @staticmethod
    def plot_barycenter(barycenter_data):
        """
        Plots barycenter values (x and y) for each K and weight combination,
        marking the final position with a single square symbol labeled 'End'.
        The weight combination is labeled as Alignment, Cohesion, or Separation.
        """
        plt.figure(figsize=(12, 8))

        for data in barycenter_data:
            k_neighbors = data["K"]
            weights = data["Weight"]
            barycenter_points = data["Barycenter"]

            # Extract x and y coordinates from the barycenter
            x_values = [point[0] for point in barycenter_points]
            y_values = [point[1] for point in barycenter_points]

            # Map weights to label
            if weights == (1, 0, 0):
                weight_label = "Alignment"
            elif weights == (0, 1, 0):
                weight_label = "Cohesion"
            elif weights == (0, 0, 1):
                weight_label = "Separation"
            else:
                weight_label = f"Factors Equal: 0.33"

            # Plot the trajectory
            line, = plt.plot(x_values, y_values, label=f"K={k_neighbors}, {weight_label}", linestyle="-", marker="o")

            # Use the same color as the line for the final position marker
            line_color = line.get_color()

            # Highlight only the final position with a single square marker, labeled "End"
            plt.scatter(x_values[-1], y_values[-1], marker="s", s=100, label="End", zorder=5)

        plt.title("Flock Barycenter Values (x vs. y) for K = 7 and Factors Combination")
        plt.xlabel("Barycenter X")
        plt.ylabel("Barycenter Y")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


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
    K_RANGE = range(7, 8)  # K-nearest neighbors
    WEIGHT_RANGE = np.linspace(0.5, 2.5, 5)  # Weight values for alignment, cohesion, and separation
    #WEIGHT_COMBINATIONS = [(a, c, s) for a in WEIGHT_RANGE for c in WEIGHT_RANGE for s in WEIGHT_RANGE]
    WEIGHT_COMBINATIONS = [(1, 0, 0), (0, 1, 0), (0, 0, 1),(0.33,0.33,0.33)]

    # Initialize simulation automator
    automator = SimulationAutomator(num_steps=20)

    # Run automated simulations
    results,bar = automator.automate(K_RANGE, WEIGHT_COMBINATIONS)

    # Plot results for Polarization as a function of K and Alignment Weight
    automator.plot_results(results, param="K", metric="Polarization")

    # Example: Plot Angular Variance
    automator.plot_results(results, param="K", metric="Variance")

            
    # Plot barycenter values
    automator.plot_barycenter(bar)