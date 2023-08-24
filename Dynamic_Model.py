import sympy as sp

class Dynamic_Model:
    def __init__(self):
        self.D  = 195e-3   # Diâmetro das rodas
        self.R  = self.D/2 # Raio das rodas
        self.mc = 13       # Massa do chassi
        self.mw = 1.5      # Massa da roda + motor
        self.m = self.mc + 2*self.mw; # Massa total do robô
        self.L = 0.1655    # Largura do robô/2
        self.d = 44.51e-3  # Distância do centro de massa ao eixo das rodas
        self.Ic = 130.7e-3 # Momento de inércia do chassi
        self.Iw = 40e-3    # Momento de inércia da roda em torno do eixo
        self.Im = 20e-3    # Momento de inércia da roda em torno do diâmetro
        self.I  = self.Ic + self.mc*self.d**2 + 2*self.mw*self.L**2 + 2*self.Im # Inércia total

        # Variáveis simbólicas
        self.omega_right, self.omega_left = sp.symbols('omega_right omega_left')


    def step(self, torque_right, torque_left):
        omega_right = (self.R * torque_right) / self.I
        omega_left = (self.R * torque_left) / self.I

        return omega_right, omega_left

# Exemplo de uso:
if __name__ == "__main__":

    # Crie um modelo de acionamento diferencial com os parâmetros especificados
    diff_drive_model = Dynamic_Model()

    # Valores de torque aplicados (exemplo)
    torque_right_value = 3.0  # N·m
    torque_left_value = 2.0   # N·m

    # Calcular as velocidades angulares das rodas
    omega_right, omega_left =diff_drive_model.step(torque_right_value, torque_left_value)

    # Exibir as velocidades angulares calculadas
    print("Velocidade angular da roda direita:", omega_right, "rad/s")
    print("Velocidade angular da roda esquerda:", omega_left, "rad/s")