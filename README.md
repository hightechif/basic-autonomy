# Basic Autonomy

This repository contains fundamental implementations of the core components required for mobile robot autonomy. It breaks down the "See-Think-Act" cycle into three distinct projects, each mapping to a critical subsystem of robotic architecture: Decision Making, Navigation, and Guidance.

## System Architecture

The autonomy stack is organized into a hierarchical loop. The robot continuously estimates its state, decides on a high-level goal, and calculates a path to reach that goal.

| Subsystem | Function | Robot Question | Algo/Implementation |
| :--- | :--- | :--- | :--- |
| **Navigation** | State Estimation | *"Where am I?"* | Probabilistic Filters (Kalman/Particle) |
| **Decision Making** | Mission Executive | *"What should I do next?"* | Finite State Machine (FSM) |
| **Guidance** | Path Planning | *"How do I get there?"* | Graph Search (A*, Dijkstra) |
| **Control** | Actuation | *"How do I steer?"* | PID, MPC, LQR |

---

## The Workflow Loop

1.  **Sense & Estimate (Navigation)**
    The robot reads sensor data (lidar, encoders, IMU) which is noisy. It uses probabilistic algorithms (in `probabilistic-state-estimation`) to filter this noise and determine its most likely position and orientation in the world.

2.  **Decide (Decision Making)**
    Based on the internal state (e.g., battery level) and external state (completed tasks), the **Finite State Machine** (in `finite-state-machine`) decides the current high-level mode (e.g., `IDLE`, `NAVIGATING`, `CHARGING`).

3.  **Plan (Guidance)**
    Once a target is decided (e.g., "Go to Charging Station"), the planner (in `graph-search-n-path-planning`) calculates the optimal route from the current estimated position (from step 1) to the target, avoiding known obstacles.

4.  **Act (Control)**
    The planner gives a reference path, but physics (friction, inertia) prevents perfect following. The **Controller** (in `control`) calculates the precise motor voltage/torque needed to minimize the error between the robot's actual position and the desired path.

---

## Projects Overview

### 1. `01_probabilistic_state_estimation` (Navigation)
Implements the localization system.
-   **Goal**: Accurate determination of the robot's pose (position + orientation).
-   **Context**: Sensors are imperfect. We can't just trust raw data. We must fuse sensor readings with a motion model to estimate the truth.
-   **Key Concepts**: Bayes Filters, Kalman Filters, Particle Filters, Sensor Fusion.

### 2. `02_finite_state_machine` (Decision Making)
Implements the high-level logic controller.
-   **Goal**: Management of robot behavior.
-   **Context**: A robot needs to switch behaviors based on triggers (e.g., if `battery < 20%`, switch to `Charge` state).
-   **Key Concepts**: States, Transitions, Events.

### 3. `03_graph_search_n_path_planning` (Guidance)
Implements the trajectory generator.
-   **Goal**: Find the shortest/safest path from point A to point B.
-   **Context**: The robot has a map and knows where it is (thanks to Estimation), but needs to find a valid route through the free space.
-   **Key Concepts**: Grid Maps, Graphs, A* Algorithm, Dijkstra, Heuristics.

### 4. `04_control` (Control)
Implements the loop closure.
-   **Goal**: Execute the planned trajectory by driving the actuators.
-   **Context**: Knowing the path is not enough; we need to correct errors in real-time (e.g., drifting due to friction) to stay on that path.
-   **Key Concepts**: PID Controllers, Feedback Loops, Error Correction.

---

## How to Run

This project now uses a unified CLI entry point `main.py`. You can run demos for each subsystem independently:

### Navigation Demo
Runs the 1D Histogram Filter simulation.
```bash
python main.py --module nav
```

### Decision Making Demo
Runs the Vacuum Cleaner FSM agent.
```bash
python main.py --module fsm
```

### Path Planning Demo
Runs the A* Path Planner on a grid map.
```bash
python main.py --module plan
```

### Control Demo
Runs the PID Controller simulation.
```bash
python main.py --module control
```
