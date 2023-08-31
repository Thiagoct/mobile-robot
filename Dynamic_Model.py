import control as ctrl
import numpy as np

class Dynamic_Model:
    def __init__(self):
        self.D  = 195e-3   # Diâmetro das rodas
        self.R  = self.D/2 # Raio das rodas
        self.mc = 13       # Massa do chassi
        self.mw = 1.5      # Massa da roda + motor
        self.M = self.mc + 2*self.mw; # Massa total do robô
        self.L = 0.1655    # Largura do robô/2
        self.d = 44.51e-3  # Distância do centro de massa ao eixo das rodas
        self.Ic = 130.7e-3 # Momento de inércia do chassi
        self.Iw = 40e-3    # Momento de inércia da roda em torno do eixo
        self.Im = 20e-3    # Momento de inércia da roda em torno do diâmetro
        self.I  = self.Ic + self.mc*self.d**2 + 2*self.mw*self.L**2 + 2*self.Im # Inércia total

        self.omega_0 = 0
        self.vu_0 = 0


    def step(self, tau_r, tau_l):
        s = ctrl.TransferFunction.s
        delta_t = 0.05000000074505806
        s_value = 2*np.pi*1/delta_t


        up_0 = tau_r*1/self.R
        down_0 = tau_l*1/self.R

        up_1 = up_0 + down_0
        down_1 = up_0 - down_0

        up_2 = up_1/self.M
        down_2 = down_1*self.L

        up_3 = up_2+self.d*self.omega_0
        down_3 = down_2 - self.vu_0*self.M*self.d

        vu = up_3/s
        omega = down_3/s

        aux = omega*self.L

        down_4 = vu - aux
        up_4 = aux + vu

        phi_R = up_4 * 1/self.R
        phi_L = down_4 * 1/self.R

        self.omega_0 = np.abs(ctrl.evalfr(omega, 1j*s_value))
        self.vu_0 = np.abs(ctrl.evalfr(vu, 1j*s_value))

        phi_R_value = np.abs(ctrl.evalfr(phi_R, 1j*s_value))
        phi_L_value = np.abs(ctrl.evalfr(phi_L, 1j*s_value))

        return phi_R_value, phi_L_value 


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