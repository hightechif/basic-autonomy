
import random
from shared.robot_state import RobotState

class Simple2DLocalizer:
    def __init__(self):
        pass

    def estimate(self, state: RobotState) -> tuple[int, int]:
        """
        In a real system, this would fuse odometry + perception.
        Here, we trust the 'true' state but maybe add a tiny bit of noise logic 
        if we wanted (but for now, let's keep it perfect for the demo).
        """
        # For this basic demo, we assume the robot knows where it is perfectly
        # after moving.
        return (state.x, state.y)

def run_demo():
    print("--- State Estimation Demo (Simple 2D Localizer) ---")
    localizer = Simple2DLocalizer()
    
    # Mocking a robot state
    state = RobotState(x=0, y=0)
    
    path = [(0,0), (1,0), (2,0), (2,1), (3,1)]
    
    for i, pos in enumerate(path):
        state.x, state.y = pos
        estimated_pos = localizer.estimate(state)
        print(f"Step {i}: True Pos {pos} -> Estimated {estimated_pos}")
        
if __name__ == "__main__":
    run_demo()
