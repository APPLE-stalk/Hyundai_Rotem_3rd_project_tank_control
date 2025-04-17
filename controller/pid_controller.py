class PIDController:
    def __init__(self, kp = 0.07, ki = 0.0, kd = 0.0, dt = 1.0):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.dt = dt

        self.integral = 0.0
        
        
    def compute(self, target, current):
        # 현재 오차 계산
        error = target - current
        
        # 적분항 누적
        self.integral += error * self.dt
        
        # 미분항 계산
        d_error = error / self.dt
        
        # PID 제어량
        output = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * d_error
        )
        
        return output