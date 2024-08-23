from boid import Boid
import pygame as pg
from settings import RES
import random as rd

class Predator(Boid):
    def __init__(self):
        # Initialize the predator as a Boid and modify its speed and force
        super().__init__()
        self.max_speed *= 1.5  # Increase max speed for predator
        self.max_force *= 1.5  # Increase max force for predator

    def update(self):
        # Update predator's state; inherits basic behavior from Boid
        super().update()
        # Predators may have additional behaviors; currently, it uses Boid's update

    def draw_p(self, screen):
        """
        Draw the predator on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the predator on.
        """
        # Draw the predator as an arrow (triangle shape)
        angle = self.velocity.as_polar()[1]  # Get the angle of the velocity vector
        points = [
            self.position + pg.Vector2(RES, 0).rotate(angle),
            self.position + pg.Vector2(-RES, RES).rotate(angle),
            self.position + pg.Vector2(-RES, -RES).rotate(angle)
        ]
        pg.draw.polygon(screen, (255, 0, 0), points)  # Draw predator as a red triangle

        # Draw the trailing smoke effect
        for i in range(len(self.history) - 1):
            alpha = int(255 * (i / len(self.history)))  # Calculate alpha for fade-out effect
            color = (100, 0, 0, alpha)  # Dark red color with varying transparency
            pg.draw.line(screen, color, self.history[i], self.history[i + 1], RES // 3)  # Draw fading trail
