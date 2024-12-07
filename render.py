import pygame
from flock import Flock
from config import SCREEN_SIZE, BOID_SIZE, NUM_BIRDS
from metrics_plot import plot_metrics

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Flock Simulation with Metrics")

# Main simulation loop
flock = Flock()
polarization_values = []
angular_variance_values = []
kinetic_energy_values = []
num_steps = 1000
running = True
clock = pygame.time.Clock()

while running and len(polarization_values) < num_steps:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    flock.update()

    # Collect metrics
    polarization_values.append(flock.calculate_polarization())
    angular_variance_values.append(flock.calculate_angular_variance())
    kinetic_energy_values.append(flock.calculate_kinetic_energy())

    # Draw the flock
    screen.fill((0, 0, 0))
    for bird in flock.birds:
        pygame.draw.circle(screen, (50, 150, 255), bird.position.astype(int), BOID_SIZE)
    pygame.display.flip()

    clock.tick(30)

pygame.quit()

# Plot metrics
plot_metrics(polarization_values, angular_variance_values, kinetic_energy_values)