import random
from pico2d import *
import gfw
import gobj
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

gravity = 0.4

class Hornet:
    images = {}
    sounds = {}
    ACTIONS = ['Dash', 'Dash end', 'Dash ready', 'Idle', 'Jump', 'Jump ready', 'Land',
               'Run', 'Sphere', 'Sphere ball', 'Sphere end', 'Sphere ready']
    DASH_COOL = 2
    JUMP_COOL = 5
    SPHERE_COOL = 7
    FPS = 10

    def __init__(self):
        self.pos = 750, 480
        self.delta = 0, 0
        self.images = Hornet.load_images()
        self.fall_image = None
        self.action = 'Idle'
        self.time = 0
        self.dash_time = 0
        self.jump_time = 0
        self.sphere_time = 0
        self.fidx = 0
        self.target = None
        self.health = 300
        self.build_behavior_tree()

    def draw(self):
        pos = self.bg.to_screen(self.pos)
        flip = '' if self.delta[0] < 0 else 'h'
        if self.action != 'Fall':
            images = self.images[self.action]
            image = images[self.fidx]
        else:
            image = self.fall_image
        image.composite_draw(0, flip, *pos, image.w, image.h)

    def update(self):
        x, y = self.pos
        bg_l, bg_b, bg_r, bg_t = self.bg.get_boundary()
        x = clamp(bg_l, x, bg_r)
        y = clamp(bg_b, y, bg_t)
        self.pos = x, y
        self.bt.run()

    def idle(self):
        if self.action != 'Idle':
            return BehaviorTree.FAIL
        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if gobj.distance(self.pos, self.target.pos) < 200:
            self.action = 'Jump ready'
            self.time = 0
            self.fidx = 0
        return BehaviorTree.SUCCESS

    def wounded(self):
        if self.action != 'wounded':
            if self.health > 0:
                return BehaviorTree.FAIL
            else:
                self.action = 'wounded'
                self.time = 0
        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['wounded']) - 1:
            gfw.world.remove(self)

    def jump_ready(self):
        if self.action == 'Jump' or self.action == 'Fall' or self.action == 'Land':
            return BehaviorTree.SUCCESS
        if self.action != 'Jump ready':
            if self.jump_time > Hornet.JUMP_COOL:
                self.action = 'Jump ready'
                self.jump_time = 0
                self.time = 0
            else:
                return BehaviorTree.FAIL

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Jump ready']) - 1:
            self.action = 'Jump'
            self.time = 0
            if self.pos[0] < self.target.pos[0]:
                self.delta = (3, 30)
            else:
                self.delta = (-3, 30)
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def jump(self):
        if self.action == 'Fall' or self.action == 'Land':
            return BehaviorTree.SUCCESS
        if self.action != 'Jump':
            return BehaviorTree.FAIL

        dx, dy = self.delta
        dy -= gravity
        dy = clamp(0, dy, 15)
        self.delta = (dx, dy)
        gobj.move_obj(self)
        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Jump']) - 1:
            self.action = 'Fall'
            self.time = 0
            images = self.images['Jump']
            self.fall_image = images[len(images) - 1]
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def fall(self):
        if self.action == 'Land':
            return BehaviorTree.SUCCESS
        if self.action != 'Fall':
            return BehaviorTree.FAIL

        dx, dy = self.delta
        dy -= gravity
        dy = clamp(-10, dy, 15)
        self.delta = (dx, dy)
        gobj.move_obj(self)
        self.time += gfw.delta_time
        if self.pos[1] <= 480:
            x, y = self.pos
            self.pos = x, 480
            self.action = 'Land'
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def land(self):
        if self.action != 'Land':
            return BehaviorTree.FAIL

        self.delta = 0, 0
        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx >= len(self.images['Land']) - 1:
            self.action = 'Idle'
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def build_behavior_tree(self):
        self.bt = BehaviorTree.build({
            "name": " ",
            "class": SelectorNode,
            "children": [
                {
                    "name": "Idle",
                    "class": LeafNode,
                    "function": self.idle,
                },
                {
                    "name": "Wounded",
                    "class": LeafNode,
                    "function": self.wounded,
                },
                {
                    "name": "Jump",
                    "class": SequenceNode,
                    "children": [
                        {
                            "name": "jump ready",
                            "class": LeafNode,
                            "function": self.jump_ready,
                        },
                        {
                            "name": "jump",
                            "class": LeafNode,
                            "function": self.jump,
                        },
                        {
                            "name": "fall",
                            "class": LeafNode,
                            "function": self.fall,
                        },
                        {
                            "name": "land",
                            "class": LeafNode,
                            "function": self.land,
                        },
                    ],
                },
            ]
        })

    @staticmethod
    def load_images():
        if len(Hornet.images) != 0:
            return Hornet.images

        images = {}
        count = 0
        file_fmt = '%s/Hornet/%s/%s (%d).png'
        for action in Hornet.ACTIONS:
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
            images[action] = action_images
        Hornet.images = images
        print('Hornet %d images loaded' % (count))
        return images