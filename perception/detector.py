
import random
import time

class ObjectDetector:
    def __init__(self):
        self.known_objects = ["person", "car", "tree", "sign", "dog"]

    def detect(self):
        """Simulates detecting objects in the environment."""
        # For the full cycle demo, we want this to be fast/instant
        # time.sleep(0.2) 
        
        num_objects = random.randint(0, 3)
        detections = []
        for _ in range(num_objects):
            obj = random.choice(self.known_objects)
            dist = round(random.uniform(1.0, 10.0), 2)
            angle = round(random.uniform(-45.0, 45.0), 1)
            detections.append({"class": obj, "distance": dist, "angle": angle})
        return detections

    def detect_obstacles(self, grid_size: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Simulates detecting new obstacles to place on the grid.
        Returns a list of (x, y) coordinates.
        """
        new_obstacles = []
        if random.random() > 0.7: # 30% chance to see something new
            x = random.randint(0, grid_size[0]-1)
            y = random.randint(0, grid_size[1]-1)
            new_obstacles.append((x, y))
        return new_obstacles

def run_demo():
    detector = ObjectDetector()
    print("--- Perception Demo (Object Detection) ---")
    results = detector.detect()
    print(f"Detected: {results}")
    print(f"Grid Obstacles: {detector.detect_obstacles((10,10))}")

if __name__ == "__main__":
    run_demo()
