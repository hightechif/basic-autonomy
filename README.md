# Basic Autonomy

This repository contains fundamental implementations of the core components required for basic autonomy. It breaks down the cycle into three distinct projects, each mapping to a critical subsystem of autonomous system architecture: Localization, Decision Making, and Planning.

```ascii

                 +-----------------------------+
                 |        THE REAL WORLD       |
                 |  (Static + Dynamic Objects) |
                 +--------------+--------------+
                                |
                                |  Exteroceptive Data
                                |  (LiDAR / Camera / Depth)
                                v
    +================================================================+
    |                    AUTONOMY LAYER                              |
    |              (Decision-Making Brain ~5–20 Hz)                  |
    |                                                                |
    |  [ Perception ]                                                |
    |    - Object Detection                                          |
    |    - Free Space Estimation                                     |
    |    - Semantic Understanding                                    |
    |           |                                                    |
    |           v                                                    |
    |  [ State Estimation / SLAM ]  <---- Coupled Estimation ---->   |
    |    - Localization (Where am I?)                                |
    |    - Mapping (What’s around me?)                               |
    |           |                                                    |
    |           v                                                    |
    |  [ Behavior / Decision Making ]                                |
    |    - Goal selection                                            |
    |    - Mode switching (follow, avoid, stop)                      |
    |           |                                                    |
    |           v                                                    |
    |  [ Planning ]                                                  |
    |    - Global Path (A*, RRT*)                                    |
    |    - Local Trajectory (MPC, DWA, RL)                           |
    |                                                                |
    +============================+===================================+
                                 |
                                 |  Intent / Setpoints
                                 |  (v, ω, trajectory, waypoints)
                                 v
    +============================+===================================+
    |                     ROBOTICS LAYER                             |
    |                (Physical Execution Body ~100–1000 Hz)          |
    |                                                                |
    |  [ Control ]                                                   |
    |    - PID / LQR / MPC                                           |
    |    - Low-level stabilization                                   |
    |           |                                                    |
    |           v                                                    |
    |  [ Actuators ]                                                 |
    |    - Motors / Wheels / Joints                                  |
    |           |                                                    |
    |           v                                                    |
    |  [ Physical Motion ]                                           |
    |           |                                                    |
    |           v                                                    |
    |  [ Proprioceptive Sensors ]                                    |
    |    - Encoders                                                  |
    |    - IMU                                                       |
    |           |                                                    |
    |           v                                                    |
    |  [ State Feedback ]                                            |
    |           |                                                    |
    |           +--------------------> back to [ Control ]           |
    |                                                                |
    |   ( Fast Reflex Loop: Control → Motion → Sensing → Control )   |
    |                                                                |
    +================================================================+

```

## System Architecture

The autonomy stack focuses on the **Autonomy** layer (The Brain) as illustrated above.

### [ AUTONOMY ]
Higher-level processing that answers *"What should I do?"* and *"Where should I go?"*.

| Subsystem | Function | Robot Question | Algo/Implementation |
| :--- | :--- | :--- | :--- |
| **State Estimation / SLAM** | Localization & Mapping | *"Where am I?"* | Probabilistic Filters (Kalman/Particle) |
| **Behavior / Decision Making** | Mission Executive | *"What should I do next?"* | Finite State Machine (FSM) |
| **Planning** | Path Planning | *"How do I get there?"* | Global (A*, RRT*) & Local (MPC, DWA) |

---

## The Workflow Loop

1.  **Sense & Estimate (State Estimation / SLAM)**
    The robot processes exteroceptive data (LiDAR, Camera) to perceive the environment (Object Detection, Free Space). It then uses probabilistic algorithms (in `probabilistic-state-estimation`) to filter noise and determine its most likely position (**Localization**) and build a map of its surroundings (**Mapping**).

2.  **Decide (Behavior / Decision Making)**
    Based on the internal state (e.g., battery level) and external state (completed tasks), the **Finite State Machine** (in `finite-state-machine`) selects the current goal and switches modes (e.g., `Follow`, `Avoid`, `Stop`).

3.  **Plan (Planning)**
    Once a goal is selected, the planner (in `graph-search-n-path-planning`) calculates the optimal route. This involves **Global Planning** (finding a path across the map, e.g., A*) and **Local Trajectory** generation (avoiding immediate obstacles, e.g., DWA/MPC).
    
    *--- Autonomy boundary: Command sent to Controller ---*

---

## Projects Overview

### [ AUTONOMY ]

### 1. `01_probabilistic_state_estimation` (State Estimation / SLAM)
Implements the localization and mapping system.
-   **Goal**: Accurate determination of the robot's pose and environment map.
-   **Context**: Coupled estimation is required to localize within a map while simultaneously building it (SLAM).
-   **Key Concepts**: Bayes Filters, Kalman Filters, Particle Filters, Sensor Fusion.

### 2. `02_finite_state_machine` (Behavior / Decision Making)
Implements the high-level decision-making brain.
-   **Goal**: Management of robot behaviors and mode switching.
-   **Context**: A robot needs to switch behaviors (e.g., from `Goal Seeking` to `Obstacle Avoidance`) based on perception and state.
-   **Key Concepts**: States, Transitions, Events, Goal Selection.

### 3. `03_graph_search_n_path_planning` (Planning)
Implements global and local trajectory generation.
-   **Goal**: Find the shortest global path and feasible local trajectory.
-   **Context**: The robot needs a global route (A*) and a local command (MPC/DWA) to follow that route while reacting to dynamic obstacles.
-   **Key Concepts**: Grid Maps, A* (Global), MPC/DWA (Local), Heuristics.

---

## How to Run

This project now uses a unified CLI entry point `main.py`. You can run demos for each subsystem independently:

### Localization Demo
Runs the 1D Histogram Filter simulation.
```bash
python main.py --module nav
```

### Decision Making Demo
Runs the Vacuum Cleaner FSM agent.
```bash
python main.py --module fsm
```

### Planning Demo
Runs the A* Path Planner on a grid map.
```bash
python main.py --module plan
```
