from bird import Bird
from optimiser import Optimiser
import random
import pygame

def distance(bird1, bird2):
    return ((bird1.position[0] - bird2.position[0])**2 + (bird1.position[1] - bird2.position[1])**2)**0.5

class Flock:
    def __init__(self, size, radius, min_distance, max_speed, optimizer_threshold, k = 6) -> None:
        self.size = size
        self.k = k
        self.min_distance = min_distance
        self.max_speed = max_speed
        self.radius = radius
        self.birds = [Bird(self.radius, self.max_speed, optimizer_threshold, 0.1, [0, 1]) for _ in range(size)]
        
        # statistics
        self.stats_history = {
            'alignment_variance': [],
            'cohesion': [],
            'separation': [],
            'clusters': [],
            'isolated': [],
            'connected': []
        }
        
    def move(self):
        for bird in self.birds:
            bird.move()
            
    def __str__(self) -> str:
        # return parameters of the flock
        bird_radius = self.birds[0].radius
        bird_max_speed = self.birds[0].max_speed
        bird_noise = self.birds[0].noise
        bird_omega_alignment = self.birds[0].omega[0]
        bird_omega_cohesion = self.birds[0].omega[1]
        bird_omega_separation = self.birds[0].omega[2]
        return f'Size: {self.size}\nMin Distance: {self.min_distance}\nBird Radius: {bird_radius}\nBird K neighbors: {self.k}\nBird Max Speed: {bird_max_speed}\nBird Noise: {bird_noise}\nBird Omega Alignment: {bird_omega_alignment}\nBird Omega Cohesion: {bird_omega_cohesion}\nBird Omega Separation: {bird_omega_separation}'
        
    def _find_neighbours(self, bird):
        neighbours = []
        for other_bird in self.birds:
            if other_bird is bird:
                continue
            if distance(bird, other_bird) < bird.radius:
                neighbours.append(other_bird)
        bird.neighbours = sorted(neighbours, key=lambda x: distance(bird, x))
    
    def _compute_alignment(self, bird):
        if not bird.neighbours:
            return [0, 0]
        avg_velocity = [0, 0]
        for neighbour in bird.neighbours[:self.k]:
            avg_velocity[0] += neighbour.velocity[0]
            avg_velocity[1] += neighbour.velocity[1]
        avg_velocity[0] /= len(bird.neighbours)
        avg_velocity[1] /= len(bird.neighbours)
        return avg_velocity
    
    def _compute_bird_cohesion(self, bird):
        if not bird.neighbours:
            return [0, 0]
        avg_position = [0, 0]
        for neighbour in bird.neighbours[:self.k]:
            avg_position[0] += neighbour.position[0]
            avg_position[1] += neighbour.position[1]
        avg_position[0] /= len(bird.neighbours)
        avg_position[1] /= len(bird.neighbours)
        return [avg_position[0] - bird.position[0], avg_position[1] - bird.position[1]]
    
    def _compute_bird_separation(self, bird):
        separation = [0, 0]
        for neighbour in bird.neighbours[:self.k]:
            if distance(bird, neighbour) < self.min_distance :
                separation[0] -= neighbour.position[0] - bird.position[0]
                separation[1] -= neighbour.position[1] - bird.position[1]
        return separation
    
    def _update_velocity(self, bird):
        # check if bird isn't near the border within min_distance
        if bird.position[0] < self.min_distance or bird.position[0] > 1000 - self.min_distance or bird.position[1] < self.min_distance or bird.position[1] > 600 - self.min_distance:
            return bird.velocity
        alignment = self._compute_alignment(bird)
        cohesion = self._compute_bird_cohesion(bird)
        separation = self._compute_bird_separation(bird)
        randomness = bird.omega[3]
        new_velocity = bird.velocity
        if not bird.neighbours:
            return new_velocity
        # standardize velocity
        alignment_norm = (alignment[0]**2 + alignment[1]**2)**0.5
        cohesion_norm = (cohesion[0]**2 + cohesion[1]**2)**0.5
        separation_norm = (separation[0]**2 + separation[1]**2)**0.5
        if alignment_norm > 0:
            alignment[0] = alignment[0] * bird.max_speed / alignment_norm
            alignment[1] = alignment[1] * bird.max_speed / alignment_norm
        if cohesion_norm > 0:
            cohesion[0] = cohesion[0] * bird.max_speed / cohesion_norm
            cohesion[1] = cohesion[1] * bird.max_speed / cohesion_norm
        if separation_norm > 0:
            separation[0] = separation[0] * bird.max_speed / separation_norm
            separation[1] = separation[1] * bird.max_speed / separation_norm

        # update velocity
        for i in range(2):
            new_velocity[i] = \
                bird.omega[0] * alignment[i] \
                    + bird.omega[1] * cohesion[i] \
                        + bird.omega[2] * separation[i] \
                            + random.uniform(-bird.noise, bird.noise) \
                                + randomness * random.uniform(-bird.max_speed, bird.max_speed)
        return new_velocity

    # compute the average direction of the flock
    def _compute_avg_direction(self):
        '''Average direction is the average velocity of all birds in the flock'''
        avg_direction = [0, 0]
        for bird in self.birds:
            avg_direction[0] += bird.velocity[0]
            avg_direction[1] += bird.velocity[1]
        avg_direction[0] /= len(self.birds)
        avg_direction[1] /= len(self.birds)
        return avg_direction
    
    # measure the cohesion of the flock
    def _compute_cohesion(self) -> float:
        '''Cohesion is the inverse of the average distance between each bird and the average position of the flock'''
        avg_position = [0, 0]
        for bird in self.birds:
            avg_position[0] += bird.position[0]
            avg_position[1] += bird.position[1]
        avg_position[0] /= len(self.birds)
        avg_position[1] /= len(self.birds)
        cohesion = 0
        for bird in self.birds:
            cohesion += (bird.position[0] - avg_position[0])**2 + (bird.position[1] - avg_position[1])**2
        return 1 / cohesion

    # measure the average separation of the flock
    def _compute_separation(self) -> float:
        '''Separation is the average distance between each bird and its neighbours'''
        separation = 0
        for bird in self.birds:
            bird_separation = 0
            for neighbour in bird.neighbours:
                separation += distance(bird, neighbour)
            separation += bird_separation / len(bird.neighbours) if bird.neighbours else 0
        return separation / len(self.birds)

    # measure the alignment variance of the flock
    def _compute_alignment_variance(self) -> float:
        '''Alignment variance is the variance of the velocity of all birds in the flock'''
        avg_velocity = [0, 0]
        for bird in self.birds:
            avg_velocity[0] += bird.velocity[0]
            avg_velocity[1] += bird.velocity[1]
        avg_velocity[0] /= len(self.birds)
        avg_velocity[1] /= len(self.birds)
        variance = 0
        for bird in self.birds:
            variance += (bird.velocity[0] - avg_velocity[0])**2 + (bird.velocity[1] - avg_velocity[1])**2
        return variance

    # measure the number of cluster of birds in the flock
    def _compute_clusters(self) -> int:
        '''Clusters is the number of connected components in the flock'''
        distances = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                distances[i][j] = distance(self.birds[i], self.birds[j])
        connected_components = 0
        visited = [False for _ in range(self.size)]
        for i in range(self.size):
            if not visited[i]:
                connected_components += 1
                stack = [i]
                while stack:
                    j = stack.pop()
                    visited[j] = True
                    for k in range(self.size):
                        if distances[j][k] < self.min_distance * 2 and not visited[k]:
                            stack.append(k)
        return connected_components
    
    def update_statistics(self):
        birds_isolated = 0
        birds_connected = 0
        for bird in self.birds:
            if bird.optimiser.state == 'isolated':
                birds_isolated += 1
            else:
                birds_connected += 1
        
        self.stats_history['alignment_variance'].append(self._compute_alignment_variance())
        self.stats_history['cohesion'].append(self._compute_cohesion())
        self.stats_history['separation'].append(self._compute_separation())
        self.stats_history['clusters'].append(self._compute_clusters())
        
        self.stats_history['isolated'].append(birds_isolated)
        self.stats_history['connected'].append(birds_connected)
                
    def update(self):
        for bird in self.birds:
            self._find_neighbours(bird)
        # asynchronus update
        new_velocities = [self._update_velocity(bird) for bird in self.birds] 
        for i, bird in enumerate(self.birds):
            bird.velocity = new_velocities[i]
            bird.move()
            if bird.position[0] < 0:
                bird.position[0] += self.screen_size[0]
            elif bird.position[0] > self.screen_size[0]:
                bird.position[0] -= self.screen_size[0]
            if bird.position[1] < 0:
                bird.position[1] += self.screen_size[1]
            elif bird.position[1] > self.screen_size[1]:
                bird.position[1]-= self.screen_size[1]
        self.update_statistics()
        
    def run_cmd(self, verbose=False):
        self.running = True
        while self.running:
            self.update()
            if verbose:
                print(self.__str__())
        # save the statistics history in csv
        with open('statistics.csv', 'w') as f:
            f.write('cohesion,separation,alignment_variance,clusters,isolated,connected\n')
            for i in range(len(self.stats_history['cohesion'])):
                f.write(f'{self.stats_history["cohesion"][i]},{self.stats_history["separation"][i]},{self.stats_history["alignment_variance"][i]},{self.stats_history["clusters"][i]},{self.stats_history["isolated"][i]},{self.stats_history["connected"][i]}\n')
    
    def __str__(self) -> str:
        # return statistics
        return f'Cohesion: {self._compute_cohesion()}\nSeparation: {self._compute_separation()}\nAlignment Variance: {self._compute_alignment_variance()}\nClusters: {self._compute_clusters()}\nIsolated: {self.stats_history["isolated"][-1]}\nConnected: {self.stats_history["connected"][-1]}'

    def render(self, verbose=False):
        # fill the screen with bg.png
        bg = pygame.image.load('assets/bg.png')
        # resize the image
        bg = pygame.transform.scale(bg, (1000, 600))
        self.screen.blit(bg, (0, 0))
        
        # draw the birds
        for bird in self.birds:
            pygame.draw.circle(self.screen, (0, 0, 0), (int(bird.position[0]), int(bird.position[1])), 3)            

        for bird in self.birds:
            pygame.draw.line(self.screen, (255, 0, 0), (bird.position[0], bird.position[1]), (bird.position[0] + bird.velocity[0], bird.position[1] + bird.velocity[1]), 2)

        avg_direction = self._compute_avg_direction()
        pygame.draw.line(self.screen, (0, 0, 0), (80, 80), (80 + avg_direction[0] * 5, 80 + avg_direction[1] * 5), 2)
        pygame.draw.circle(self.screen, (0, 0, 0), (80 + avg_direction[0] * 5, 80 + avg_direction[1] * 5), 5)

        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render('Average Direction', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.topleft = (10, 10)
        self.screen.blit(text, textRect)

        # Draw buttons
        self.draw_buttons()
        
        # Print statistics if verbose in CMD
        if verbose:
            print(self.__str__())

        pygame.display.flip()
        pygame.time.delay(10)

    def draw_buttons(self):
        start_button = pygame.Rect(850, 50, 100, 40)
        pause_button = pygame.Rect(850, 100, 100, 40)
        stop_button = pygame.Rect(850, 150, 100, 40)
        
        pygame.draw.rect(self.screen, (0, 255, 0), start_button)
        pygame.draw.rect(self.screen, (255, 255, 0), pause_button)
        pygame.draw.rect(self.screen, (255, 0, 0), stop_button)
        
        font = pygame.font.Font('freesansbold.ttf', 16)
        start_text = font.render('Play', True, (0, 0, 0))
        pause_text = font.render('Pause', True, (0, 0, 0))
        stop_text = font.render('Stop', True, (0, 0, 0))
        
        self.screen.blit(start_text, (860, 60))
        self.screen.blit(pause_text, (860, 110))
        self.screen.blit(stop_text, (860, 160))

    def init_render(self):
        pygame.init()
        self.screen_size = (1000, 600)
        self.screen = pygame.display.set_mode(self.screen_size)

    def start_render(self, verbose=False):
        self.running = True
        self.paused = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Start button
                    if 850 <= mouse_x <= 950 and 50 <= mouse_y <= 90:
                        self.paused = False
                    # Pause button
                    elif 850 <= mouse_x <= 950 and 100 <= mouse_y <= 140:
                        self.paused = True
                    # Stop button
                    elif 850 <= mouse_x <= 950 and 150 <= mouse_y <= 190:
                        self.running = False
                        
            if not self.paused:
                self.update()
            self.render(verbose = verbose)

    def pause_render(self):
        self.running = False
        self.paused = True
        print(self.__str__())

    def stop_render(self):
        # save the statistics history in csv
        with open('statistics.csv', 'w') as f:
            f.write('cohesion,separation,alignment_variance,clusters,isolated,connected\n')
            for i in range(len(self.stats_history['cohesion'])):
                f.write(f'{self.stats_history["cohesion"][i]},{self.stats_history["separation"][i]},{self.stats_history["alignment_variance"][i]},{self.stats_history["clusters"][i]},{self.stats_history["isolated"][i]},{self.stats_history["connected"][i]}\n')
        
        self.running = False
        
