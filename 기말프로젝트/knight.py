from pico2d import *
import gfw
import gobj
from slash import Slash

def load_images(action):
    if action in Knight.images:
        return Knight.images[action]

    count = 0
    file_fmt = '%s/knight/%s/%s (%d).png'
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
    Knight.images[action] = action_images
    print('%s %d images loaded' % (action, count))
    return action_images
def load_sound(sound):
    if sound in Knight.sounds:
        return Knight.sounds[sound]

    file_fmt = 'res/Sound/knight/%s'
    fn = file_fmt % sound
    s = gfw.sound.load_w(fn)
    Knight.sounds[sound] = s
    print('%s sound loaded' % (sound))
    return s

gravity = 0.4
floor = 480

class IdleState:
    @staticmethod
    def get(knight):
        if not hasattr(IdleState, 'singleton'):
            IdleState.singleton = IdleState()
            IdleState.singleton.knight = knight
        else:
            IdleState.singleton.knight = knight
        return IdleState.singleton

    def __init__(self):
        self.images = load_images('Idle')

    def enter(self):
        self.time = 0
        self.fidx = 0

    def exit(self):
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos_translated, image.w, image.h)

    def update(self):
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * Knight.FPS
        self.fidx = int(frame) % len(self.images)

        if self.knight.delta[0] != 0:
            self.knight.set_state(WalkState)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Knight.KEY_MAP:
            self.knight.delta = gobj.point_add(self.knight.delta, Knight.KEY_MAP[pair])
        elif pair == Knight.KEYDOWN_SPACE:
            dx, dy = self.knight.delta
            dy = 15
            self.knight.delta = (dx, dy)
            self.knight.set_state(JumpState)
        elif pair == Knight.KEYDOWN_d:
            self.knight.set_state(SlashState)

    def get_name(self):
        return 'Idle'

class WalkState:
    @staticmethod
    def get(knight):
        if not hasattr(WalkState, 'singleton'):
            WalkState.singleton = WalkState()
            WalkState.singleton.knight = knight
        else:
            WalkState.singleton.knight = knight
        return WalkState.singleton

    def __init__(self):
        self.images = load_images('Walk')
        self.walk_sound = load_sound('hero_walk_footsteps_stone.wav')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.walk_sound.play()

    def exit(self):
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos_translated, image.w, image.h)

    def update(self):
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * Knight.FPS
        self.fidx = int(frame) % len(self.images)
        if self.knight.delta[0] == 0:
            self.knight.set_state(IdleState)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Knight.KEY_MAP:
            self.knight.delta = gobj.point_add(self.knight.delta, Knight.KEY_MAP[pair])
        elif pair == Knight.KEYDOWN_SPACE:
            dx, dy = self.knight.delta
            dy = 15
            self.knight.delta = (dx, dy)
            self.knight.set_state(JumpState)
        elif pair == Knight.KEYDOWN_d:
            self.knight.set_state(SlashState)

    def get_name(self):
        return 'Walk'

class FallState:
    @staticmethod
    def get(knight):
        if not hasattr(FallState, 'singleton'):
            FallState.singleton = FallState()
            FallState.singleton.knight = knight
        else:
            FallState.singleton.knight = knight
        return FallState.singleton

    def __init__(self):
        self.images = load_images('Fall')
        self.land_sound = load_sound('hero_land_soft.wav')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.clockFlap = False

    def exit(self):
        self.land_sound.play()
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos_translated, image.w, image.h)

    def update(self):
        dx, dy = self.knight.delta
        dy -= gravity
        dy = clamp(-10, dy, 15)
        self.knight.delta = (dx, dy)
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * Knight.FPS
        if self.clockFlap == False:
            self.fidx = int(frame) % len(self.images)
            if self.fidx == len(self.images) - 1:
                self.clockFlap = True
        else:
            self.fidx = int(frame) % 3 + (len(self.images) - 3)

        if self.knight.pos[1] <= floor:
            dx, dy = self.knight.delta
            self.knight.delta = (dx, 0)
            self.knight.set_state(IdleState)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Knight.KEY_MAP:
            self.knight.delta = gobj.point_add(self.knight.delta, Knight.KEY_MAP[pair])
        elif pair == Knight.KEYDOWN_d:
            self.knight.set_state(SlashState)

    def get_name(self):
        return 'Fall'

class JumpState:
    @staticmethod
    def get(knight):
        if not hasattr(JumpState, 'singleton'):
            JumpState.singleton = JumpState()
            JumpState.singleton.knight = knight
        else:
            JumpState.singleton.knight = knight
        return JumpState.singleton

    def __init__(self):
        self.images = load_images('Jump')
        self.jump_sound = load_sound('hero_jump.wav')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.jump_sound.play()

    def exit(self):
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos_translated, image.w, image.h)

    def update(self):
        dx, dy = self.knight.delta
        dy -= gravity
        self.knight.delta = (dx, dy)
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        tfidx = self.fidx
        frame = self.time * Knight.FPS
        self.fidx = int(frame) % len(self.images)
        if self.fidx < tfidx:
            self.fidx = tfidx

        if dy <= 0:
            self.knight.set_state(FallState)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Knight.KEY_MAP:
            self.knight.delta = gobj.point_add(self.knight.delta, Knight.KEY_MAP[pair])
        elif pair == Knight.KEYUP_SPACE:
            dx, dy = self.knight.delta
            self.knight.delta = (dx, 0)
            self.knight.set_state(FallState)
        elif pair == Knight.KEYDOWN_d:
            self.knight.set_state(SlashState)

    def get_name(self):
        return 'Jump'

