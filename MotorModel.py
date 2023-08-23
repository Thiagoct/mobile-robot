import numpy as np

class MotorModel:
    def __init__(self):
        self.R = 710e-3   # Resistência de armadura do motor (ohms)
        self.L = 0.66e-3  # Indutância de armadura do motor (henrys)
        self.N = 38.3     # Razão da caixa de redução
        self.Ke = 23e-3   # Constante de força eletromotriz (Volts por unidade de velocidade angular)
        self.Kt = 29e-3   # Constante de torque (Nm por Ampere)

    def step(self, voltage_right, voltage_left, angular_velocity_right, angular_velocity_left):
        # Calcule a corrente nas rodas direita e esquerda com base nas tensões aplicadas
        current_right = (voltage_right - self.Ke * angular_velocity_right) / (self.R + self.L * angular_velocity_right)
        current_left = (voltage_left - self.Ke * angular_velocity_left) / (self.R + self.L * angular_velocity_left)

        # Calcule o torque nas rodas direita e esquerda com base na corrente
        torque_right = self.Kt * current_right
        torque_left = self.Kt * current_left

        return torque_right, torque_left
    
# Exemplo de uso:
if __name__ == "__main__":

    # Crie um modelo de motor com os parâmetros especificados
    motor_model = MotorModel()

    # Aplique tensões às rodas direita e esquerda e obtenha as velocidades angulares (ajuste conforme necessário)
    voltage_right = 12.0  # Volts
    voltage_left = 10.0  # Volts
    angular_velocity_right = 0.0  # Unidades de velocidade angular (ajuste conforme necessário)
    angular_velocity_left = 0.0  # Unidades de velocidade angular (ajuste conforme necessário)

    # Calcule o torque nas rodas direita e esquerda
    torque_right, torque_left = motor_model.step(voltage_right, voltage_left, angular_velocity_right, angular_velocity_left)

    print(f"Torque na Roda Direita: {torque_right} Nm")
    print(f"Torque na Roda Esquerda: {torque_left} Nm")