import matplotlib.pyplot as plt

def plot_metrics(polarization, angular_variance, kinetic_energy):
    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    plt.plot(polarization, label="Polarization")
    plt.title("Polarization")
    plt.xlabel("Time step")
    plt.ylabel("Polarization")

    plt.subplot(3, 1, 2)
    plt.plot(angular_variance, label="Angular Variance", color="orange")
    plt.title("Angular Variance")
    plt.xlabel("Time step")
    plt.ylabel("Variance")

    plt.subplot(3, 1, 3)
    plt.plot(kinetic_energy, label="Kinetic Energy", color="red")
    plt.title("Kinetic Energy")
    plt.xlabel("Time step")
    plt.ylabel("Energy")

    plt.tight_layout()
    plt.show()
