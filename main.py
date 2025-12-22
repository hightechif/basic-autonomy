
import argparse
import sys
import time
import importlib
from enum import Enum
from shared.robot_state import RobotState

# Import modules (assuming refactored structure)
from perception.detector import ObjectDetector
from state_estimation.simple_2d_filter import Simple2DLocalizer
from behavior.vacuum_agent import BehaviorAgent
from planning.astar_grid import AStarPlanner, print_grid

class Process(Enum):
    FULL_CYCLE = ("full_cycle", "\n--- Running Full Autonomy Cycle ---", "main")
    PERCEPTION = ("perception", "\n--- Running Perception (Object Detection) Demo ---", "perception.detector")
    ESTIMATION = ("estimation", "\n--- Running State Estimation (2D Mock) Demo ---", "state_estimation.simple_2d_filter")
    BEHAVIOR = ("behavior", "\n--- Running Behavior (Finite State Machine) Demo ---", "behavior.vacuum_agent")
    PLANNING = ("planning", "\n--- Running Planning (Graph Search) Demo ---", "planning.astar_grid")

    # Type hints
    title: str
    path: str

    def __new__(cls, value: str, title: str, path: str) -> 'Process':
        obj = object.__new__(cls)
        obj._value_ = value
        obj.title = title
        obj.path = path
        return obj
    
    def __init__(self, value: str, title: str, path: str) -> None:
        pass

def run_full_cycle_demo():
    print("Initializing Autonomy Stack...")
    
    # 1. Initialize Components
    perception = ObjectDetector()
    estimation = Simple2DLocalizer()
    behavior = BehaviorAgent()
    
    # Initialize Map (10x10 empty grid)
    grid_size = (10, 10)
    grid = [[0 for _ in range(grid_size[1])] for _ in range(grid_size[0])]
    # Add some static obstacles
    grid[3][3] = 1; grid[3][4] = 1; grid[4][3] = 1
    
    planner = AStarPlanner(grid)
    
    # Initialize State
    robot_state = RobotState(x=0, y=0, battery=100, map_size=grid_size)
    
    print("\n--- STARTING AUTONOMY LOOP ---")
    
    for step in range(20):
        print(f"\n[Step {step+1}] Mode: {behavior.state.name} | Pos: ({robot_state.x}, {robot_state.y}) | Batt: {robot_state.battery}%")
        
        # --- 1. WORLD SIMULATION (Robotics Layer) ---
        # Simulate moving along the path if we have one
        if robot_state.current_path and len(robot_state.current_path) > 0:
            next_pos = robot_state.current_path.pop(0) # Move to next step
            robot_state.x, robot_state.y = next_pos
            print(f"  -> Robotics: Moved to {next_pos}")
            # Battery drain
            robot_state.battery -= 2
        
        if behavior.state.name == "CHARGE" and (robot_state.x, robot_state.y) == (0,0):
             robot_state.battery = min(100, robot_state.battery + 20)
             print(f"  -> Robotics: Charging... ({robot_state.battery}%)")

        # --- 2. PERCEPTION ---
        # Detect obstacles (updates map)
        new_obs = perception.detect_obstacles(grid_size)
        if new_obs:
            for ox, oy in new_obs:
                if (ox, oy) != (robot_state.x, robot_state.y): # Don't spawn on robot
                    print(f"  -> Perception: New Obstacle at ({ox}, {oy})")
                    grid[ox][oy] = 1
                    planner.grid = grid # Update planner's map

        # --- 3. STATE ESTIMATION ---
        # Update belief (trivial here)
        robot_state.x, robot_state.y = estimation.estimate(robot_state)
        
        # --- 4. BEHAVIOR ---
        # Decide Goal
        previous_goal = robot_state.current_goal
        robot_state.current_goal = behavior.decide(robot_state)
        
        if robot_state.current_goal != previous_goal:
             print(f"  -> Behavior: New Goal Selected: {robot_state.current_goal}")
             robot_state.current_path = None # Trigger replan

        # --- 5. PLANNING ---
        # If we have a goal but no path (or blocked path), plan
        if robot_state.current_goal and not robot_state.current_path and (robot_state.x, robot_state.y) != robot_state.current_goal:
            print(f"  -> Planning: Calculating path to {robot_state.current_goal}...")
            path = planner.plan((robot_state.x, robot_state.y), robot_state.current_goal)
            if path:
                robot_state.current_path = path[1:] # Skip current start pos
                print(f"  -> Planning: Path found ({len(robot_state.current_path)} steps)")
            else:
                print("  -> Planning: MOVEMENT BLOCKED! (No path)")
                # Force behavior to pick new goal next time?
                robot_state.current_goal = None
        
        time.sleep(0.5)

def call_module(args: argparse.Namespace, process: Process) -> None:
    print(process.title)
    if process == Process.FULL_CYCLE:
        run_full_cycle_demo()
        return

    try:
        module = importlib.import_module(f"{process.path}")
        if hasattr(module, 'run_demo'):
                module.run_demo()
        else:
            print("Error: The module does not have a run_demo() function yet.")
    except ImportError as e:
        print(f"Error importing {process.path} module: {e}")
        return

def main() -> None:
    parser = argparse.ArgumentParser(description="Basic Autonomy Robotics Demos")
    parser.add_argument("--module", "-m", type=str, choices=[process.value for process in Process], required=True,
                        help="Which module demo to run: 'full_cycle', 'perception', 'estimation', 'behavior', 'planning'")
    
    args = parser.parse_args()

    match args.module:
        case Process.FULL_CYCLE.value:
            call_module(args, Process.FULL_CYCLE)
        case Process.PERCEPTION.value:
            call_module(args, Process.PERCEPTION)
        case Process.ESTIMATION.value:
            call_module(args, Process.ESTIMATION)
        case Process.BEHAVIOR.value:
            call_module(args, Process.BEHAVIOR)
        case Process.PLANNING.value:
            call_module(args, Process.PLANNING)

if __name__ == "__main__":
    main()
