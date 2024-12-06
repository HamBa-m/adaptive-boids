from flock import Flock

# Example usage
if __name__ == "__main__":
    flock = Flock(size=100, radius = 400, min_distance=20, max_speed=20, optimizer_threshold=0)
    flock.init_render()
    
    flock.start_render(verbose=True)
    flock.stop_render()
    
    # flock.run_cmd(verbose=True)