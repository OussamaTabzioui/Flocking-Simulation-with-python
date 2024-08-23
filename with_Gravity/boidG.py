import random as rd
import pygame as pg
from settings import *

class Boid:
    def __init__(self):
        self.position = pg.Vector2(rd.randint(0, width), rd.randint(0, height))
        self.velocity = pg.Vector2(rd.uniform(-2, 2), rd.uniform(-2, 2))
        self.acceleration = pg.Vector2(0, 0)
        self.max_speed = 50 / Gravity
        self.mass = rd.randint(10, 50)  # kg
        self.max_force = 1 / Gravity
        self.distance_max = self.mass * 2  # Adjusted for better flocking

    def update(self):
        # Apply gravity as a constant downward force
        gravity_force = pg.Vector2(0, self.mass * Gravity)
        self.apply_force(gravity_force)

        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
        self.position += self.velocity
        self.acceleration *= 0  # Reset acceleration after each update

    def edges(self):
        if self.position.x <= 10 or self.position.x >= width - 10:
            self.velocity.x *= -1  # Reverse the velocity on the x-axis
            self.position.x = max(10, min(self.position.x, width - 10))  # Keep the boid within bounds

        if self.position.y <= 10 or self.position.y >= height - 10:
            self.velocity.y *= -1  # Reverse the velocity on the y-axis
            self.position.y = max(10, min(self.position.y, height - 10))  # Keep the boid within bounds

    def apply_force(self, force):
        # Incorporate the mass of the boid to simulate realistic physics
        self.acceleration += force / self.mass

    def isNeighbor(self, boid):
        distance = self.position.distance_to(boid.position)
        if 0 < distance <= self.distance_max:
            return True
        return False

    def alignment(self, boids):
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
        desired = target - self.position
        desired = desired.normalize() * self.max_speed
        steer = desired - self.velocity
        if steer.length() > self.max_force:
            steer = steer.normalize() * self.max_force
        return steer

    def flock(self, boids):
        alignment_force = self.alignment(boids) * 1.0
        cohesion_force = self.cohesion(boids) * 1.0
        separation_force = self.separation(boids) * 1.5

        self.apply_force(alignment_force)
        self.apply_force(cohesion_force)
        self.apply_force(separation_force)
