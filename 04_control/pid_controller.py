
class PIDController:
    def __init__(self, kp: float, ki: float, kd: float, setpoint: float = 0.0):
        """
        Initializes the PID Controller.
        
        Args:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
            setpoint (float): Target value to reach.
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        
        self.prev_error = 0.0
        self.integral = 0.0

    def update(self, measurement: float, dt: float = 1.0) -> float:
        """
        Calculates the control output based on the current measurement.
        
        Args:
            measurement (float): Current measured process variable.
            dt (float): Time step duration.
            
        Returns:
            float: Control output (u).
        """
        error = self.setpoint - measurement
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term
        self.integral += error * dt
        i_term = self.ki * self.integral
        
        # Derivative term
        derivative = (error - self.prev_error) / dt
        d_term = self.kd * derivative
        
        # Save error for next step
        self.prev_error = error
        
        return p_term + i_term + d_term

def run_demo() -> None:
    import time
    
    # Simulation parameters
    setpoint = 10.0
    current_pos = 0.0
    velocity = 0.0
    dt = 0.1
    max_steps = 100
    
    # PID Gains (Tunable)
    kp = 2.0  # Spring force
    ki = 0.0  # Accumulation correction
    kd = 1.0  # Damping force
    
    print(f"Goal: Move from {current_pos} to {setpoint}")
    print(f"PID Parameters: Kp={kp}, Ki={ki}, Kd={kd}")
    print("-" * 30)
    
    pid = PIDController(kp, ki, kd, setpoint)
    
    history = []
    
    for t in range(max_steps):
        # 1. Calculate Control Output (Force)
        force = pid.update(current_pos, dt)
        
        # 2. Physics Simulation (F = ma)
        # Using simple Euler integration
        mass = 1.0
        acceleration = force / mass
        
        # Apply some friction/drag
        friction = -0.1 * velocity
        acceleration += friction
        
        velocity += acceleration * dt
        current_pos += velocity * dt
        
        history.append(current_pos)
        
        # Simple text visualization
        bar_len = int(current_pos * 2)
        bar = "#" * max(0, bar_len)
        print(f"t={t*dt:.1f}s | Pos={current_pos:6.2f} | Vel={velocity:6.2f} | Force={force:6.2f} | [{bar}]")
        
        # Check convergence
        if abs(current_pos - setpoint) < 0.01 and abs(velocity) < 0.01:
            print(f"\nConverged to target in {t*dt:.1f} seconds!")
            break

if __name__ == "__main__":
    run_demo()
