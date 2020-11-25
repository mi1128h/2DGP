import random
from pico2d import *
import gfw

RES_DIR = 'res'

def rand(val):
    return val * random.uniform(0.9, 1.1)


def point_add(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return x1 + x2, y1 + y2


def move_obj(obj):
    obj.pos = point_add(obj.pos, obj.delta)


def collides_box(a, b):
    (la, ba, ra, ta) = a.get_bb()
    (lb, bb, rb, tb) = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ba > tb: return False
    if ta < bb: return False

    return True

def collides_distance(a, b):
    d_sq = distance_sq(a.pos, b.pos)
    radius_sum = a.radius + b.radius
    if d_sq < radius_sum**2:
        return True
    return False


def distance_sq(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def distance(point1, point2):
    return math.sqrt(distance_sq(point1, point2))


def draw_collision_box():
    for obj in gfw.world.all_objects():
        if hasattr(obj, 'get_bb'):
            draw_rectangle(*obj.get_bb())


class ImageObject:
    def __init__(self, imageName, pos):
        self.image = gfw.image.load(RES_DIR + '/' + imageName)
        self.pos = pos

    def draw(self):
        self.image.draw(*self.pos)

    def update(self):
        pass


if __name__ == "__main__":
    print("This file is not supposed to be executed directly.")
