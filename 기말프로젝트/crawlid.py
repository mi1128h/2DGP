from pico2d import *
import gfw
import gobj

def load_sound(sound):
    if sound in Crawlid.sounds:
        return Crawlid.sounds[sound]

    file_fmt = 'res/Sound/enemy/%s'
    fn = file_fmt % sound
    s = gfw.sound.load_w(fn)
    Crawlid.sounds[sound] = s
    print('%s sound loaded' % (sound))

class Crawlid:
    images = {}
    sounds = {}
    def __init__(self):
        if len(Crawlid.images) == 0:
            Crawlid.load_images()
        self.health = 10
        self.pos = (1200, 50)
        self.delta = (-1, 0)
        self.time = 0
        self.fidx = 0
        self.flip = ''
        self.action = 'Walk'
        self.slashed = None
        self.images = Crawlid.load_images()
        self.sounds = Crawlid.load_sounds()
        self.sounds['crawler.wav'].set_volume(50)
        self.sounds['crawler.wav'].repeat_play()

    @staticmethod
    def load_images():
        if len(Crawlid.images) != 0:
            return Crawlid.images

        images = {}
        count = 0
        file_fmt = '%s/crawlid/%s/%s (%d).png'
        for action in ['Walk', 'Death']:
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
        Crawlid.images = images
        print('crawlid %d images loaded' % (count))
        return images

    @staticmethod
    def load_sounds():
        load_sound('crawler.wav')
        load_sound('enemy_damage.wav')
        load_sound('enemy_death_sword.wav')
        return Crawlid.sounds

    def draw(self):
        images = self.images[self.action]
        image = images[self.fidx % len(images)]
        image.composite_draw(0, self.flip, *self.pos, image.w, image.h)

    def update(self):
        if self.action != 'Death':
            if self.pos[0] <= 50:
                self.flip = 'h'
                self.delta = (1, 0)
            elif self.pos[0] >= get_canvas_width() - 50:
                self.flip = ''
                self.delta = (-1, 0)
            gobj.move_obj(self)
            self.time += gfw.delta_time
            frame = self.time * 10
            self.fidx = int(frame)
            if self.health == 0:
                self.sounds['enemy_death_sword.wav'].play()
                self.sounds['crawler.wav'].set_volume(0)
                self.action = 'Death'
                self.time = 0
                self.delta = (0, 0)
        else:
            self.time += gfw.delta_time
            frame = self.time * 10
            self.fidx = int(frame)
            self.fidx = clamp(0, self.fidx, len(self.images[self.action]) - 1)

    def handle_event(self):
        pass

    def get_bb(self):
        x, y = self.pos
        return x - 50, y - 30, x + 50, y + 30