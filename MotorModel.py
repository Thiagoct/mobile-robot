import numpy as np
from scipy.integrate import solve_ivp

class MotorModel:
    def __init__(self):
        self.R = 710e-3   # Resistência de armadura do motor (ohms)
        self.L = 0.66e-3  # Indutância de armadura do motor (henrys)
        self.N = 38.3     # Razão da caixa de redução
        self.Ke = 23e-3   # Constante de força eletromotriz (Volts por unidade de velocidade angular)
        self.Kt = 29e-3   # Constante de torque (Nm por Ampere)

        # Inicialize as condições iniciais para as correntes e torques
        self.I0_1 = 0.0
        self.I0_2 = 0.0
        self.torque0_1 = 0.0
        self.torque0_2 = 0.0

    def motor_equations(self, t, state, voltage, omega):
        I = state[0]
        E = self.Ke * omega  # Cálculo da constante de eletromotriz (volts)
        dI_dt = (voltage - I * self.R - E) / self.L
        torque_m = self.Kt * I
        torque = self.N*torque_m
        return [dI_dt, torque]

    def step(self, voltage1, voltage2, omega1, omega2, t):
        # Integre as equações diferenciais para calcular as correntes e os torques no próximo ponto de tempo
        solution_1 = solve_ivp(
            fun=lambda t, y: self.motor_equations(t, y, voltage1, omega1),
            t_span=(t, t + 0.01),  # Próximo ponto de tempo
            y0=[self.I0_1, self.torque0_1],
            t_eval=[t + 0.01],
            method='RK45' #Runge-Kutta
        )

        solution_2 = solve_ivp(
            fun=lambda t, y: self.motor_equations(t, y, voltage2, omega2),
            t_span=(t, t + 0.01),  # Próximo ponto de tempo
            y0=[self.I0_2, self.torque0_2],
            t_eval=[t + 0.01],
            method='RK45' #Runge-Kutta
        )

        I1 = solution_1.y[0]
        I2 = solution_2.y[0]

        torque_1 = solution_1.y[1]
        torque_2 = solution_2.y[1]

        self.I0_1 = I1[0]
        self.I0_2 = I2[0]
        self.torque_01 = torque_1[0]
        self.torque_02 = torque_2[0]

        return torque_1[0], torque_2[0]

if __name__ == "__main__":
    # Crie uma instância do motor CC
    motor = MotorModel()

    # Tensões e velocidades angulares de entrada
    voltage1 = 12.0  # Tensão para o primeiro motor (volts)
    voltage2 = 8.0   # Tensão para o segundo motor (volts)
    omega1 = 100.0   # Velocidade angular para o primeiro motor (rad/s)
    omega2 = 50.0    # Velocidade angular para o segundo motor (rad/s)

    # Tempo inicial
    t = 0.0

    # Calcule as correntes e os torques no próximo ponto de tempo
    torque1, torque2 = motor.step(voltage1, voltage2, omega1, omega2, t)

    # Exiba os resultados
    print("Torque no primeiro motor no próximo ponto de tempo:", torque1)
    print("Torque no segundo motor no próximo ponto de tempo:", torque2)
