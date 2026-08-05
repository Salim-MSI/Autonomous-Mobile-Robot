import time

import pygame


pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise RuntimeError("Aucune manette détectée.")

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Manette : {joystick.get_name()}")
print(f"Axes : {joystick.get_numaxes()}")
print(f"Boutons : {joystick.get_numbuttons()}")

try:
    while True:
        pygame.event.pump()

        axes = [
            round(joystick.get_axis(index), 2)
            for index in range(joystick.get_numaxes())
        ]

        buttons = [
            joystick.get_button(index)
            for index in range(joystick.get_numbuttons())
        ]

        print(
            f"\rAxes={axes} | Boutons={buttons}",
            end="",
            flush=True,
        )

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nTest terminé.")

finally:
    pygame.quit()