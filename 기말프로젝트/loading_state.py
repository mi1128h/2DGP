from pico2d import *
import gfw
import gobj
import main_state

canvas_width = 1280
canvas_height = 720

cx = canvas_width // 2
cy = canvas_height // 2

def enter():
    global bg, index, loading_icon, time
    bg = gfw.image.load('res/Loding/loading_bg.png')

    loading_icon = []

    file_fmt = 'res/Loding/loading_icon (%d).png'
    for i in range(1, 8):
        fn = file_fmt % i
        loading_icon.append(gfw.image.load(fn))

    index = 0
    time = 0

    global frame_interval
    frame_interval = gfw.frame_interval
    gfw.frame_interval = 0

def exit():
    global bg, loading_icon
    gfw.image.unload('res/Loding/loading_bg.png')
    file_fmt = 'res/Loding/loading_icon (%d).png'
    for i in range(1, 8):
        fn = file_fmt % i
        gfw.image.unload(fn)

    del bg
    del loading_icon

    global frame_interval
    gfw.frame_interval = frame_interval

def update():
    image_count = len(IMAGE_FILES)
    global index, time
    if index < image_count:
        file = IMAGE_FILES[index]
        gfw.image.load(file)
    else:
        gfw.change(main_state)
        return
    index += 1
    time += gfw.delta_time

def draw():
    bg.draw(cx, cy)
    frame = time * len(loading_icon) * 3
    fidx = int(frame) % len(loading_icon)
    image = loading_icon[fidx]
    image.draw(get_canvas_width() - image.w, image.h)

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()


IMAGE_FILES = []

def make_IMAGE_LIST(file_fmt):
    global IMAGE_FILES
    n = 0
    while True:
        n += 1
        fn = file_fmt % n
        if os.path.isfile(fn):
            IMAGE_FILES.append(fn)
        else:
            break

file_fmt = 'res/crawlid/%s/%s'
for a in ['Death', 'Walk']:
    fn = file_fmt % (a, a) + ' (%d).png'
    make_IMAGE_LIST(fn)

file_fmt = 'res/HUD/Frame/%s/%s'
for a in ['Appear', 'Cracked', 'Idle']:
    fn = file_fmt % (a, a) + ' (%d).png'
    make_IMAGE_LIST(fn)

file_fmt = 'res/HUD/Health/%s/%s'
for a in ['Appear', 'Break', 'Empty', 'Idle']:
    fn = file_fmt % (a, a) + ' (%d).png'
    make_IMAGE_LIST(fn)

file_fmt = 'res/knight/%s/%s'
for a in ['Death', 'Fall', 'Idle', 'Jump', 'Recoil', 'Slash', 'SlashEffect', 'Walk']:
    fn = file_fmt % (a, a) + ' (%d).png'
    make_IMAGE_LIST(fn)

file_fmt = 'res/hornet/%s/%s'
for a in ['Dash', 'Dash end', 'Dash ready', 'Idle', 'Jump', 'Jump ready', 'Land',
          'Run', 'Sphere', 'Sphere ball', 'Sphere end', 'Sphere ready', 'Wounded']:
    fn = file_fmt % (a, a) + ' (%d).png'
    make_IMAGE_LIST(fn)

if __name__ == '__main__':
    gfw.run_main()
