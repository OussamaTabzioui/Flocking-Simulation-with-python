import pygame as pg
from boid import Boid
from predator import Predator
from obstacle import Obstacle  # Added missing import for Obstacle
from settings import width, height, BoidsNum  # Added relevant imports
import random as rd

def main():
    # Initialize Pygame
    pg.init()

    # Set up the display window
    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()

    # Create lists of boids, predators, and obstacles
    boids = [Boid() for _ in range(BoidsNum)]
    predators = [Predator() for _ in range(BoidsNum // 5)]
    obstacles = [Obstacle() for _ in range(BoidsNum // 5)]  # Added obstacle initialization

    running = True
    while running:
        # Fill the screen with a background color
        screen.fill((30, 30, 30))

        # Draw obstacles (if necessary, add a function for this)
        # draw_obstacles(screen, obstacles)

        # Handle events (e.g., quit event)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Update and draw boids
        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.edges()
            boid.draw_b(screen)

        # Update and draw predators
        for predator in predators:
            predator.flock(boids)
            predator.update()
            predator.edges()
            predator.draw_p(screen)

        # Update the display
        pg.display.flip()

        # Cap the frame rate at 60 FPS
        clock.tick(60)

    # Quit Pygame
    pg.quit()

if __name__ == "__main__":
    main()
