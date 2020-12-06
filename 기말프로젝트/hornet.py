import random
from pico2d import *
import gfw
import gobj
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from needle import Sphere_Ball, Throw_Needle
import landform

gravity = 0.4

class Hornet:
    images = {}
    sounds = {}
    IMAGE_LIST = ['Flourish', 'Run', 'Idle', 'Jump', 'Jump ready', 'Land', 'Death',
                  'Dash', 'Dash end', 'Dash ready',
                  'Sphere ready', 'Sphere', 'Sphere end', 'Sphere ball',
                  'Throw ready', 'Throw', 'Throw end', 'Throw needle']
    RUN_MAX_TIME = 1
    DASH_MAX_TIME = 0.3
    THROW_MAX_TIME = 0.7
    SPHERE_MAX_TIME = 1.0
    FPS = 13
    SOUND_NUM = {'Death': 7, 'Dash': 8, 'Run': 9, 'Land': 10, 'Jump': 11, 'Sphere': 12, 'Throw': 13, 'Catch': 14, 'Flourish': 15}
    BB_DIFFS = {
        'Flourish': (-50, -115, 50, 60),
        'Run': (-50, -93, 50, 92),
        'Idle': (-50, -100, 50, 80),
        'Jump': (-50, -80, 50, 97),
        'Jump ready': (-50, -90, 50, 60),
        'Land': (-50, -100, 50, 66),
        'Death': (-50, -87, 50, 86),
        'Dash': (-50, -66, 50, 16),
        'Dash end': (-50, -100, 50, 10),
        'Dash ready': (-50, -90, 50, 7),
        'Sphere ready': (-50, -68, 50, 62),
        'Sphere': (-50, -60, 50, 72),
        'Sphere end': (-50, -98, 50, 80),
        'Throw ready': (-50, -100, 50, 70),
        'Throw': (-50, -90, 50, 10),
        'Throw end': (-50, -90, 57, 10),
    }

    def __init__(self):
        self.pos = 5000, 300
        self.delta = 0, 0
        self.images = Hornet.load_images()
        self.sounds = Hornet.load_all_sounds()
        self.fall_image = None
        self.action = 'Idle'
        self.time = 0
        self.run_time = 0
        self.dash_time = 0
        self.throw_time = 0
        self.th_needle = None
        self.sphere_time = 0
        self.ball = None
        self.start_attack = False
        self.dash_cool = False
        self.jump_cool = False
        self.sphere_cool = False
        self.throw_cool = False
        self.fidx = 0
        self.flip = 'h'
        self.target = None
        self.health = 200
        self.slashed = None
        self.death_time = 0
        self.build_behavior_tree()

    def draw(self):
        pos = self.bg.to_screen(self.pos)
        if self.action != 'Dash ready' and self.action != 'Dash' and self.action != 'Dash end'\
                and self.action != 'Throw ready' and self.action != 'Throw' and self.action != 'Throw end'\
                and self.action != 'Flourish' and self.action != 'Death':
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

        landform.get_wall(self)
        l, foot, r, _ = self.get_bb()
        hx = (l + r) / 2
        landform.get_floor(self, hx, foot)
        if self.floor is not None:
            l, b, r, t = self.floor.get_bb()
            if self.action in ['Idle', 'Run']:
                if foot > t:
                    self.action = 'Fall'
                    if self.fall_image is None:
                        images = self.images['Jump']
                        self.fall_image = images[len(images) - 1]

        if self.action != 'Death':
            if self.health <= 0:
                self.action = 'Death'
                self.sounds[Hornet.SOUND_NUM['Death']].play()
                self.bgm.stop()
                self.time = 0
                self.fdix = 0
                if self.th_needle is not None:
                    gfw.world.remove(self.th_needle)
                if self.ball is not None:
                    gfw.world.remove(self.ball)
                self.wounded_anim_end = False
        self.bt.run()

    def idle(self):
        cool = random.choice(['jump', 'sphere', 'dash', 'throw'])
        self.jump_cool = False
        self.sphere_cool = False
        self.dash_cool = False
        self.throw_cool = False
        if cool == 'jump':
            self.jump_cool = True
        elif cool == 'sphere':
            self.jump_cool = True
            self.sphere_cool = True
        elif cool == 'dash':
            self.dash_cool = True
        elif cool == 'throw':
            self.throw_cool = True
        if self.start_attack:
            return BehaviorTree.FAIL
        self.action = 'Idle'
        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if gobj.distance(self.pos, self.target.pos) < 500:
            if self.start_attack == False:
                self.start_attack = True
                if self.pos[0] < self.target.pos[0]:
                    self.flip = 'h'
                else:
                    self.flip = ''
                self.time = 0
                self.action = 'Flourish'
                self.bgm = gfw.sound.load_m('res/Sound/hornet/S45 HORNET-110.mp3')
                self.bgm.repeat_play()
                self.sounds[Hornet.SOUND_NUM['Flourish']].play()
        return BehaviorTree.SUCCESS

    def flourish(self):
        if self.action != 'Flourish':
            return BehaviorTree.FAIL
        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Flourish']) - 1:
            self.action = 'Idle'
            self.fidx = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def wounded(self):
        if self.action != 'Death':
            return BehaviorTree.FAIL
        self.death_time += gfw.delta_time
        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS

        dx, dy = self.delta
        dy -= gravity
        dy = clamp(-15, dy, 15)
        self.delta = (dx, dy)
        landform.move(self)
        _, foot, _, _ = self.get_bb()
        if self.floor is not None:
            l, b, r, t = self.floor.get_bb()
            if foot <= t:
                x, y = self.pos
                self.pos = x, y + t - foot
                self.delta = (0, 0)

        if self.wounded_anim_end:
            self.fidx = int(frame) % 5 + (len(self.images[self.action]) - 5)
        else:
            self.fidx = int(frame) % len(self.images[self.action])
            if self.fidx == len(self.images[self.action]) - 1:
                self.wounded_anim_end = True
        if self.fidx == len(self.images['Death']) - 1:
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def jump_ready(self):
        if self.action == 'Death':
            return BehaviorTree.FAIL
        if self.action != 'Jump ready':
            if self.jump_cool:
                self.action = 'Jump ready'
                self.time = 0
            else:
                return BehaviorTree.FAIL

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Jump ready']) - 1:
            self.action = 'Jump'
            self.sounds[Hornet.SOUND_NUM['Jump']].play()
            self.sounds[random.choice([0, 2, 4])].play()
            self.time = 0
            dx = random.randint(1, 8)
            if self.pos[0] < self.target.pos[0]:
                self.delta = (dx, 30)
            else:
                self.delta = (-dx, 30)
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def jump(self):
        if self.action != 'Jump':
            return BehaviorTree.FAIL

        dx, dy = self.delta
        dy -= gravity
        dy = clamp(0, dy, 15)
        self.delta = (dx, dy)

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])

        landform.get_ceiling(self)
        tempX, tempY = self.pos
        gobj.move_obj(self)
        l, _, r, t = self.get_bb_real()
        if l <= self.wall_l or r >= self.wall_r:
            self.pos = tempX, self.pos[1]
        if t >= self.ceiling:
            self.pos = tempX, tempY
            self.delta = dx, 0
            self.action = 'Fall'
            self.time = 0
            images = self.images['Jump']
            self.fall_image = images[len(images) - 1]
            return BehaviorTree.SUCCESS

        if self.fidx == len(self.images['Jump']) - 1:
            self.action = 'Fall'
            self.time = 0
            images = self.images['Jump']
            self.fall_image = images[len(images) - 1]
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def fall(self):
        if self.action != 'Fall':
            return BehaviorTree.FAIL

        dx, dy = self.delta
        dy -= gravity
        dy = clamp(-15, dy, 15)
        self.delta = (dx, dy)
        landform.move(self)
        self.time += gfw.delta_time

        _, foot, _, _ = self.get_bb()
        if self.floor is not None:
            l, b, r, t = self.floor.get_bb()
            if foot <= t:
                x, y = self.pos
                self.pos = x, y + t - foot
                dx, dy = self.delta
                self.delta = (dx, 0)
                self.action = 'Land'
                self.sounds[Hornet.SOUND_NUM['Land']].play()
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
        if self.action == 'Death':
            return BehaviorTree.FAIL
        if self.action != 'Sphere ready':
            if self.sphere_cool:
                self.action = 'Sphere ready'
                self.sounds[random.choice([1, 3, 5, 6])].play()
                self.time = 0
            else:
                return BehaviorTree.FAIL

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Sphere ready']) - 1:
            self.action = 'Sphere'
            self.ball = Sphere_Ball(self)
            gfw.world.add(gfw.layer.needle, self.ball)
            self.sphere_anim_end = False
            self.sounds[Hornet.SOUND_NUM['Sphere']].play()
            self.time = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def sphere(self):
        if self.action != 'Sphere':
            return BehaviorTree.FAIL

        self.time += gfw.delta_time
        self.sphere_time += gfw.delta_time
        frame = self.time * Hornet.FPS
        if self.sphere_anim_end:
            self.fidx = int(frame) % 4 + (len(self.images[self.action]) - 4)
        else:
            self.fidx = int(frame) % len(self.images[self.action])
            if self.fidx == len(self.images[self.action]) - 1:
                self.sphere_anim_end = True
        if self.sphere_time > Hornet.SPHERE_MAX_TIME:
            self.sphere_time = 0
            self.action = 'Sphere end'
            gfw.world.remove(self.ball)
            self.ball = None
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
        if self.action == 'Death' or self.action == 'Fall':
            return BehaviorTree.FAIL
        if self.action != 'Run':
            self.run_time = random.random()
            self.action = 'Run'
            self.sounds[Hornet.SOUND_NUM['Run']].play()
        if self.pos[0] < self.target.pos[0]:
            self.delta = -3, 0
        else:
            self.delta = 3, 0

        landform.move(self)
        self.time += gfw.delta_time
        self.run_time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])

        if self.run_time > Hornet.RUN_MAX_TIME:
            self.delta = 0, 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def dash_ready(self):
        if self.action == 'Death':
            return BehaviorTree.FAIL
        if self.action != 'Dash ready':
            if self.dash_cool:
                self.action = 'Dash ready'
                self.sounds[random.choice([1, 3])].play()
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
            self.sounds[Hornet.SOUND_NUM['Dash']].play()
            self.time = 0
            if self.flip == 'h':
                self.delta = 25, 0
            else:
                self.delta = -25, 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def dash(self):
        if self.action != 'Dash':
            return BehaviorTree.FAIL

        landform.move(self)
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

    def throw_ready(self):
        if self.action == 'Death':
            return BehaviorTree.FAIL
        if self.action != 'Throw ready':
            if self.throw_cool:
                self.action = 'Throw ready'
                self.sounds[random.choice([1, 3, 5, 6])].play()
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
        if self.fidx == len(self.images['Throw ready']) - 1:
            self.action = 'Throw'
            self.th_needle = Throw_Needle(self)
            if self.flip == 'h':
                self.th_needle.delta = 30, 0
            else:
                self.th_needle.delta = -30, 0
            gfw.world.add(gfw.layer.needle, self.th_needle)
            self.sounds[Hornet.SOUND_NUM['Throw']].play()
            self.time = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def throw(self):
        if self.action != 'Throw':
            return BehaviorTree.FAIL

        self.throw_time += gfw.delta_time
        if self.fidx != len(self.images[self.action]) - 1:
            self.time += gfw.delta_time
            frame = self.time * Hornet.FPS
            self.fidx = int(frame) % len(self.images[self.action])

        if self.throw_time >= Hornet.THROW_MAX_TIME:
            l,_,r,_ = self.th_needle.get_bb()
            hl,_,hr,_ = self.get_bb()
            if self.flip == 'h':
                if l <= hl:
                    self.throw_time = 0
                    self.action = 'Throw end'
                    gfw.world.remove(self.th_needle)
                    self.th_needle = None
                    self.time = 0
                    return BehaviorTree.SUCCESS
            else:
                if r >= hr:
                    self.throw_time = 0
                    self.action = 'Throw end'
                    gfw.world.remove(self.th_needle)
                    self.th_needle = None
                    self.time = 0
                    return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def throw_end(self):
        if self.action != 'Throw end':
            return BehaviorTree.FAIL

        self.time += gfw.delta_time
        frame = self.time * Hornet.FPS
        self.fidx = int(frame) % len(self.images[self.action])
        if self.fidx == len(self.images['Throw end']) - 1:
            self.sounds[Hornet.SOUND_NUM['Catch']].play()
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
                    "name": "Flourish",
                    "class": LeafNode,
                    "function": self.flourish,
                },
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
                    "name": "Throw",
                    "class": SequenceNode,
                    "children": [
                        {
                            "name": "throw ready",
                            "class": LeafNode,
                            "function": self.throw_ready,
                        },
                        {
                            "name": "throw",
                            "class": LeafNode,
                            "function": self.throw,
                        },
                        {
                            "name": "throw end",
                            "class": LeafNode,
                            "function": self.throw_end,
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
        for action in Hornet.IMAGE_LIST:
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

    @staticmethod
    def load_sound(sound):
        if sound in Hornet.sounds:
            return Hornet.sounds[sound]

        file_fmt = 'res/Sound/hornet/%s'
        fn = file_fmt % sound
        s = gfw.sound.load_w(fn)
        Hornet.sounds[sound] = s
        print('%s sound loaded' % (sound))
        return s

    @staticmethod
    def load_all_sounds():
        sounds = []
        sounds.append(Hornet.load_sound('Hornet_Fight_Yell_03.wav'))
        sounds.append(Hornet.load_sound('Hornet_Fight_Yell_04.wav'))
        sounds.append(Hornet.load_sound('Hornet_Fight_Yell_05.wav'))
        sounds.append(Hornet.load_sound('Hornet_Fight_Yell_06.wav'))
        sounds.append(Hornet.load_sound('Hornet_Fight_Yell_07.wav'))
        sounds.append(Hornet.load_sound('Hornet_Fight_Yell_08.wav'))
        sounds.append(Hornet.load_sound('Hornet_Fight_Yell_09.wav'))
        sounds.append(Hornet.load_sound('Hornet_Fight_Death_01.wav'))
        sounds.append(Hornet.load_sound('hornet_dash.wav'))
        sounds.append(Hornet.load_sound('hornet_footstep_run_loop.wav'))
        sounds.append(Hornet.load_sound('hornet_ground_land.wav'))
        sounds.append(Hornet.load_sound('hornet_jump.wav'))
        sounds.append(Hornet.load_sound('hornet_needle_throw.wav'))
        sounds.append(Hornet.load_sound('hornet_needle_throw_and_return.wav'))
        sounds.append(Hornet.load_sound('hornet_needle_catch.wav'))
        sounds.append(Hornet.load_sound('Hornet_Fight_Flourish_02.wav'))
        return sounds

    def get_bb(self):
        x, y = self.bg.to_screen(self.pos)
        if self.action != 'Fall':
            l, b, r, t = Hornet.BB_DIFFS[self.action]
        else:
            l, b, r, t = Hornet.BB_DIFFS['Jump']
        if self.flip == '':
            return x + l, y + b, x + r, y + t
        else:
            return x - r, y + b, x - l, y + t

    def get_bb_real(self):
        x, y = self.pos
        if self.action != 'Fall':
            l, b, r, t = Hornet.BB_DIFFS[self.action]
        else:
            l, b, r, t = Hornet.BB_DIFFS['Jump']
        if self.flip == '':
            return x + l, y + b, x + r, y + t
        else:
            return x - r, y + b, x - l, y + t