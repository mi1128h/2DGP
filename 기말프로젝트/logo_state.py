import gfw
from pico2d import *
import title_state
import gobj

canvas_width = 1280
canvas_height = 720
elapsed = 0

def enter():
    gfw.world.init(['logo'])
    logo = gobj.ImageObject('logo.png', (canvas_width // 2, canvas_height // 2))
    gfw.world.add(gfw.layer.logo, logo)

def update():
    gfw.world.update()
    global elapsed
    elapsed += gfw.delta_time
    if elapsed > 1.5:
        gfw.change(title_state)

def draw():
    gfw.world.draw()

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.quit()

def exit():
    pass


def pause():
    pass


def resume():
    pass


if __name__ == '__main__':
    gfw.run_main()
