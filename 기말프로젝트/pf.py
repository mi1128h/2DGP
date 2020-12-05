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
    def __init__(self, l, b, w, h):
        self.l = l
        self.b = b
        self.w = w
        self.h = h

    def update(self):
        pass
    def draw(self):
        pass
    def get_bb(self):
        pos = self.l + self.w/2, self.b + self.h/2
        x, y = self.bg.to_screen(pos)
        return x - self.w/2, y - self.h/2, x + self.w/2, y + self.h/2
    def get_bb_real(self):
        x, y = self.l + self.w / 2, self.b + self.h / 2
        return x - self.w / 2, y - self.h / 2, x + self.w / 2, y + self.h / 2

class Platform:
    def __init__(self, json_fn):
        with open(json_fn) as f:
            self.map = Map(json.load(f))
        self.tileset = self.map.tilesets[0]
        self.layer = self.map.layers[0]
        self.rects = []
        self.load_rects()

    def load_rects(self):
        for ti in range(0, len(self.layer.data) - 1):
            if self.layer.data[ti] != 0:
                tile = self.layer.data[ti]
                l, b, w, h = self.tileset.getRectForTile(tile)
                rect = RECT(l, b, w, h)
                self.rects.append(rect)