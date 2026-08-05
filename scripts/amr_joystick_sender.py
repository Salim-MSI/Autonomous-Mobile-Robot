import json
import socket
import time

import pygame


WSL_IP = "172.23.60.167"
WSL_PORT = 5005

SEND_RATE_HZ = 30.0
DEADZONE = 0.10

MAX_LINEAR_SPEED = 0.5
MAX_ANGULAR_SPEED = 1.5

# À adapter selon la manette.
LINEAR_AXIS = 1
ANGULAR_AXIS = 0

# Exemple : bouton LB sur une manette Xbox.
ENABLE_BUTTON = 4


def apply_deadzone(value: float, deadzone: float) -> float:
    if abs(value) < deadzone:
        return 0.0

    # Rééchelonnement progressif après la zone morte.
    sign = 1.0 if value >= 0.0 else -1.0
    return sign * (abs(value) - deadzone) / (1.0 - deadzone)


def main() -> None:
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        raise RuntimeError(
            "Aucune manette détectée par Windows. "
            "Vérifie la connexion avec joy.cpl."
        )

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Manette détectée : {joystick.get_name()}")
    print(f"Axes : {joystick.get_numaxes()}")
    print(f"Boutons : {joystick.get_numbuttons()}")
    print(f"Envoi UDP vers {WSL_IP}:{WSL_PORT}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    period = 1.0 / SEND_RATE_HZ

    try:
        while True:
            start_time = time.monotonic()
            pygame.event.pump()

            enabled = (
                joystick.get_numbuttons() > ENABLE_BUTTON
                and joystick.get_button(ENABLE_BUTTON) == 1
            )

            if enabled:
                linear_axis = joystick.get_axis(LINEAR_AXIS)
                angular_axis = joystick.get_axis(ANGULAR_AXIS)

                # Sur beaucoup de manettes, pousser le stick donne une valeur négative.
                linear_axis = -apply_deadzone(linear_axis, DEADZONE)
                angular_axis = -apply_deadzone(angular_axis, DEADZONE)

                linear_x = linear_axis * MAX_LINEAR_SPEED
                angular_z = angular_axis * MAX_ANGULAR_SPEED
            else:
                linear_x = 0.0
                angular_z = 0.0

            message = {
                "linear_x": linear_x,
                "angular_z": angular_z,
                "enabled": enabled,
                "timestamp": time.time(),
            }

            sock.sendto(
                json.dumps(message).encode("utf-8"),
                (WSL_IP, WSL_PORT),
            )

            elapsed = time.monotonic() - start_time
            time.sleep(max(0.0, period - elapsed))

    except KeyboardInterrupt:
        stop_message = {
            "linear_x": 0.0,
            "angular_z": 0.0,
            "enabled": False,
            "timestamp": time.time(),
        }

        sock.sendto(
            json.dumps(stop_message).encode("utf-8"),
            (WSL_IP, WSL_PORT),
        )

        print("\nArrêt de la téléopération.")

    finally:
        joystick.quit()
        pygame.quit()
        sock.close()


if __name__ == "__main__":
    main()