from flock import Flock

# Example usage
if __name__ == "__main__":
    flock = Flock(size=100, min_distance=20, max_speed=40)
    flock.init_render()
    
    # flock.start_render(verbose=True)
    # flock.stop_render()
    
    flock.run_cmd(verbose=True)