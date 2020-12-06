import gfw
from pico2d import *
import json
import gobj

class Layer:
    def __init__(self, dict):
        self.__dict__.update(dict)

class Tileset:
    def __init__(self, dict):
        self.__dict__.update(dict)
        self.rows = math.ceil(self.tilecount / self.columns)
        print('rows:', self.rows)
    def getRectForTile(self, tile):
        x = (tile - 1) % self.columns;
        y = (tile - 1) // self.columns;
        l = x * (self.tilewidth + self.spacing) + self.margin;
        t  = (self.rows - y - 1) * (self.tileheight + self.spacing) + self.margin;
        return l, t, self.tilewidth, self.tileheight

class Map:
    def __init__(self, dict):
        self.__dict__.update(dict)
        self.layers = list(map(Layer, self.layers))
        self.tilesets = list(map(Tileset, self.tilesets))

class RECT:
    def __init__(self, l, b, r, t):
        self.l = l
        self.b = b
        self.r = r
        self.t = t
        self.w = r-l
        self.h = t-b

    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pos = self.l + self.w/2, self.b + self.h/2
        x, y = self.bg.to_screen(pos)
        return x - self.w/2, y - self.h/2, x + self.w/2, y + self.h/2
    def get_bb_real(self):
        return self.l, self.b, self.r, self.t

class Platform:
    def __init__(self, json_fn):
        self.json_fn = json_fn
        self.rects = []
        self.load_rects()

    def load_rects(self):
        with open(self.json_fn) as f:
            data = json.load(f)
            for d in data:
                r = RECT(d['l'], d['b'], d['r'], d['t'])
                self.rects.append(r)