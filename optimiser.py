# an optimiser class to wrap the flock bird class and update the weights 
# there is 3 states : isolated, peripheral, central
# there is 3 weights : w_isolated, w_peripheral, w_central
# there is 3 actions which are the weights
# the optimiser will update the weights based on the state
# the state will be updated based on the number of neighbours
class Optimiser:
    def __init__(self, bird, w_peripheral = [0.4, 0.3, 0.3, 0.0], w_isolated = [0.0, 0.0, 0.0, 1], w_central = [0.3, 0.0, 0.7, 0.0]) -> None:
        self.bird = bird
        self.w_peripheral = w_peripheral
        self.w_isolated = w_isolated
        self.w_central = w_central
        self.state = 'isolated'
        self.actions = {'isolated': self.w_isolated, 'peripheral': self.w_peripheral, 'central': self.w_central}
        self.threshold = 3
        
    def update_state(self):
        if len(self.bird.neighbours) == 0:
            self.state = 'isolated'
        elif len(self.bird.neighbours) < self.threshold:
            self.state = 'peripheral'
        else:
            self.state = 'central'
            
    def update_weights(self):
        self.update_state()
        if self.state == 'isolated':
            self.bird.omega = self.actions['isolated']
        elif self.state == 'peripheral':
            self.bird.omega = self.actions['peripheral']
        else:
            self.bird.omega = self.actions['central']
            
    def __str__(self) -> str:
        return f'State: {self.state}, Weights: {self.bird.omega}'