class SlashState:
    @staticmethod
    def get(knight):
        if not hasattr(SlashState, 'singleton'):
            SlashState.singleton = SlashState()
            SlashState.singleton.knight = knight
        else:
            SlashState.singleton.knight = knight
        return SlashState.singleton

    def __init__(self):
        self.images = load_images('Slash')
        self.images_effect = load_images('SlashEffect')
        self.slash_sound = load_sound('sword_1.wav')

    def enter(self):
        self.time = 0
        self.fidx = 0
        slash = Slash(self.knight)
        gfw.world.add(gfw.layer.slash, slash)
        self.slash_sound.play()

    def exit(self):
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos_translated, image.w, image.h)

    def update(self):
        dx, dy = self.knight.delta
        if self.knight.pos[1] <= floor:
            dy = 0
        else:
            dy -= gravity
            dy = clamp(-10, dy, 15)
        self.knight.delta = (dx, dy)
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * Knight.FPS * 2

        if frame < len(self.images):
            self.fidx = int(frame)
        else:
            if self.knight.pos[1] > floor:
                self.knight.set_state(FallState)
            else:
                self.knight.set_state(IdleState)

    def get_name(self):
        return 'Slash'

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Knight.KEY_MAP:
            self.knight.delta = gobj.point_add(self.knight.delta, Knight.KEY_MAP[pair])
        elif pair == Knight.KEYUP_SPACE:
            dx, dy = self.knight.delta
            self.knight.delta = (dx, 0)

class RecoilState:
    @staticmethod
    def get(knight):
        if not hasattr(RecoilState, 'singleton'):
            RecoilState.singleton = RecoilState()
            RecoilState.singleton.knight = knight
        else:
            RecoilState.singleton.knight = knight
        return RecoilState.singleton

    def __init__(self):
        self.images = load_images('Recoil')
        self.damage_sound = load_sound('hero_damage.wav')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.tempdelta = self.knight.delta[0], 0
        self.damage_sound.play()

    def exit(self):
        self.knight.delta = self.tempdelta

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos_translated, image.w, image.h)

    def update(self):
        gobj.move_obj(self.knight)
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * Knight.FPS * 2
        self.fidx = int(frame) % len(self.images)

        if frame < len(self.images):
            self.fidx = int(frame)
        else:
            self.knight.set_state(FallState)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Knight.KEY_MAP:
            self.tempdelta = gobj.point_add(self.tempdelta, Knight.KEY_MAP[pair])

    def get_name(self):
        return 'Recoil'

class DeathState:
    @staticmethod
    def get(knight):
        if not hasattr(DeathState, 'singleton'):
            DeathState.singleton = DeathState()
            DeathState.singleton.knight = knight
        else:
            DeathState.singleton.knight = knight
        return DeathState.singleton

    def __init__(self):
        self.images = load_images('Death')
        self.damage_sound = load_sound('hero_damage.wav')
        self.death_sound = load_sound('hero_death_extra_details.wav')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.knight.delta = (0, 0)
        self.damage_sound.play()
        self.death_sound.play()

    def exit(self):
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos_translated, image.w, image.h)

    def update(self):
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * Knight.FPS * 2
        if frame < len(self.images):
            self.fidx = int(frame)
        else:
            self.knight.mask = 0

    def handle_event(self, e):
        pass

    def get_name(self):
        return 'Death'

class Knight:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  (-5, 0),
        (SDL_KEYDOWN, SDLK_RIGHT): (5, 0),
        (SDL_KEYUP, SDLK_LEFT):    (5, 0),
        (SDL_KEYUP, SDLK_RIGHT):   (-5, 0)
    }
    KEYDOWN_SPACE = (SDL_KEYDOWN, SDLK_SPACE)
    KEYUP_SPACE = (SDL_KEYUP, SDLK_SPACE)
    KEYDOWN_d = (SDL_KEYDOWN, SDLK_d)
    images = {}
    sounds = {}
    Unbeatable_Time = 1.3
    FPS = 10
    def __init__(self):
        if len(Knight.images) == 0:
            Knight.load_all_images()
        self.pos = 750, 3232
        self.radius = 95
        self.delta = 0, 0
        self.time = 0.0
        self.fidx = 0
        self.flip = 'h'
        self.mask = 5
        self.state = None
        self.set_state(FallState)

    @staticmethod
    def load_all_images():
        for action in ['Idle', 'Walk', 'Fall', 'Jump', 'Slash', 'SlashEffect', 'Recoil', 'Death']:
            load_images(action)

    def set_state(self, clazz):
        if self.state != None:
            self.state.exit()
        self.state = clazz.get(self)
        self.state.enter()

    def draw(self):
        self.pos_translated = self.bg.to_screen(self.pos)
        self.state.draw()

    def update(self):
        x, y = self.pos
        bg_l, bg_b, bg_r, bg_t = self.bg.get_boundary()
        x = clamp(bg_l, x, bg_r)
        y = clamp(bg_b, y, bg_t)
        self.pos = x, y
        self.state.update()
        self.time += gfw.delta_time
        # flip 설정
        if self.state.get_name() != 'Recoil':
            tflip = self.flip
            if self.delta[0] > 0:
                self.flip = 'h'
            elif self.delta[0] < 0:
                self.flip = ''
            else:
                self.flip = tflip

    def handle_event(self, e):
        self.state.handle_event(e)

    def get_bb(self):
        x,y = self.bg.to_screen(self.pos)
        return x - 20, y - 60, x + 20, y + 50