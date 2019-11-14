"""
Implementation of 2D Perlin noise in Python
"""
import os
import random
from turtle import Vec2D

from PIL import Image

MAX_X = 100
MAX_Y = 100

# Precompute gradients
GRADIENTS = [Vec2D(1, 0).rotate(random.randint(0, 360)) for _ in range((MAX_X + 1) * (MAX_Y + 1))]


def interpolate(a0, a1, weight):
    return (1 - weight) * a0 + weight * a1

def dot_grid_gradient(grid_x, grid_y, sample_x, sample_y):
    # Distance from the grid points
    dx = sample_x - grid_x
    dy = sample_y - grid_y

    gradient = GRADIENTS[grid_y * MAX_X + grid_x]
    return dx * gradient[0] + dy * gradient[1]


def perlin_noise(x: float, y: float) -> float:
    # Closest grid points
    x0, y0 = int(x), int(y)
    x1, y1 = x0 + 1, y0 + 1

    # Interpolate between the two lower grid points and the two upper
    lower = interpolate(
        dot_grid_gradient(x0, y0, x, y),
        dot_grid_gradient(x1, y0, x, y),
        x - x0
    )

    upper = interpolate(
        dot_grid_gradient(x0, y1, x, y),
        dot_grid_gradient(x1, y1, x, y),
        x - x0
    )

    return interpolate(lower, upper, y - y0)


img_x, img_y  = 200, 200
im = Image.new('L', (img_x, img_y), 0.5)
px = im.load()
scale = 0.03

for y in range(img_y):
    for x in range(img_x):
        noise = perlin_noise(x * scale, y * scale)
        px[x, y] = int((noise + 0.7) * 255)
        print(px[x, y])

im.save(os.path.expanduser('~/perlin.png'))




