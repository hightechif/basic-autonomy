
import random
from enum import Enum, auto
from shared.robot_state import RobotState
from typing import Optional

class BehaviorState(Enum):
    IDLE = auto()
    EXPLORE = auto()
    CHARGE = auto()

class BehaviorAgent:
    def __init__(self):
        self.state = BehaviorState.IDLE
        # Define some fixed locations
        self.charging_station = (0, 0)
        self.explore_targets = [(5, 5), (8, 2), (2, 8), (9, 9)]

    def decide(self, robot_state: RobotState) -> Optional[tuple[int, int]]:
        """
        Decides the next goal based on robot state.
        Returns: (x, y) goal or None (stay/stop).
        """
        # 1. Check Critical Conditions
        if robot_state.battery < 20:
            if self.state != BehaviorState.CHARGE:
                print("!!! BATTERY LOW -> Switching to CHARGE mode.")
                self.state = BehaviorState.CHARGE
                return self.charging_station
            
        # 2. State Logic
        if self.state == BehaviorState.IDLE:
            print("State: IDLE -> Starting EXPLORE.")
            self.state = BehaviorState.EXPLORE
            return random.choice(self.explore_targets)

        elif self.state == BehaviorState.EXPLORE:
            # If we reached the goal?
            if robot_state.current_goal and \
               (robot_state.x, robot_state.y) == robot_state.current_goal:
                print("Target Reached! Picking new target.")
                return random.choice(self.explore_targets)
            
            # If we don't have a goal yet
            if not robot_state.current_goal:
                 return random.choice(self.explore_targets)

        elif self.state == BehaviorState.CHARGE:
            if (robot_state.x, robot_state.y) == self.charging_station:
                print("At Charging Station. Charging...")
                if robot_state.battery >= 100:
                    print("Battery Full! Switching to EXPLORE.")
                    self.state = BehaviorState.EXPLORE
                    return random.choice(self.explore_targets)
                return self.charging_station # Stay here

        return robot_state.current_goal # Maintain current goal

def run_demo():
    agent = BehaviorAgent()
    state = RobotState(x=0, y=0, battery=15)
    print(f"Start: {state}")
    
    goal = agent.decide(state)
    print(f"Decision: Go to {goal}")
