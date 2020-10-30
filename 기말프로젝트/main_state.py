import os.path
import gfw
from pico2d import *
from knight import Knight
import gobj

canvas_width = 1280
canvas_height = 720

def enter():
    gfw.world.init(['bg', 'knight'])

    bg = gobj.ImageObject('bg.png', (canvas_width // 2, canvas_height // 2))
    gfw.world.add(gfw.layer.bg, bg)

    global knight
    knight = Knight()
    gfw.world.add(gfw.layer.knight, knight)

def update():
    gfw.world.update()

def draw():
    gfw.world.draw()
    # gobj.draw_collision_box()

def handle_event(e):
    global knight
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

    knight.handle_event(e)

def exit():
    gfw.world.clear()

def pause():
    pass
def resume():
    pass

if __name__ == '__main__':
    gfw.run_main()
