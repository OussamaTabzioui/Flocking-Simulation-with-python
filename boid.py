import random as rd
import pygame as pg
import math
from settings import width, height, Gravity, RES  # Import settings

class Boid:
    def __init__(self):
        # Initialize position, velocity, and acceleration
        self.position = pg.Vector2(rd.randint(0, width), rd.randint(0, height))
        self.velocity = pg.Vector2(rd.uniform(-2, 2), rd.uniform(-2, 2))
        self.acceleration = pg.Vector2(0, 0)

        # Set physical properties
        self.max_speed = 50 / Gravity
        self.mass = rd.randint(10, 50)  # kg
        self.max_force = 1 / Gravity
        self.distance_max = self.mass * 2  # For better flocking behavior

        # History for drawing trailing effect
        self.history = []

    def update(self):
        # Update the boid's velocity and position
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
        self.position += self.velocity
        self.acceleration *= 0  # Reset acceleration after each update

        # Maintain history for trailing effect
        self.history.append(self.position.copy())
        if len(self.history) > RES + RES // 3:  # Limit history length
            self.history.pop(0)

    def draw_b(self, screen):
        # Draw the boid as an arrow (triangle shape)
        angle = self.velocity.as_polar()[1]  # Get the angle of the velocity vector
        points = [
            self.position + pg.Vector2(RES, 0).rotate(angle),
            self.position + pg.Vector2(-RES, RES).rotate(angle),
            self.position + pg.Vector2(-RES, -RES).rotate(angle)
        ]
        pg.draw.polygon(screen, (255, 255, 255), points)

        # Draw the trailing smoke effect
        for i in range(len(self.history) - 1):
            alpha = int(255 * (i / len(self.history)))  # Fade out effect
            color = (100, 100, 100, alpha)
            pg.draw.line(screen, color, self.history[i], self.history[i + 1], RES // 3)

    def avoid_obstacles(self, obstacles, min_distance=50, repulsion_strength=2.0):
        # Calculate the repulsion force to avoid obstacles
        repulsion_force = pg.Vector2(0, 0)

        for obs in obstacles:
            obs_rect = pg.Rect(obs.position, (obs.size, obs.size))  # Create obstacle rectangle
            if obs_rect.collidepoint(self.position):  # Check if the boid is within the obstacle
                to_obstacle = self.position - pg.Vector2(obs.position)
                distance = to_obstacle.length()

                if distance < min_distance:  # Apply force if within threshold distance
                    force = to_obstacle.normalize() * (1 / (distance + 0.1)) * repulsion_strength
                    repulsion_force += force

        # Apply the repulsion force to the boid's velocity
        if repulsion_force.length() > 0:
            new_velocity = self.velocity + repulsion_force
            if new_velocity.length() > self.max_speed:
                new_velocity = new_velocity.normalize() * self.max_speed
            self.velocity = new_velocity

    def edges(self):
        # Handle boid movement when it reaches screen edges
        if self.position.x <= RES or self.position.x >= width - RES:
            self.velocity.x *= -1  # Reverse velocity on x-axis
            self.position.x = max(RES, min(self.position.x, width - RES))  # Keep within bounds

        if self.position.y <= RES or self.position.y >= height - RES:
            self.velocity.y *= -1  # Reverse velocity on y-axis
            self.position.y = max(RES, min(self.position.y, height - RES))  # Keep within bounds

    def apply_force(self, force):
        # Apply a force to the boid's acceleration
        self.acceleration += force

    def isNeighbor(self, boid):
        # Check if another boid is within the interaction distance
        distance = self.position.distance_to(boid.position)
        return 0 < distance <= self.distance_max

    def alignment(self, boids):
        # Align boid with the average velocity of neighbors
        total_velocity = pg.Vector2(0, 0)
        neighbors_count = 0

        for boid in boids:
            if self.isNeighbor(boid):
                total_velocity += boid.velocity
                neighbors_count += 1

        if neighbors_count > 0:
            average_velocity = total_velocity / neighbors_count
            average_velocity = average_velocity.normalize() * self.max_speed
            steer = average_velocity - self.velocity
            if steer.length() > self.max_force:
                steer = steer.normalize() * self.max_force
            return steer
        return pg.Vector2(0, 0)

    def separation(self, boids):
        # Separate from nearby boids to avoid crowding
        desired_separation = 25
        steer = pg.Vector2(0, 0)
        neighbors_count = 0

        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if 0 < distance < desired_separation:
                diff = self.position - boid.position
                diff = diff.normalize() / distance  # Weight by distance
                steer += diff
                neighbors_count += 1

        if neighbors_count > 0:
            steer /= neighbors_count
        if steer.length() > 0:
            steer = steer.normalize() * self.max_speed - self.velocity
            if steer.length() > self.max_force:
                steer = steer.normalize() * self.max_force
        return steer

    def cohesion(self, boids):
        # Move towards the average position of neighbors
        total_position = pg.Vector2(0, 0)
        neighbors_count = 0

        for boid in boids:
            if self.isNeighbor(boid):
                total_position += boid.position
                neighbors_count += 1

        if neighbors_count > 0:
            center_of_mass = total_position / neighbors_count
            return self.seek(center_of_mass)
        return pg.Vector2(0, 0)

    def seek(self, target):
        # Calculate the steering force to move towards a target
        desired = target - self.position
        desired = desired.normalize() * self.max_speed
        steer = desired - self.velocity
        if steer.length() > self.max_force:
            steer = steer.normalize() * self.max_force
        return steer

    def flock(self, boids):
        # Combine alignment, cohesion, and separation behaviors
        alignment_force = self.alignment(boids) * 1.0
        cohesion_force = self.cohesion(boids) * 1.0
        separation_force = self.separation(boids) * 1.5

        self.apply_force(alignment_force)
        self.apply_force(cohesion_force)
        self.apply_force(separation_force)
