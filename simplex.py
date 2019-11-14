"""
Create frames for a 2D GIF of simplex noise moving through time
"""

import os

import opensimplex
from PIL import Image

WIDTH = 200
HEIGHT = 200
TIME = 200
SCALE = 0.03

im = Image.new('L', (WIDTH, HEIGHT), 0.5)
px = im.load()
noise_fn = opensimplex.OpenSimplex().noise3d

for t in range(TIME):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            noise = noise_fn(x * SCALE, y * SCALE, t * SCALE)
            px[x, y] = int((noise + 0.5) * 255)

    im.save(os.path.expanduser('~/simplex_%03d.png') % t)