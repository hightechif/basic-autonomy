# 1D Grid Localization (Histogram Filter)

# World definition: 1D line of cells
# Let's say we have 10 cells, with some landmarks (colors)
# 'G' = Green, 'R' = Red
world = ['G', 'R', 'R', 'G', 'G', 'R', 'G', 'G', 'G', 'R']

# Initial belief: Uniform distribution (1/10 for each cell)
p = [0.1] * len(world)

# Sensor noise
pHit = 0.6
pMiss = 0.2

# Motion noise
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    """
    Updates belief p based on measurement Z.
    P(X|Z) = P(Z|X) * P(X) / P(Z)
    """
    q = []
    for i in range(len(p)):
        hit = (Z == world[i])
        # Multiplier depends on whether the measurement matches the world at this cell
        multiplier = pHit if hit else pMiss
        q.append(p[i] * multiplier)
    
    # Normalize
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q

def move(p, U):
    """
    Updates belief p based on motion U.
    Convolution / Total Probability
    """
    q = []
    for i in range(len(p)):
        # Calculate the probability that the robot ends up in cell i
        # derived from previous cells (i-U)
        
        # Exact move from (i-U)
        s = pExact * p[(i - U) % len(p)]
        
        # Overshoot from (i-U-1)
        s += pOvershoot * p[(i - U - 1) % len(p)]
        
        # Undershoot from (i-U+1)
        s += pUndershoot * p[(i - U + 1) % len(p)]
        
        q.append(s)
    return q

def print_distribution(p):
    # Print formatted probabilities
    formatted = ["{:.3f}".format(x) for x in p]
    print(" ".join(formatted))

def run_simulation():
    global p
    
    print("Initial Distribution:")
    print_distribution(p)
    
    # Motions and Measurements sequence
    # U=1 means move 1 cell right
    # Z='G' means sensor sees Green
    measurements = ['G', 'R', 'R', 'G']
    motions = [1, 1, 1, 1]
    
    for k in range(len(measurements)):
        # 1. Move (Predict)
        p = move(p, motions[k])
        print(f"\n--- Step {k+1}: Moved {motions[k]} ---")
        print_distribution(p)
        
        # 2. Sense (Update)
        p = sense(p, measurements[k])
        print(f"--- Step {k+1}: Sensed '{measurements[k]}' ---")
        print_distribution(p)

        # Identify most likely position
        max_p = max(p)
        best_indices = [i for i, x in enumerate(p) if x == max_p]
        print(f"Most likely position(s): {best_indices} with prob {max_p:.3f}")

if __name__ == "__main__":
    print(f"World: {world}")
    run_simulation()
