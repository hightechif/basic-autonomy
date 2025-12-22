
import argparse
import sys
import importlib
from enum import Enum
from abc import abstractmethod

class Process(Enum):
    NAV = ("nav", "\n--- Running Localization (Probabilistic State Estimation) Demo ---", "01_probabilistic_state_estimation.grid_world_probability")
    FSM = ("fsm", "\n--- Running Decision Making (Finite State Machine) Demo ---", "02_finite_state_machine.vacuum_agent")
    PLAN = ("plan", "\n--- Running Planning (Path Planning) Demo ---", "03_graph_search_n_path_planning.astar_grid")
    CONTROL = ("control", "\n--- Running Control (PID) Demo ---", "04_control.pid_controller")

    # Type hints for attributes added by __new__
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


def call_module(args: argparse.Namespace, process: Process) -> None:
    print(process.title)
    try:
        module = importlib.import_module(f"{process.path}")
        if hasattr(module, 'run_demo'):
                module.run_demo()
        else:
            print("Error: The module does not have a run_demo() function yet.")
    except ImportError as e:
        print(f"Error importing {module} module: {e}")
        return

def main() -> None:
    parser = argparse.ArgumentParser(description="Basic Autonomy Robotics Demos")
    parser.add_argument("--module", "-m", type=str, choices=[process.value for process in Process], required=True,
                        help="Which module demo to run: 'nav' (Localization), 'fsm' (Decision), 'plan' (Planning), 'control' (Control)")
    
    args = parser.parse_args()

    match args.module:
        case Process.NAV.value:
            call_module(args, Process.NAV)
        case Process.FSM.value:
            call_module(args, Process.FSM)
        case Process.PLAN.value:
            call_module(args, Process.PLAN)
        case Process.CONTROL.value:
            call_module(args, Process.CONTROL)

if __name__ == "__main__":
    main()
