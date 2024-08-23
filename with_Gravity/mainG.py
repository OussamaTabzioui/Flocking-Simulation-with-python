import pygame as pg
from boid import Boid
# from boidG import Boid #with gravity
from settings import *
import random as rd

def main():
    pg.init()

    screen = pg.display.set_mode((width, height))
    clock = pg.time.Clock()

    boids = [Boid() for _ in range(BoidsNum)]

    running = True
    while running:
        screen.fill((30, 30, 30))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.edges()
            boid.draw(screen)


        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
