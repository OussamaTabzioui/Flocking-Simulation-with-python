import pygame as pg

# Screen dimensions and resolution
width, height = 1280, 720
RES = 10

# Number of boids and gravity constant
BoidsNum = 3
Gravity = 1

def draw_background(screen):
    """
    Draws a gradient background on the screen.

    Args:
        screen (pygame.Surface): The surface to draw the background on.
    """
    for y in range(0, height, 20):
        # Calculate the color gradient based on the vertical position
        color = (0, int(255 - y / height * 255), int(y / height * 255))
        # Draw a horizontal line with the calculated color
        pg.draw.line(screen, color, (0, y), (width, y))

def draw(screen):
    """
    Draws all visual elements on the screen.

    Args:
        screen (pygame.Surface): The surface to draw on.
    """
    draw_background(screen)
    # Additional drawing code can be added here
