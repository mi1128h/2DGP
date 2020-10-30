import gfw
from pico2d import *
import main_state
import gobj

canvas_width = 1280
canvas_height = 720
select = 'start'

def enter():
    global title_bg, menu_pointer
    gfw.world.init(['title_bg', 'menu_pointer'])
    title_bg = gobj.ImageObject('title_1280.png', (canvas_width // 2, canvas_height // 2))
    gfw.world.add(gfw.layer.title_bg, title_bg)

    menu_pointer = gobj.ImageObject('menu_pointer.png', (canvas_width // 2, canvas_height // 4))
    gfw.world.add(gfw.layer.menu_pointer, menu_pointer)

def update():
    gfw.world.update()

def draw():
    gfw.world.draw()


def handle_event(e):
    global select, menu_pointer
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.quit()
        elif e.key == SDLK_UP:
            select = 'start'
            menu_pointer.pos = (canvas_width // 2, canvas_height // 4)
        elif e.key == SDLK_DOWN:
            select = 'exit'
            menu_pointer.pos = (canvas_width // 2, canvas_height // 6 + 17)
        elif e.key == SDLK_RETURN:
            if select == 'start':
                gfw.push(main_state)
            elif select == 'exit':
                gfw.quit()
    elif e.type == SDL_MOUSEMOTION:
        if get_canvas_height() - e.y - 1 >= canvas_height // 4 - 10:
            select = 'start'
            menu_pointer.pos = (canvas_width // 2, canvas_height // 4)
        else:
            select = 'exit'
            menu_pointer.pos = (canvas_width // 2, canvas_height // 6 + 17)
    elif e.type == SDL_MOUSEBUTTONDOWN:
        x = canvas_width // 2
        y1 = canvas_height // 4
        y2 = canvas_height // 6 + 17
        if abs(e.x - x) <= 80 :
            if abs(get_canvas_height() - e.y - 1 - y1) <= 10:
                select = 'start'
                gfw.push(main_state)
            elif abs(get_canvas_height() - e.y - 1 - y2) <= 10:
                select = 'exit'
                gfw.quit()

def exit():
    gfw.world.clear()

def pause():
    gfw.world.clear()

def resume():
    gfw.world.init(['title_bg', 'menu_pointer'])
    gfw.world.add(gfw.layer.title_bg, title_bg)
    gfw.world.add(gfw.layer.menu_pointer, menu_pointer)

if __name__ == '__main__':
    gfw.run_main()
