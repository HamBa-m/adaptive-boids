# define a bird class from the boids algorithm
import random
from optimiser import Optimiser

class Bird:
    def __init__(self, radius, max_speed, optimizer_threshold, noise, north_direction) -> None:
        self.position = [random.randint(300, 700), random.randint(100, 500)]
        self.velocity =[north_direction[0] + random.uniform(-noise, noise), north_direction[1] + random.uniform(-noise, noise)]
        self.max_speed = max_speed
        self.neighbours = []
        self.omega = [0.3, 0.1, 0.6, 0.0] # weights for alignment, cohesion, separation, randomness
        self.noise = noise
        self.radius = radius
        self.optimiser = Optimiser(self, threshold=optimizer_threshold)
        
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.velocity[0] = min(self.velocity[0], self.max_speed)
        self.velocity[1] = min(self.velocity[1], self.max_speed)
        self.optimiser.update_weights()
        
    def __str__(self) -> str:
        return f'Position: {self.position}, Velocity: {self.velocity}, Neighbours: {len(self.neighbours)}'
