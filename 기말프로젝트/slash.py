import gfw
import gobj
import knight

class Slash:
    images = {}
    def __init__(self, knt):
        self.k = knt
        self.flip = knt.flip
        self.images = knight.load_images('SlashEffect')
        self.time = 0
        self.fidx = 0

    def draw(self):
        image = self.images[self.fidx]
        x, y = self.k.bg.to_screen(self.k.pos)
        if self.flip == 'h':
            image.composite_draw(0, self.flip, x + image.w // 3, y, image.w, image.h)
        else:
            image.composite_draw(0, self.flip, x - image.w // 3, y, image.w, image.h)

    def update(self):
        if self.flip != self.k.flip:
            gfw.world.remove(self)

        self.time += gfw.delta_time
        frame = self.time * knight.Knight.FPS * 4
        if frame < len(self.images):
            self.fidx = int(frame)
        else:
            gfw.world.remove(self)

    def handle_event(self):
        pass

    def get_bb(self):
        x, y = self.k.bg.to_screen(self.k.pos)
        if self.k.flip == 'h':
            return x + 10, y - 40, x + 130, y + 40
        elif self.k.flip == '':
            return x - 130, y - 40, x - 10, y + 40