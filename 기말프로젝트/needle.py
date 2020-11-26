import gfw
import gobj

class Sphere_Ball:
    def __init__(self, h):
        self.h = h
        self.pos = h.pos
        self.time = 0
        self.fidx = 0
        self.radius = 130
        self.images = self.h.images['Sphere ball']

    def draw(self):
        pos = self.h.bg.to_screen(self.pos)
        image = self.images[self.fidx]
        image.composite_draw(0, self.h.flip, *pos, image.w, image.h)

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * 10
        self.fidx = int(frame) % len(self.images)

class Throw_Needle:
    def __init__(self, h):
        self.h = h
        self.pos = h.pos[0], h.pos[1] - 40
        self.delta = 0, 0
        self.time = 0
        self.fidx = 0
        self.images = self.h.images['Throw needle']

    def draw(self):
        pos = self.h.bg.to_screen(self.pos)
        image = self.images[self.fidx]
        image.composite_draw(0, self.h.flip, *pos, image.w, image.h)

    def update(self):
        dx, dy = self.delta
        if self.h.flip == 'h':
            dx -= 0.6
        else:
            dx += 0.6
        self.delta = dx, dy

        gobj.move_obj(self)
        self.time += gfw.delta_time
        frame = self.time * 10
        if self.fidx != len(self.images) - 1:
            self.fidx = int(frame) % len(self.images)


    def get_bb(self):
        x, y = self.h.bg.to_screen(self.pos)
        return x - 100, y - 10, x + 100, y + 10