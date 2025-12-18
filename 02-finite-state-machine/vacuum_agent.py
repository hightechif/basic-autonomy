import random
import time
from enum import Enum, auto

class VacuumState(Enum):
    CLEAN = auto()
    CHARGE = auto()
    STUCK = auto()

class VacuumCleaner:
    def __init__(self):
        self.state = VacuumState.CLEAN
        self.battery = 100
        self.steps_stuck = 0

    def step(self, sensors):
        """
         transitions based on sensor data:
         - sensors['battery_level']: int (0-100)
         - sensors['bumper_hit']: bool
        """
        battery = sensors.get('battery_level', 0)
        bumper = sensors.get('bumper_hit', False)
        
        print(f"Current State: {self.state.name}, Battery: {battery}, Bumper: {bumper}")

        if self.state == VacuumState.CLEAN:
            if bumper:
                print(" -> Bumper hit! Switching to STUCK.")
                self.state = VacuumState.STUCK
                self.steps_stuck = 0
            elif battery < 20:
                print(" -> Low battery! Switching to CHARGE.")
                self.state = VacuumState.CHARGE
            else:
                print(" -> Cleaning...")
                
        elif self.state == VacuumState.STUCK:
            self.steps_stuck += 1
            if self.steps_stuck > 2:
                print(" -> Wigged free! Switching back to CLEAN.")
                self.state = VacuumState.CLEAN
            else:
                print(" -> Still stuck, trying to maneuver...")

        elif self.state == VacuumState.CHARGE:
            if battery >= 90:
                print(" -> Fully charged! Switching back to CLEAN.")
                self.state = VacuumState.CLEAN
            else:
                print(" -> Charging...")

def run_simulation(steps=15):
    bot = VacuumCleaner()
    
    # Simulating a scenario
    # 0-4: Normal cleaning, battery draining
    # 5: Bumper hit -> Stuck
    # 6-8: Stuck processing
    # 9-: Low battery -> Charge
    
    current_battery = 100
    
    for i in range(steps):
        print(f"\n--- Step {i+1} ---")
        
        # Fake sensor generation
        is_bumper_hit = False
        
        # Simulate battery drain
        if bot.state != VacuumState.CHARGE:
            current_battery -= 5
        else:
            current_battery += 20 # Fast charge
            
        current_battery = max(0, min(100, current_battery))
        
        # Invoke a stuck situation at step 5
        if i == 4: 
            is_bumper_hit = True
            
        # Force low battery scenario later if not already low
        if i >= 10 and bot.state == VacuumState.CLEAN:
             current_battery = 15

        sensors = {
            'battery_level': current_battery,
            'bumper_hit': is_bumper_hit
        }
        
        bot.step(sensors)
        time.sleep(0.5)

if __name__ == "__main__":
    run_simulation()
