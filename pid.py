
class PID():
    def __init__(self, dt, max, min, Kp, Ki, Kd):
        self.dt = dt  # 循环时长
        self.max = max  # 操作变量最大值
        self.min = min  # 操作变量最小值
        self.Kp = Kp  # 比例增益
        self.Ki = Ki  # 微分增益
        self.Kd = Kd  # 积分增益
        self.integral = 0  # 直到上一次的误差值
        self.pre_error = 0  # 上一次的误差值

    def calculate(self, setPoint, pv):
        # 其中 pv:process value 即过程值，
        error = setPoint - pv  # 误差（设定值与实际值的差值）
        Pout = self.Kp * error  # 比例项 Kp * e(t)
        self.integral += error * self.dt  #∑e(t)*△t
        Iout = self.Ki * self.integral  # 积分项 Ki * ∑e(t)*△t
        derivative = (error - self.pre_error) / self.dt  #(e(t)-e(t-1))/△t
        Dout = self.Kd * derivative  # 微分项 Kd * (e(t)-e(t-1))/△t

        output = Pout + Iout + Dout  # 新的目标值  位置式PID：u(t) = Kp*e(t) + Ki * ∑e(t)*△t + Kd * (e(t)-e(t-1))/△t

        if (output > self.max):
            output = self.max
        elif (output < self.min):
            output = self.min

        self.pre_error = error  # 保存本次误差，以供下次计算  e(k-1) = e(k)
        return output


t = range(160)
pid = PID(0.1, 100, -100, 0.1, 0.5, 0.01)
val = 0
setpoint = 15
z = []
for i in t:
    inc = pid.calculate(setpoint, val)    #新的目标值
    print("val:%f inc:%f" % (val, inc))
    z.append(val)  
    val += inc
