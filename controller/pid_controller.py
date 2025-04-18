class PIDController:
    def __init__(self, kp = 0.0, ki = 0.0, kd = 0.0, dt = 1.0):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.dt = dt

        self.integral = 0.0
        self.prev_error = 0.0
        
        
    def compute(self, target, current):
        # 현재 오차 계산
        error = target - current
        
        # 적분항 누적
        self.integral += error * self.dt
        
        # 미분항 계산
        d_error = (error - self.prev_error) / self.dt
        
        # 이전 오차 업데이트
        self.prev_error = error
        
        # PID 제어량
        output = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * d_error
        )
        # print('controller output: ', output)
        
        return output
    
    
    def update_gains(self, kp=None, ki=None, kd=None):
        if kp is not None:
            self.kp = kp
        if ki is not None:
            self.ki = ki
        if kd is not None:
            self.kd = kd
            