import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start
        self.h = 0  # Heuristic to end
        self.f = 0  # Total cost

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.position == other.position

class AStarPlanner:
    def __init__(self, grid):
        """
        grid: 2D list where 0 is empty, 1 is obstacle
        """
        self.grid = grid
        self.width = len(grid)
        self.height = len(grid[0])

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, position):
        neighbors = []
        x, y = position
        # 4-way connectivity
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors

    def plan(self, start, end):
        start_node = Node(start)
        end_node = Node(end)
        
        open_list = []
        closed_list = [] # Ideally use a set for closed list for O(1) lookup, but need robust hashing for Node
        # Using a dictionary for closed_set is better: key=pos, value=g_cost
        closed_set = {}
        
        heapq.heappush(open_list, start_node)
        
        # Keep track of best g seen so far
        g_scores = {start: 0}

        while open_list:
            current_node = heapq.heappop(open_list)
            
            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path
            
            for child_pos in self.get_neighbors(current_node.position):
                # Check for obstacle
                if self.grid[child_pos[0]][child_pos[1]] == 1:
                    continue
                
                tentative_g = current_node.g + 1
                
                if child_pos in closed_set and tentative_g >= closed_set[child_pos]:
                    continue
                    
                if tentative_g < g_scores.get(child_pos, float('inf')):
                    child_node = Node(child_pos, current_node)
                    child_node.g = tentative_g
                    child_node.h = self.heuristic(child_node.position, end_node.position)
                    child_node.f = child_node.g + child_node.h
                    
                    heapq.heappush(open_list, child_node)
                    g_scores[child_pos] = tentative_g
                    closed_set[child_pos] = tentative_g
            
        return None

def print_grid(grid, path=None, start=None, end=None):
    for x in range(len(grid)):
        line = ""
        for y in range(len(grid[0])):
            pos = (x, y)
            if pos == start:
                line += "S "
            elif pos == end:
                line += "E "
            elif path and pos in path:
                line += "+ "
            elif grid[x][y] == 1:
                line += "# "
            else:
                line += ". "
        print(line)

def run_demo():
    # 0 = Empty, 1 = Obstacle
    grid = [
        [0, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    planner = AStarPlanner(grid)
    start = (0, 0)
    end = (5, 5)

    print("Grid Map:")
    print_grid(grid, start=start, end=end)
    
    path = planner.plan(start, end)
    
    if path:
        print(f"\nPath Found! Length: {len(path)}")
        print_grid(grid, path, start, end)
    else:
        print("\nNo path found.")

if __name__ == "__main__":
    run_demo()
