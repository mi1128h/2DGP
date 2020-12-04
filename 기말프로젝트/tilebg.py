import gfw
from pico2d import *
import json

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

class Background:
    def __init__(self, json_fn, tile_fn, layer):
        with open(json_fn) as f:
            self.map = Map(json.load(f))
        self.image = gfw.image.load(tile_fn)
        self.width = self.map.tilewidth * self.map.width
        self.height = self.map.tileheight * self.map.height
        self.scroll_x, self.scroll_y = 0, 0
        self.tileset = self.map.tilesets[0]
        self.layer = self.map.layers[layer]
        self.wraps = True
    def get_boundary(self):
        return 0, 0, self.width, self.height
    def to_screen(self, pos):
        x, y = pos
        l, b, r, t = self.win_rect
        return x - l, y - b
    def translate(self, pos):
        x, y = pos
        l, b, r, t = self.win_rect
        return l + x, b + y
    def update(self):
        if self.target is None:
            return
        tx, ty = self.target.pos
        cw, ch = get_canvas_width(), get_canvas_height()
        sl = clamp(0, round(tx - cw / 2), self.width - cw)
        sb = clamp(0, round(ty - ch / 2), self.height - ch)
        self.win_rect = sl, sb, cw, ch
    def draw(self):
        cw,ch = get_canvas_width(), get_canvas_height()
        l,b,t,r = self.win_rect
        tile_x = l // self.map.tilewidth
        tile_y = b // self.map.tileheight
        beg_x = -(l % self.map.tilewidth)
        beg_y = -(b % self.map.tileheight)
        db = beg_y
        ty = tile_y
        while ty < self.layer.height and db < ch:
            if ty >= 0:
                dl = beg_x
                tx = tile_x
                ti = (self.map.height - ty - 1) * self.map.width + tx
                while tx < self.layer.width and dl < cw:
                    tile = self.layer.data[ti]
                    rect = self.tileset.getRectForTile(tile)
                    self.image.clip_draw_to_origin(*rect, dl, db)
                    print(rect, dl, db)
                    dl += self.map.tilewidth
                    ti += 1
                    tx += 1
            db += self.map.tileheight
            ty += 1
            if self.wraps and ty >= self.layer.height:
                ty -= self.layer.height
