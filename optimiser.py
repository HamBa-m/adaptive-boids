# an optimiser class to wrap the flock bird class and update the weights 
# there is 2 states : isolated, and connected
# there is 2 weights : w_isolated, w_connected
# there is 2 actions which are the weights
# the optimiser will update the weights based on the state
# the state will be updated based on the number of neighbours
class Optimiser:
    def __init__(self, bird, threshold = 3, w_isolated = [0.0, 0.0, 0.0, 1], w_connected = [0.5, 0.1, 0.4, 0.0]) -> None:
        self.bird = bird
        self.w_isolated = w_isolated
        self.w_connected = w_connected
        self.state = 'isolated'
        self.actions = {'isolated': self.w_isolated, 'connected': self.w_connected}
        self.threshold = threshold
        
    def update_state(self):
        if len(self.bird.neighbours) < self.threshold:
            self.state = 'isolated'
        else:
            self.state = 'connected'
            
    def update_weights(self):
        self.update_state()
        if self.state == 'isolated':
            self.bird.omega = self.actions['isolated']
        else:
            self.bird.omega = self.actions['connected']
            
    def __str__(self) -> str:
        return f'State: {self.state}, Weights: {self.bird.omega}'