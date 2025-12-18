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

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(position, grid_size):
    neighbors = []
    x, y = position
    # 4-way connectivity
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size[0] and 0 <= ny < grid_size[1]:
            neighbors.append((nx, ny))
    return neighbors

def astar(grid, start, end):
    """
    grid: 2D list where 0 is empty, 1 is obstacle
    start: (x, y) tuple
    end: (x, y) tuple
    """
    start_node = Node(start)
    end_node = Node(end)
    
    open_list = []
    closed_list = []
    
    heapq.heappush(open_list, start_node)
    
    grid_w = len(grid)
    grid_h = len(grid[0])
    
    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)
        
        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path
        
        children = get_neighbors(current_node.position, (grid_w, grid_h))
        
        for child_pos in children:
            # Check for obstacle
            if grid[child_pos[0]][child_pos[1]] == 1:
                continue
                
            child_node = Node(child_pos, current_node)
            
            # Check if in closed list using position check to be safe
            if any(child.position == child_node.position for child in closed_list):
                 continue

            child_node.g = current_node.g + 1
            child_node.h = heuristic(child_node.position, end_node.position)
            child_node.f = child_node.g + child_node.h
            
            # Check if in open list with a lower g value
            if any(open_node.position == child_node.position and child_node.g > open_node.g for open_node in open_list):
                continue
                
            heapq.heappush(open_list, child_node)
            
    return None

def print_grid(grid, path, start, end):
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
    grids = [
        [
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 0]
        ],
    ]

    for i, grid in enumerate(grids):
        start = (0, 0)
        end = (5, 5)
        
        print("Finding path from (0,0) to (5,5)...")
        
        print(f"Grid {i+1}")
        print("-" * 20)
        print_grid(grid, None, start, end)
        print(  "-" * 20)

        path = astar(grid, start, end)
        
        if path:
            print(f"Path found! Length: {len(path)}")
            print_grid(grid, path, start, end)
        else:
            print("No path found.")
        print("\n")

if __name__ == "__main__":
    run_demo()
