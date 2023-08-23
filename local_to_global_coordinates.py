import math

def local_to_global_coordinates(x_local, y_local, x_robot, y_robot, theta_robot):
    """
    Converte coordenadas locais do sistema de coordenadas do robô para coordenadas globais.

    Args:
        x_local (float): Coordenada x local no sistema do robô.
        y_local (float): Coordenada y local no sistema do robô.
        x_robot (float): Coordenada x global do robô.
        y_robot (float): Coordenada y global do robô.
        theta_robot (float): Orientação do robô em radianos.

    Returns:
        tuple: Uma tupla contendo as coordenadas globais (x_global, y_global) após a conversão.
    """
    # Calcule as coordenadas globais
    x_global = x_robot + (x_local * math.cos(theta_robot) - y_local * math.sin(theta_robot))
    y_global = y_robot + (x_local * math.sin(theta_robot) + y_local * math.cos(theta_robot))

    return x_global, y_global, theta_robot  # Também retornamos theta_robot sem modificação

# Exemplo de uso:
if __name__ == "__main__":
    # Coordenadas locais no sistema do robô
    x_local = 1.0  # Coordenada x local
    y_local = 2.0  # Coordenada y local

    # Coordenadas globais da posição do robô
    x_robot = 3.0  # Coordenada x global do robô
    y_robot = 4.0  # Coordenada y global do robô

    # Orientação do robô em radianos
    theta_robot = math.radians(45)  # 45 graus em radianos

    # Converta as coordenadas locais para coordenadas globais
    x_global, y_global, theta_robot = local_to_global_coordinates(x_local, y_local, x_robot, y_robot, theta_robot)

    print(f"Coordenada X Global: {x_global} metros")
    print(f"Coordenada Y Global: {y_global} metros")
    print(f"Orientação Theta Global: {math.degrees(theta_robot)} graus")
