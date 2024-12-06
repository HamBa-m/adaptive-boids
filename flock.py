from bird import Bird
from optimiser import Optimiser
import random
import pygame

def distance(bird1, bird2):
    return ((bird1.position[0] - bird2.position[0])**2 + (bird1.position[1] - bird2.position[1])**2)**0.5

class Flock:
    def __init__(self, size, min_distance, max_speed, k = 6) -> None:
        self.size = size
        self.k = k
        self.min_distance = min_distance
        self.max_speed = max_speed
        self.birds = [Bird(0.1, self.max_speed, [0, 1]) for _ in range(size)]
        
        # statistics
        self.variance = 0
        self.birds_isolated = 0
        self.birds_peripheral = 0
        self.birds_central = 0
        self.variance_history = []
        self.stats = []
        
    def move(self):
        for bird in self.birds:
            bird.move()
            
    def __str__(self) -> str:
        # return parameters of the flock
        size = self.size
        min_distance = self.min_distance
        bird_radius = self.birds[0].radius
        bird_max_speed = self.birds[0].max_speed
        bird_noise = self.birds[0].noise
        bird_omega_alignment = self.birds[0].omega[0]
        bird_omega_cohesion = self.birds[0].omega[1]
        bird_omega_separation = self.birds[0].omega[2]
        return f'Size: {size}\nMin Distance: {min_distance}\nBird Radius: {bird_radius}\nBird Max Speed: {bird_max_speed}\nBird Noise: {bird_noise}\nBird Omega Alignment: {bird_omega_alignment}\nBird Omega Cohesion: {bird_omega_cohesion}\nBird Omega Separation: {bird_omega_separation}'
        
    def _find_neighbours(self, bird):
        neighbours = []
        for other_bird in self.birds:
            if other_bird is bird:
                continue
            if distance(bird, other_bird) < bird.radius:
                neighbours.append(other_bird)
        bird.neighbours = sorted(neighbours, key=lambda x: distance(bird, x))[:self.k]
    
    def _compute_alignment(self, bird):
        if not bird.neighbours:
            return [0, 0]
        avg_velocity = [0, 0]
        for neighbour in bird.neighbours:
            avg_velocity[0] += neighbour.velocity[0]
            avg_velocity[1] += neighbour.velocity[1]
        avg_velocity[0] /= len(bird.neighbours)
        avg_velocity[1] /= len(bird.neighbours)
        return avg_velocity
    
    def _compute_cohesion(self, bird):
        if not bird.neighbours:
            return [0, 0]
        avg_position = [0, 0]
        for neighbour in bird.neighbours:
            avg_position[0] += neighbour.position[0]
            avg_position[1] += neighbour.position[1]
        avg_position[0] /= len(bird.neighbours)
        avg_position[1] /= len(bird.neighbours)
        return [avg_position[0] - bird.position[0], avg_position[1] - bird.position[1]]
    
    def _compute_separation(self, bird):
        separation = [0, 0]
        for neighbour in bird.neighbours:
            if distance(bird, neighbour) < self.min_distance :
                separation[0] -= neighbour.position[0] - bird.position[0]
                separation[1] -= neighbour.position[1] - bird.position[1]
        return separation
    
    def standardize_velocity(self, bird):
        norm = (bird.velocity[0]**2 + bird.velocity[1]**2)**0.5
        if norm > bird.max_speed:
            bird.velocity[0] = bird.velocity[0] * bird.max_speed / norm
            bird.velocity[1] = bird.velocity[1] * bird.max_speed / norm
    
    def _update_velocity(self, bird):
        # check if bird isn't near the border within min_distance
        if bird.position[0] < self.min_distance or bird.position[0] > 1000 - self.min_distance or bird.position[1] < self.min_distance or bird.position[1] > 600 - self.min_distance:
            return bird.velocity
        alignment = self._compute_alignment(bird)
        cohesion = self._compute_cohesion(bird)
        separation = self._compute_separation(bird)
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
            new_velocity[i] = bird.omega[0] * alignment[i] + bird.omega[1] * cohesion[i] + bird.omega[2] * separation[i] + random.uniform(-bird.noise, bird.noise) \
                + randomness * random.uniform(-1, 1)
        return new_velocity
    
    def update_statistics(self):
        self.birds_isolated = 0
        self.birds_peripheral = 0
        self.birds_central = 0
        for bird in self.birds:
            if bird.optimiser.state == 'isolated':
                self.birds_isolated += 1
            elif bird.optimiser.state == 'peripheral':
                self.birds_peripheral += 1
            else:
                self.birds_central += 1
                
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
        self.variance_history.append(self.compute_variance())

    def compute_variance(self):
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
    
    # compute the average neighbour distance
    def compute_avg_neighbour_distance(self):
        avg_distance = 0
        for bird in self.birds:
            avg_distance_bird = 0
            for neighbour in bird.neighbours:
                avg_distance_bird += distance(bird, neighbour)
            avg_distance += avg_distance_bird / len(bird.neighbours) if bird.neighbours else 0
        return avg_distance / len(self.birds)
    
    # compute the average number of neighbours
    def compute_avg_neighbours(self):
        avg_neighbours = 0
        for bird in self.birds:
            avg_neighbours += len(bird.neighbours)
        return avg_neighbours / len(self.birds)
    
    # compute the average direction of the flock
    def compute_avg_direction(self):
        avg_direction = [0, 0]
        for bird in self.birds:
            avg_direction[0] += bird.velocity[0]
            avg_direction[1] += bird.velocity[1]
        avg_direction[0] /= len(self.birds)
        avg_direction[1] /= len(self.birds)
        return avg_direction
    
    # measure the cohesion of the flock
    def cohesion(self) -> float:
        avg_position = [0, 0]
        for bird in self.birds:
            avg_position[0] += bird.position[0]
            avg_position[1] += bird.position[1]
        avg_position[0] /= len(self.birds)
        avg_position[1] /= len(self.birds)
        cohesion = 0
        for bird in self.birds:
            cohesion += (bird.position[0] - avg_position[0])**2 + (bird.position[1] - avg_position[1])**2
        return cohesion

    # measure the average separation of the flock
    def separation(self) -> float:
        separation = 0
        for bird in self.birds:
            bird_separation = 0
            for neighbour in bird.neighbours:
                separation += distance(bird, neighbour)
            separation += bird_separation / len(bird.neighbours) if bird.neighbours else 0
        return separation / len(self.birds)

    # measure the alignment variance of the flock
    def alignment_variance(self) -> float:
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
    def clusters(self) -> int:
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
                        if distances[j][k] < self.min_distance and not visited[k]:
                            stack.append(k)
        return connected_components
    
    def run_cmd(self, verbose=False):
        # create a csv file to save statistics
        with open('statistics.csv', 'w') as f:
            f.write('cohesion,separation,alignment_variance,clusters\n')
        self.running = True
        while self.running:
            self.update()
            if verbose:
                print(self.__str__())
                # append to csv
                with open('statistics.csv', 'a') as f:
                    f.write(f'{self.cohesion()},{self.separation()},{self.alignment_variance()},{self.clusters()}\n')         
        print(self.__str__())
    
    def __str__(self) -> str:
        # return statistics
        return f'Variance: {self.compute_variance()}, Avg Neighbour Distance: {self.compute_avg_neighbour_distance()}, Avg Neighbours: {self.compute_avg_neighbours()}, Avg Direction: {self.compute_avg_direction()} \n \
            Birds Isolated: {self.birds_isolated}, \tBirds Peripheral: {self.birds_peripheral}, \tBirds Central: {self.birds_central}'

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

        avg_direction = self.compute_avg_direction()
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
        # save the variance history in csv
        with open('variance_history.csv', 'w') as f:
            # write the header
            f.write('variance\n')
            for variance in self.variance_history:
                f.write(f'{variance}\n')
        
        self.running = False
        
