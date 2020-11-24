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
               'Run', 'Sphere', 'Sphere end', 'Sphere ready']
    RUN_MAX_TIME = 1
    DASH_MAX_TIME = 0.5
    DASH_COOL = 1
    JUMP_COOL = 3
    SPHERE_COOL = 6
    FPS = 10

    def __init__(self):
        self.pos = 750, 480
        self.delta = 0, 0
        self.images = Hornet.load_images()
        self.fall_image = None
        self.action = 'Idle'
        self.time = 0
        self.run_time = 0
        self.dash_time = 0
        self.dash_cool_time = 0
        self.jump_cool_time = 0
        self.sphere_cool_time = 0
        self.fidx = 0
        self.flip = 'h'
        self.target = None
        self.health = 300
        self.build_behavior_tree()

    def draw(self):
        pos = self.bg.to_screen(self.pos)
        if self.action != 'Dash ready' and self.action != 'Dash' and self.action != 'Dash end':
            self.flip = '' if self.delta[0] < 0 else 'h'
        if self.action != 'Fall':
            images = self.images[self.action]
            image = images[self.fidx]
        else:
            image = self.fall_image
        image.composite_draw(0, self.flip, *pos, image.w, image.h)

    def update(self):
        x, y = self.pos
        bg_l, bg_b, bg_r, bg_t = self.bg.get_boundary()
        x = clamp(bg_l, x, bg_r)
        y = clamp(bg_b, y, bg_t)
        self.pos = x, y
        self.jump_cool_time += gfw.delta_time
        self.dash_cool_time += gfw.delta_time
        self.sphere_cool_time += gfw.delta_time
        self.bt.run()

    def idle(self):
        if self.action != 'Idle':
            return BehaviorTree.FAIL
        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if gobj.distance(self.pos, self.target.pos) < 800:
            self.action = 'Run'
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
            if self.jump_cool_time > Hornet.JUMP_COOL:
                self.action = 'Jump ready'
                self.jump_cool_time = 0
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
        return BehaviorTree.RUNNING

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
        return BehaviorTree.RUNNING

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
        return BehaviorTree.RUNNING

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
        return BehaviorTree.RUNNING

    def sphere_ready(self):
        if self.action == 'Sphere' or self.action == 'Sphere end':
            return BehaviorTree.SUCCESS
        if self.action != 'Sphere ready':
            if self.sphere_cool_time > Hornet.SPHERE_COOL:
                self.action = 'Sphere ready'
                self.sphere_cool_time = 0
                self.time = 0
            else:
                return BehaviorTree.FAIL

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Sphere ready']) - 1:
            self.action = 'Sphere'
            self.time = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def sphere(self):
        if self.action == 'Sphere end':
            return BehaviorTree.SUCCESS
        if self.action != 'Sphere':
            return BehaviorTree.FAIL

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Sphere']) - 1:
            self.action = 'Sphere end'
            self.time = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def sphere_end(self):
        if self.action != 'Sphere end':
            return BehaviorTree.FAIL

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Sphere end']) - 1:
            self.action = 'Fall'
            self.time = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def run(self):
        if self.action != 'Run':
            self.run_time = random.random()
            self.action = 'Run'
        if self.pos[0] < self.target.pos[0]:
            self.delta = -3, 0
        else:
            self.delta = 3, 0

        gobj.move_obj(self)
        self.time += gfw.delta_time
        self.run_time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])

        if self.run_time > Hornet.RUN_MAX_TIME:
            self.delta = 0, 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def dash_ready(self):
        if self.action == 'Dash' or self.action == 'Dash end':
            return BehaviorTree.SUCCESS
        if self.action != 'Dash ready':
            if self.dash_cool_time > Hornet.DASH_COOL:
                self.action = 'Dash ready'
                self.dash_cool_time = 0
                self.time = 0
                if self.pos[0] < self.target.pos[0]:
                    self.flip = 'h'
                else:
                    self.flip = ''
            else:
                return BehaviorTree.FAIL

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Dash ready']) - 1:
            self.action = 'Dash'
            self.time = 0
            if self.pos[0] < self.target.pos[0]:
                self.delta = 20, 0
            else:
                self.delta = -20, 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def dash(self):
        if self.action == 'Dash end':
            return BehaviorTree.SUCCESS
        if self.action != 'Dash':
            return BehaviorTree.FAIL

        gobj.move_obj(self)
        self.dash_time += gfw.delta_time
        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])

        if self.dash_time > Hornet.DASH_MAX_TIME:
            self.dash_time = 0
            self.action = 'Dash end'
            self.delta = 0, 0
            self.time = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def dash_end(self):
        if self.action != 'Dash end':
            return BehaviorTree.FAIL

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Dash end']) - 1:
            self.action = 'Idle'
            self.time = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def do_nothing(self):
        return BehaviorTree.SUCCESS

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
                            "name": "sphere or fall",
                            "class": SelectorNode,
                            "children": [
                                {
                                    "name": "Sphere Attack",
                                    "class": SequenceNode,
                                    "children": [
                                        {
                                            "name": "sphere ready",
                                            "class": LeafNode,
                                            "function": self.sphere_ready,
                                        },
                                        {
                                            "name": "sphere",
                                            "class": LeafNode,
                                            "function": self.sphere,
                                        },
                                        {
                                            "name": "sphere end",
                                            "class": LeafNode,
                                            "function": self.sphere_end,
                                        },
                                    ],
                                },
                                {
                                    "name": "Do nothing",
                                    "class": LeafNode,
                                    "function": self.do_nothing,
                                }
                            ]
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
                {
                    "name": "Dash",
                    "class": SequenceNode,
                    "children": [
                        {
                            "name": "dash ready",
                            "class": LeafNode,
                            "function": self.dash_ready,
                        },
                        {
                            "name": "dash",
                            "class": LeafNode,
                            "function": self.dash,
                        },
                        {
                            "name": "dash end",
                            "class": LeafNode,
                            "function": self.dash_end,
                        },
                    ],
                },
                {
                    "name": "Run",
                    "class": LeafNode,
                    "function": self.run,
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

    def get_bb(self):
        x, y = self.bg.to_screen(self.pos)
        return x - 30, y - 50, x + 30, y + 50