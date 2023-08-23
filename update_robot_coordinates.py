import math

def update_robot_coordinates(current_x, current_y, current_theta, omega_right, omega_left, wheel_radius, base_width, delta_t):
    """
    Atualiza as coordenadas do robô com base nas velocidades angulares das rodas.

    Args:
        current_x (float): Coordenada x atual do robô.
        current_y (float): Coordenada y atual do robô.
        current_theta (float): Orientação atual do robô em radianos.
        omega_right (float): Velocidade angular da roda direita em radianos por segundo.
        omega_left (float): Velocidade angular da roda esquerda em radianos por segundo.
        wheel_radius (float): Raio das rodas em metros.
        base_width (float): Largura da base do robô (distância entre as rodas) em metros.
        delta_t (float): Intervalo de tempo em segundos.

    Returns:
        tuple: Uma tupla contendo as novas coordenadas (x, y, theta) do robô após a atualização.
    """
    # Calcule a velocidade linear do robô
    V = (omega_right * wheel_radius + omega_left * wheel_radius) / 2.0

    # Calcule a mudança na orientação (delta_theta)
    delta_theta = (omega_right - omega_left) * wheel_radius / base_width

    # Calcule as mudanças nas coordenadas (delta_x e delta_y)
    delta_x = V * math.cos(current_theta) * delta_t
    delta_y = V * math.sin(current_theta) * delta_t

    # Atualize as coordenadas e a orientação
    new_x = current_x + delta_x
    new_y = current_y + delta_y
    new_theta = current_theta + delta_theta

    return new_x, new_y, new_theta

# Exemplo de uso:
if __name__ == "__main__":
    # Parâmetros do robô
    wheel_radius = 0.1  # Raio das rodas em metros
    base_width = 0.2   # Largura da base do robô (distância entre as rodas) em metros

    # Coordenadas atuais do robô
    current_x = 0.0485    # Coordenada x inicial
    current_y = 1.0    # Coordenada y inicial
    current_theta = 0.1499999999999999  # Orientação inicial em radianos

    # Velocidades angulares das rodas em radianos por segundo
    omega_right = 5.0  # rad/s
    omega_left = 4.70   # rad/s

    # Passo de tempo em segundos
    delta_t = 0.1

    # Atualize as coordenadas do robô
    new_x, new_y, new_theta = update_robot_coordinates(current_x, current_y, current_theta, omega_right, omega_left, wheel_radius, base_width, delta_t)

    print(f"Nova Coordenada X: {new_x} metros")
    print(f"Nova Coordenada Y: {new_y} metros")
    print(f"Nova Orientação Theta: {new_theta} radianos")
