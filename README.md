# Basic Autonomy

This repository contains fundamental implementations of the core components required for basic autonomy. It breaks down the cycle into three distinct projects, each mapping to a critical subsystem of autonomous system architecture: Localization, Decision Making, and Planning.

```text
                  +-------------------------+
                  |     THE REAL WORLD      | <-----------------------+
                  +------------+------------+                         |
                               |                                      |
                               | (Visual/Depth Data)                  |
                               v                                      |
       +=================================================+            |
       |  AUTONOMY LAYER  (The Brain: ~10 Hz)            |            |
       |                                                 |            |
       |  [ Exteroceptive Sensors (LiDAR/Camera) ]       |            |
       |                   |                             |            |
       |                   v                             |            |
       |             [ Perception ]                      |            |
       |                   |                             |            |
       |                   v                             |            |
       |  [ Localization ] <-----> [ Mapping ]           |            |
       |                   |                             |            |
       |                   v                             |            |
       |              [ Planning ]                       |            |
       |                                                 |            |
       +===================+=============================+            |
                           |                                          |
                           | Command (e.g., Velocity: 0.5 m/s)        |
                           v                                          |
       +===================+=============================+            |
       |  ROBOTICS LAYER  (The Body: ~1000 Hz)           |            |
       |                                                 |            |
       |         +----> [ Control / PID ]                |            |
       |         |             |                         |            |
       |         |             v                         |            |
       |         |      [   Actuators   ]                |            |
       |  (Fast  |             |                         |            |
       |  Reflex |             v                         |            |
       |  Loop)  |      [ Physical Motion ] -------------+------------+
       |         |             |
       |         |             v
       |         +----- [ Proprioceptive Sensors ]
       |                  (Encoders / IMU)
       |
       +=================================================+
```

## System Architecture

The autonomy stack focuses on the **Autonomy** layer (The Brain) as illustrated above.

### [ AUTONOMY ]
Higher-level processing that answers *"What should I do?"* and *"Where should I go?"*.

| Subsystem | Function | Robot Question | Algo/Implementation |
| :--- | :--- | :--- | :--- |
| **Localization** | State Estimation | *"Where am I?"* | Probabilistic Filters (Kalman/Particle) |
| **Decision Making** | Mission Executive | *"What should I do next?"* | Finite State Machine (FSM) |
| **Planning** | Path Planning | *"How do I get there?"* | Graph Search (A*, Dijkstra) |

---

## The Workflow Loop

1.  **Sense & Estimate (Localization)**
    The robot reads sensor data (lidar, encoders, IMU) which is noisy. It uses probabilistic algorithms (in `probabilistic-state-estimation`) to filter this noise and determine its most likely position and orientation in the world.

2.  **Decide (Decision Making)**
    Based on the internal state (e.g., battery level) and external state (completed tasks), the **Finite State Machine** (in `finite-state-machine`) decides the current high-level mode (e.g., `IDLE`, `NAVIGATING`, `CHARGING`).

3.  **Plan (Planning)**
    Once a target is decided (e.g., "Go to Charging Station"), the planner (in `graph-search-n-path-planning`) calculates the optimal route from the current estimated position (from step 1) to the target, avoiding known obstacles.
    
    *--- Autonomy boundary: Command sent to Controller ---*

---

## Projects Overview

### [ AUTONOMY ]

### 1. `01_probabilistic_state_estimation` (Localization)
Implements the localization system.
-   **Goal**: Accurate determination of the robot's pose (position + orientation).
-   **Context**: Sensors are imperfect. We can't just trust raw data. We must fuse sensor readings with a motion model to estimate the truth.
-   **Key Concepts**: Bayes Filters, Kalman Filters, Particle Filters, Sensor Fusion.

### 2. `02_finite_state_machine` (Decision Making)
Implements the high-level logic controller.
-   **Goal**: Management of robot behavior.
-   **Context**: A robot needs to switch behaviors based on triggers (e.g., if `battery < 20%`, switch to `Charge` state).
-   **Key Concepts**: States, Transitions, Events.

### 3. `03_graph_search_n_path_planning` (Planning)
Implements the trajectory generator.
-   **Goal**: Find the shortest/safest path from point A to point B.
-   **Context**: The robot has a map and knows where it is (thanks to Estimation), but needs to find a valid route through the free space.
-   **Key Concepts**: Grid Maps, Graphs, A* Algorithm, Dijkstra, Heuristics.

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
