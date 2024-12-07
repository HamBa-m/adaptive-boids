import numpy as np
from config import SCREEN_SIZE, MAX_SPEED, ALIGNMENT_WEIGHT, COHESION_WEIGHT, SEPARATION_WEIGHT

class Bird:
    """Class representing an individual bird (boid)."""

    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def limit_speed(self):
        """Limit the bird's speed to the maximum."""
        speed = np.linalg.norm(self.velocity)
        if speed > MAX_SPEED:
            self.velocity = (self.velocity / speed) * MAX_SPEED

    def move(self):
        """Move the bird and wrap around screen edges."""
        self.position += self.velocity
        self.position %= SCREEN_SIZE

    def calculate_new_velocity(self, neighbors):
        """Calculate the new velocity based on alignment, cohesion, and separation."""
        if neighbors:
            # Alignment: Match velocity with neighbors
            alignment = np.mean([bird.velocity for bird in neighbors], axis=0)
            # Cohesion: Move towards the average position of neighbors
            cohesion = np.mean([bird.position for bird in neighbors], axis=0) - self.position
            # Separation: Avoid getting too close to neighbors
            separation = -np.sum([bird.position - self.position for bird in neighbors], axis=0)

            # Combine forces
            new_velocity = (
                self.velocity
                + ALIGNMENT_WEIGHT * alignment
                + COHESION_WEIGHT * cohesion
                + SEPARATION_WEIGHT * separation
            )
            return self.limit_velocity(new_velocity)
        return self.velocity

    def limit_velocity(self, velocity):
        """Ensure the given velocity does not exceed the max speed."""
        speed = np.linalg.norm(velocity)
        if speed > MAX_SPEED:
            return (velocity / speed) * MAX_SPEED
        return velocity