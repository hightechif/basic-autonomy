
class HistogramFilter:
    def __init__(self, world, pHit=0.6, pMiss=0.2, pExact=0.8, pOvershoot=0.1, pUndershoot=0.1):
        """
        Initializes the Histogram Filter (1D Grid Localization).
        
        Args:
            world (list): List of landmarks/colors representing the world map.
            pHit (float): Probability of sensor reading matching the world.
            pMiss (float): Probability of sensor reading NOT matching (1 - pHit).
            pExact (float): Probability of exact movement.
            pOvershoot (float): Probability of moving one extra step.
            pUndershoot (float): Probability of moving one less step.
        """
        self.world = world
        self.pHit = pHit
        self.pMiss = pMiss
        self.pExact = pExact
        self.pOvershoot = pOvershoot
        self.pUndershoot = pUndershoot
        self.p = [1.0 / len(world)] * len(world) # Uniform initial distribution

    def sense(self, measurement):
        """
        Updates belief based on measurement Z (Bayes Rule).
        """
        q = []
        for i in range(len(self.p)):
            hit = (measurement == self.world[i])
            multiplier = self.pHit if hit else self.pMiss
            q.append(self.p[i] * multiplier)
        
        # Normalize
        s = sum(q)
        self.p = [val / s for val in q]
        return self.p

    def move(self, u):
        """
        Updates belief based on motion u (Total Probability).
        """
        q = []
        for i in range(len(self.p)):
            # Exact move from (i-u)
            s = self.pExact * self.p[(i - u) % len(self.p)]
            # Overshoot from (i-u-1)
            s += self.pOvershoot * self.p[(i - u - 1) % len(self.p)]
            # Undershoot from (i-u+1)
            s += self.pUndershoot * self.p[(i - u + 1) % len(self.p)]
            q.append(s)
        self.p = q
        return self.p

    def get_distribution(self):
        return self.p

    def get_most_likely_position(self):
        max_p = max(self.p)
        indices = [i for i, x in enumerate(self.p) if x == max_p]
        return indices, max_p

def run_demo():
    # World definition
    world = ['G', 'R', 'R', 'G', 'G', 'R', 'G', 'G', 'G', 'R']
    print(f"World Map: {world}")
    
    hf = HistogramFilter(world)
    
    print("\nInitial Distribution:")
    print(["{:.3f}".format(x) for x in hf.get_distribution()])
    
    measurements = ['G', 'R', 'R', 'G']
    motions = [1, 1, 1, 1]
    
    for k in range(len(measurements)):
        # 1. Move
        hf.move(motions[k])
        print(f"\n--- Step {k+1}: Moved {motions[k]} ---")
        
        # 2. Sense
        hf.sense(measurements[k])
        print(f"--- Step {k+1}: Sensed '{measurements[k]}' ---")
        
        dist = hf.get_distribution()
        print(" ".join(["{:.3f}".format(x) for x in dist]))
        
        indices, prob = hf.get_most_likely_position()
        print(f"Most likely: {indices} (prob {prob:.3f})")

if __name__ == "__main__":
    run_demo()
