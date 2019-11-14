"""
Boid-like agents in Python using the Turtle module
"""
import math
import random
import turtle
from turtle import Turtle, Vec2D

from typing import Iterable


class Turtloid(Turtle):
    def separation(self, others: Iterable[Turtle]):
        vectors = [
            self.pos() - other.pos() for other in self.neighbors(others, 30)
        ]
        return sum(vectors, Vec2D(0, 0))

    def alignment(self, others: Iterable[Turtle]):
        angles = [other.heading() for other in self.neighbors(others, 40)]
        if angles:
            avg_angle = sum(angles) / len(angles)
            return Vec2D(math.cos(math.radians(avg_angle)), math.sin(math.radians(avg_angle)))
        else:
            return Vec2D(0,0)

    def cohesion(self, others: Iterable[Turtle]):
        positions = [other.position() for other in self.neighbors(others, 60)]
        return sum(positions, Vec2D(0,0)) * (1/len(positions)) - self.pos()


    def boid_rules(self, others: Iterable[Turtle]):
        v = self.separation(others) + self.alignment(others) + self.cohesion(others)

        self.setheading(self.towards(self.pos() + v)) # + random.randint(-15, +15))
        self.forward(15)

    def neighbors(self, others: Iterable[Turtle], dist: float):
        for other in others:
            if self.distance(other) < dist:
                yield other


turtleoids = [Turtloid() for _ in range(100)]

turtle.tracer(0, 0)
for t in turtleoids:
    t.penup()
    t.speed(0)
    t.setpos(random.randint(-300, 300), random.randint(-300, 300))
    t.setheading(random.randint(0, 360))
    t.pencolor(random.random(), random.random(), random.random())
    #t.pendown()

while True:
    for t in turtleoids:
        t.boid_rules(turtleoids)
    turtle.update()