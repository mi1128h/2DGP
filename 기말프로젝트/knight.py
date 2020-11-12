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

gravity = 0.4

class IdleState:
    @staticmethod
    def get(knight):
        if not hasattr(IdleState, 'singleton'):
            IdleState.singleton = IdleState()
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
        image.composite_draw(0, self.knight.flip, *self.knight.pos, image.w, image.h)

    def update(self):
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * len(self.images) * 2
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

class WalkState:
    @staticmethod
    def get(knight):
        if not hasattr(WalkState, 'singleton'):
            WalkState.singleton = WalkState()
            WalkState.singleton.knight = knight
        return WalkState.singleton

    def __init__(self):
        self.images = load_images('Walk')

    def enter(self):
        self.time = 0
        self.fidx = 0

    def exit(self):
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos, image.w, image.h)

    def update(self):
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * len(self.images) * 2
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

class FallState:
    @staticmethod
    def get(knight):
        if not hasattr(FallState, 'singleton'):
            FallState.singleton = FallState()
            FallState.singleton.knight = knight
        return FallState.singleton

    def __init__(self):
        self.images = load_images('Fall')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.clockFlap = False

    def exit(self):
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos, image.w, image.h)

    def update(self):
        dx, dy = self.knight.delta
        dy -= gravity
        dy = clamp(-10, dy, 15)
        self.knight.delta = (dx, dy)
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * len(self.images) * 2
        if self.clockFlap == False:
            self.fidx = int(frame) % len(self.images)
            if self.fidx == len(self.images) - 1:
                self.clockFlap = True
        else:
            self.fidx = int(frame) % 2 + (len(self.images) - 2)

        if self.knight.pos[1] <= 80:
            dx, dy = self.knight.delta
            self.knight.delta = (dx, 0)
            self.knight.set_state(IdleState)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Knight.KEY_MAP:
            self.knight.delta = gobj.point_add(self.knight.delta, Knight.KEY_MAP[pair])
        elif pair == Knight.KEYDOWN_d:
            self.knight.set_state(SlashState)

class JumpState:
    @staticmethod
    def get(knight):
        if not hasattr(JumpState, 'singleton'):
            JumpState.singleton = JumpState()
            JumpState.singleton.knight = knight
        return JumpState.singleton

    def __init__(self):
        self.images = load_images('Jump')

    def enter(self):
        self.time = 0
        self.fidx = 0

    def exit(self):
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos, image.w, image.h)

    def update(self):
        dx, dy = self.knight.delta
        dy -= gravity
        self.knight.delta = (dx, dy)
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * len(self.images) * 2 - 1
        self.fidx = int(frame) % len(self.images)

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

class SlashState:
    @staticmethod
    def get(knight):
        if not hasattr(SlashState, 'singleton'):
            SlashState.singleton = SlashState()
            SlashState.singleton.knight = knight
        return SlashState.singleton

    def __init__(self):
        self.images = load_images('Slash')
        self.images_effect = load_images('SlashEffect')

    def enter(self):
        self.time = 0
        self.fidx = 0
        slash = Slash(self.knight)
        gfw.world.add(gfw.layer.slash, slash)

    def exit(self):
        pass

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos, image.w, image.h)

    def update(self):
        dx, dy = self.knight.delta
        if self.knight.pos[1] <= 80:
            dy = 0
        else:
            dy -= gravity
            dy = clamp(-10, dy, 15)
        self.knight.delta = (dx, dy)
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * len(self.images) * 4

        if frame < len(self.images):
            self.fidx = int(frame)
        else:
            if self.knight.delta[1] < 0:
                self.knight.set_state(FallState)
            else:
                self.knight.set_state(IdleState)

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
        return RecoilState.singleton

    def __init__(self):
        self.images = load_images('Recoil')

    def enter(self):
        self.time = 0
        self.fidx = 0
        self.tempdelta = self.knight.delta

    def exit(self):
        self.knight.delta = self.tempdelta

    def draw(self):
        image = self.images[self.fidx]
        image.composite_draw(0, self.knight.flip, *self.knight.pos, image.w, image.h)

    def update(self):
        if self.knight.flip == 'h':
            self.knight.delta = (-2, 1)
        elif self.knight.flip == '':
            self.knight.delta = (2, 1)
        gobj.move_obj(self.knight)
        self.time += gfw.delta_time
        gobj.move_obj(self.knight)
        frame = self.time * len(self.images) * 2
        self.fidx = int(frame) % len(self.images)

        if frame < len(self.images):
            self.fidx = int(frame)
        else:
            self.knight.set_state(FallState)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Knight.KEY_MAP:
            self.tempdelta = gobj.point_add(self.tempdelta, Knight.KEY_MAP[pair])
        pass

class Knight:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  (-3, 0),
        (SDL_KEYDOWN, SDLK_RIGHT): (3, 0),
        (SDL_KEYUP, SDLK_LEFT):    (3, 0),
        (SDL_KEYUP, SDLK_RIGHT):   (-3, 0)
    }
    KEYDOWN_SPACE = (SDL_KEYDOWN, SDLK_SPACE)
    KEYUP_SPACE = (SDL_KEYUP, SDLK_SPACE)
    KEYDOWN_d = (SDL_KEYDOWN, SDLK_d)
    images = {}
    Unbeatable_Time = 2.0
    def __init__(self):
        self.pos = get_canvas_width() // 2, get_canvas_height()
        self.delta = 0, 0
        self.time = 0.0
        self.fidx = 0
        self.flip = 'h'
        self.mask = 5
        self.state = None
        self.set_state(FallState)

    def set_state(self, clazz):
        if self.state != None:
            self.state.exit()
        self.state = clazz.get(self)
        self.state.enter()

    def draw(self):
        self.state.draw()

    def update(self):
        self.state.update()
        self.time += gfw.delta_time

    def handle_event(self, e):
        # flip 설정
        pair = (e.type, e.key)
        if pair == (SDL_KEYDOWN, SDLK_LEFT):
           self.flip = ''
        elif pair == (SDL_KEYDOWN, SDLK_RIGHT):
           self.flip = 'h'

        self.state.handle_event(e)

    def get_bb(self):
        x,y = self.pos
        return x - 20, y - 60, x + 20, y + 50