# Basic Autonomy

This repository contains fundamental implementations of the core components required for mobile robot autonomy. It breaks down the "See-Think-Act" cycle into three distinct projects, each mapping to a critical subsystem of robotic architecture: Decision Making, Navigation, and Guidance.

## System Architecture

The autonomy stack is organized into a hierarchical loop. The robot continuously estimates its state, decides on a high-level goal, and calculates a path to reach that goal.

| Subsystem | Function | Robot Question | Algo/Implementation |
| :--- | :--- | :--- | :--- |
| **Navigation** | State Estimation | *"Where am I?"* | Probabilistic Filters (Kalman/Particle) |
| **Decision Making** | Mission Executive | *"What should I do next?"* | Finite State Machine (FSM) |
| **Guidance** | Path Planning | *"How do I get there?"* | Graph Search (A*, Dijkstra) |

---

## The Workflow Loop

1.  **Sense & Estimate (Navigation)**
    The robot reads sensor data (lidar, encoders, IMU) which is noisy. It uses probabilistic algorithms (in `probabilistic-state-estimation`) to filter this noise and determine its most likely position and orientation in the world.

2.  **Decide (Decision Making)**
    Based on the internal state (e.g., battery level) and external state (completed tasks), the **Finite State Machine** (in `finite-state-machine`) decides the current high-level mode (e.g., `IDLE`, `NAVIGATING`, `CHARGING`).

3.  **Plan (Guidance)**
    Once a target is decided (e.g., "Go to Charging Station"), the planner (in `graph-search-n-path-planning`) calculates the optimal route from the current estimated position (from step 1) to the target, avoiding known obstacles.

*(Note: The final step, **Control**, which actively steers the motors to follow this generated path, sits downstream of this stack.)*

---

## Projects Overview

### 1. `01-probabilistic-state-estimation` (Navigation)
Implements the localization system.
-   **Goal**: accurately determine the robot's pose (position + orientation).
-   **Context**: Sensors are imperfect. We can't just trust raw data. We must fuse sensor readings with a motion model to estimate the truth.
-   **Key Concepts**: BAYES Filters, Kalman Filters, Particle Filters, Sensor Fusion.

### 2. `02-finite-state-machine` (Decision Making)
Implements the high-level logic controller.
-   **Goal**: Management of robot behavior.
-   **Context**: A robot needs to switch behaviors based on triggers (e.g., if `battery < 20%`, switch to `Charge` state).
-   **Key Concepts**: States, Transitions, Events.

### 3. `03-graph-search-n-path-planning` (Guidance)
Implements the trajectory generator.
-   **Goal**: Find the shortest/safest path from point A to point B.
-   **Context**: The robot has a map and knows where it is (thanks to Estimation), but needs to find a valid route through the free space.
-   **Key Concepts**: Grid Maps, Graphs, A* Algorithm, Dijkstra, Heuristics.
