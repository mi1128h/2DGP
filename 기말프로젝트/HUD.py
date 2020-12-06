from pico2d import *
import gfw
import gobj

class Health:
    action = ['Appear', 'Break', 'Empty', 'Idle', 'Refill']
    images = {}
    def __init__(self):
        self.pos = (0, 0)
        self.time = 0
        self.fidx = 0
        self.images = Health.load_images()
        self.action = 'Appear'

    def draw(self):
        images = self.images[self.action]
        if self.action == 'Appear':
            frame = self.time * len(images) * 3
        elif self.action == 'Idle':
            frame = self.time * len(images) / 2
        else:
            frame = self.time * len(images) * 2

        self.fidx = int(frame) % len(images)
        image = images[self.fidx]
        image.draw(*self.pos)

    def update(self):
        self.time += gfw.delta_time
        if self.action == 'Appear' or self.action == 'Refill':
            if self.fidx == len(self.images[self.action]) - 1:
                self.set_action('Idle')
        elif self.action == 'Break':
            if self.fidx == len(self.images[self.action]) - 1:
                self.set_action('Empty')

    def set_action(self, action):
        self.time = 0
        self.action = action

    @staticmethod
    def load_images():
        if len(Health.images) != 0:
            return Health.images

        for action in Health.action:
            count = 0
            file_fmt = '%s/HUD/Health/%s/%s (%d).png'
            action_images = []
            n = 0
            while True:
                n += 1
                fn = file_fmt % (gobj.RES_DIR, action, action, n)
                if os.path.isfile(fn):
                    action_images.append(gfw.image.load(fn))
                else:
                    break
                count += 1
            Health.images[action] = action_images
            print('%s %d images loaded' % (action, count))
        return Health.images

class Frame:
    action = ['Appear', 'Idle', 'Cracked']
    images = {}
    def __init__(self, knt):
        self.pos = (250, get_canvas_height() - 100)
        self.k = knt
        self.images = Frame.load_images()
        self.time = 0
        self.cracked_time = 0
        self.fidx = 0
        self.action = 'Appear'
        self.mask_stack = []

    def draw(self):
        images = self.images[self.action]
        frame = self.time * len(images)
        self.fidx = int(frame) % len(images)
        image = images[self.fidx]
        image.draw(*self.pos)

        for m in self.mask_stack:
            m.draw()

    def update(self):
        self.time += gfw.delta_time
        if self.action == 'Appear':
            if self.fidx == len(self.images[self.action]) - 1:
                self.action = 'Idle'
        if self.k.mask == 0:
            self.action = 'Cracked'
            self.cracked_time += gfw.delta_time

        self.update_mask()

    def update_mask(self):
        for m in self.mask_stack:
            if m.action != 'Idle':
                m.update()
        if len(self.mask_stack) < self.k.mask:
            i = len(self.mask_stack)
            if self.time >= 0.2 * i:
                self.mask_stack.append(Health())
                self.mask_stack[-1].pos = (200 + i * 70, self.pos[1] + 20)

        idleupdate = True
        for m in self.mask_stack:
            if m.action != 'Idle' and m.action != 'Empty':
                idleupdate = False

        if idleupdate == False:
            for m in self.mask_stack:
                if m.action == 'Idle':
                    m.time = 0

        if idleupdate:
            for m in self.mask_stack:
                m.update()

    def refill_all(self):
        self.k.mask = 5
        for m in self.mask_stack:
            if m.action == 'Empty' or m.action == 'Break':
                m.set_action('Refill')

    def handle_event(self, e):
        pass

    @staticmethod
    def load_images():
        if len(Frame.images) != 0:
            return Frame.images

        for action in Frame.action:
            count = 0
            file_fmt = '%s/HUD/Frame/%s/%s (%d).png'
            action_images = []
            n = 0
            while True:
                n += 1
                fn = file_fmt % (gobj.RES_DIR, action, action, n)
                if os.path.isfile(fn):
                    action_images.append(gfw.image.load(fn))
                else:
                    break
                count += 1
            Frame.images[action] = action_images
            print('%s %d images loaded' % (action, count))
        return Frame.images