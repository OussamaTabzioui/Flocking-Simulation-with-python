import random as rd
import pygame as pg
from settings import width, height

class Obstacle:
    def __init__(self):
        # Initialize obstacle with a random size and position
        self.size = rd.randint(50, 200)  # Random size between 50 and 200
        self.position = pg.Vector2(
            rd.randint(self.size, width - self.size),  # Ensure obstacle is within screen bounds
            rd.randint(self.size, height - self.size)
        )

    def draw_o(self, screen):
        # Draw the obstacle as a rectangle
        pg.draw.rect(screen, (150, 50, 50), (*self.position, self.size, self.size))

def check_obstacle_collision(boid, obstacles):
    """
    Check if the boid collides with any obstacles.

    Args:
        boid (Boid): The boid object to check.
        obstacles (list): A list of obstacle objects to check against.

    Returns:
        bool: True if the boid collides with any obstacle, False otherwise.
    """
    boid_rect = pg.Rect(boid.position, (RES, RES))  # Assuming boid has a square shape with size RES
    for obs in obstacles:
        # Create a rectangle for the obstacle
        obs_rect = pg.Rect(obs.position, (obs.size, obs.size))
        # Check for collision between the boid and the obstacle
        if boid_rect.colliderect(obs_rect):
            return True
    return False
