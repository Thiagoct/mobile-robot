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
        # Equações de Lagrange para as velocidades angulares das rodas
        eq1 = sp.Eq(torque_right, self.I * self.omega_right)
        eq2 = sp.Eq(torque_left, self.I * self.omega_left)

        # Resolva as equações para as velocidades angulares das rodas
        solutions = sp.solve((eq1, eq2), (self.omega_right, self.omega_left))

        return solutions[self.omega_right], solutions[self.omega_left]

# Exemplo de uso:
if __name__ == "__main__":

    # Crie um modelo de acionamento diferencial com os parâmetros especificados
    diff_drive_model = Dynamic_Model()

    # Aplique torques nas rodas direita e esquerda (entrada do modelo)
    torque_right = 2.0  # Nm
    torque_left = 1.0  # Nm

    # Calcule as velocidades angulares das rodas direita e esquerda
    omega_right, omega_left = diff_drive_model.step(torque_right, torque_left)

    print(f"Velocidade Angular da Roda Direita: {omega_right} rad/s")
    print(f"Velocidade Angular da Roda Esquerda: {omega_left} rad/s")