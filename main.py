
import argparse
import sys
import importlib

def main():
    parser = argparse.ArgumentParser(description="Basic Autonomy Robotics Demos")
    parser.add_argument("--module", "-m", type=str, choices=["nav", "fsm", "plan", "control"], required=True,
                        help="Which module demo to run: 'nav' (Navigation), 'fsm' (Decision), 'plan' (Guidance), 'control' (Control)")
    
    args = parser.parse_args()
    

    if args.module == "nav":
        print("\n--- Running Navigation (Probabilistic State Estimation) Demo ---")
        module = importlib.import_module("01_probabilistic_state_estimation.grid_world_probability")
        module.run_demo()
        
    elif args.module == "fsm":
        print("\n--- Running Decision Making (Finite State Machine) Demo ---")
        try:
             module = importlib.import_module("02_finite_state_machine.vacuum_agent")
             if hasattr(module, 'run_demo'):
                 module.run_demo()
             else:
                 print("Error: The FSM module does not have a run_demo() function yet.")
        except ImportError as e:
             print(f"Error importing FSM module: {e}")
             return
        
    elif args.module == "plan":
        print("\n--- Running Guidance (Path Planning) Demo ---")
        module = importlib.import_module("03_graph_search_n_path_planning.astar_grid")
        module.run_demo()
        
    elif args.module == "control":
        print("\n--- Running Control (PID) Demo ---")
        module = importlib.import_module("04_control.pid_controller")
        module.run_demo()

if __name__ == "__main__":
    main()
