import pygame
from screeninfo import get_monitors

def show_monitors():
    # Initialize Pygame
    pygame.init()

    # Get monitor information using screeninfo
    monitors = get_monitors()
    for monitor in monitors:
        print(f"Monitor {monitor.name}: {monitor.width}x{monitor.height}")

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    show_monitors()

