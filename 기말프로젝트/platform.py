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

class Platform:
    def __init__(self, json_fn):
        with open(json_fn) as f:
            self.map = Map(json.load(f))
        self.tileset = self.map.tilesets[0]
        self.layer = self.map.layers[0]
