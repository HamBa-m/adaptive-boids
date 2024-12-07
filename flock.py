import numpy as np
from bird import Bird
from config import NUM_BIRDS, SCREEN_SIZE, K_NEAREST

class Flock:
    """Class representing the flock of birds (boids)."""

    def __init__(self):
        self.birds = [
            Bird(
                position=np.random.rand(2) * SCREEN_SIZE,
                velocity=(np.random.rand(2) - 0.5) * 2,
            )
            for _ in range(NUM_BIRDS)
        ]

    def get_k_nearest_neighbors(self, bird, k):
        """Find the K-nearest neighbors of a bird."""
        distances = [
            (other_bird, np.linalg.norm(bird.position - other_bird.position))
            for other_bird in self.birds
            if other_bird != bird
        ]
        distances.sort(key=lambda x: x[1])  # Sort by distance
        return [neighbor[0] for neighbor in distances[:k]]

    def update(self):
        """Update the position and velocity of each bird asynchronously."""
        # Calculate new velocities first
        new_velocities = []
        for bird in self.birds:
            neighbors = self.get_k_nearest_neighbors(bird, K_NEAREST)
            new_velocities.append(bird.calculate_new_velocity(neighbors))

        # Apply new velocities after all have been computed
        for bird, new_velocity in zip(self.birds, new_velocities):
            bird.velocity = new_velocity
            bird.move()

    def calculate_polarization(self):
        velocities = np.array([bird.velocity for bird in self.birds])
        normalized_velocities = velocities / np.linalg.norm(velocities, axis=1, keepdims=True)
        avg_direction = np.mean(normalized_velocities, axis=0)
        return np.linalg.norm(avg_direction)

    def calculate_angular_variance(self):
        velocities = np.array([bird.velocity for bird in self.birds])
        angles = np.arctan2(velocities[:, 1], velocities[:, 0])
        mean_angle = np.arctan2(np.mean(np.sin(angles)), np.mean(np.cos(angles)))
        return np.mean((angles - mean_angle) ** 2)

    def calculate_kinetic_energy(self):
        velocities = np.array([bird.velocity for bird in self.birds])
        return 0.5 * np.mean(np.linalg.norm(velocities, axis=1) ** 2)
    
    def flock_barycenter(self):
        positions = np.array([bird.position for bird in self.birds])
        return np.mean(positions, axis=0)
