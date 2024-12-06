# metrics for evaluation of the model
import numpy as np
from flock import Flock

# measure the cohesion of the flock
def cohesion(flock: Flock) -> float:
    # get the center of mass of the flock
    center_of_mass = np.mean(flock.positions, axis=0)
    # get the distance of each bird to the center of mass
    distances = np.linalg.norm(flock.positions - center_of_mass, axis=1)
    # return the average distance
    return np.mean(distances)

# measure the separation of the flock
def separation(flock: Flock) -> float:
    # get the distance of each bird to every other bird
    distances = np.linalg.norm(flock.positions[:, np.newaxis] - flock.positions, axis=2)
    # keep only the distances that are less than the separation distance
    distances = np.where(distances < flock.min_distance, distances, 0)
    # set the diagonal to infinity so that the minimum distance is not zero
    np.fill_diagonal(distances, np.inf)
    # return the average minimum distance
    return np.mean(np.min(distances, axis=1))

# measure the alignment variance of the flock
def alignment_variance(flock: Flock) -> float:
    # get the average velocity of the flock
    average_velocity = np.mean(flock.velocities, axis=0)
    # get the angle of each bird with respect to the average velocity
    angles = np.arctan2(flock.velocities[:, 1], flock.velocities[:, 0]) - np.arctan2(average_velocity[1], average_velocity[0])
    # return the variance of the angles
    return np.var(angles)

# measure the number of cluster of birds in the flock
def clusters(flock: Flock) -> int:
    # get the distance of each bird to every other bird
    distances = np.linalg.norm(flock.positions[:, np.newaxis] - flock.positions, axis=2)
    # keep only the distances that are less than the separation distance
    distances = np.where(distances < flock.min_distance, 1, 0)
    # set the diagonal to zero
    np.fill_diagonal(distances, 0)
    # get the number of connected components
    connected_components = 0
    visited = np.zeros(flock.size, dtype=bool)
    for i in range(flock.size):
        if not visited[i]:
            connected_components += 1
            stack = [i]
            while stack:
                j = stack.pop()
                visited[j] = True
                stack.extend([k for k in range(flock.size) if distances[j, k] and not visited[k]])
    return connected_components