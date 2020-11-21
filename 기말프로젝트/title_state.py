import gfw
from pico2d import *
import loading_state
import gobj

canvas_width = 1280
canvas_height = 720
select = 'start'

def build_world():
    global title_bg, menu_pointer
    gfw.world.init(['title_bg', 'menu_pointer'])
    title_bg = gobj.ImageObject('title.png', (canvas_width // 2, canvas_height // 2))
    gfw.world.add(gfw.layer.title_bg, title_bg)

    menu_pointer = gobj.ImageObject('menu_pointer.png', (canvas_width // 2, canvas_height // 4))
    gfw.world.add(gfw.layer.menu_pointer, menu_pointer)

    global title_bgm, change_selection, button_confirm
    title_bgm = gfw.sound.load_m('res/Sound/Title.mp3')
    change_selection = gfw.sound.load_w('res/Sound/ui_change_selection.wav')
    button_confirm = gfw.sound.load_w('res/Sound/ui_button_confirm.wav')
    title_bgm.repeat_play()

def enter():
    build_world()

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
            if select == 'exit':
                change_selection.play()
            select = 'start'
            menu_pointer.pos = (canvas_width // 2, canvas_height // 4)
        elif e.key == SDLK_DOWN:
            if select == 'start':
                change_selection.play()
            select = 'exit'
            menu_pointer.pos = (canvas_width // 2, canvas_height // 6 + 17)
        elif e.key == SDLK_RETURN:
            button_confirm.play()
            if select == 'start':
                gfw.push(loading_state)
            elif select == 'exit':
                gfw.quit()
    elif e.type == SDL_MOUSEMOTION:
        if get_canvas_height() - e.y - 1 >= canvas_height // 4 - 10:
            if select == 'exit':
                change_selection.play()
            select = 'start'
            menu_pointer.pos = (canvas_width // 2, canvas_height // 4)
        else:
            if select == 'start':
                change_selection.play()
            select = 'exit'
            menu_pointer.pos = (canvas_width // 2, canvas_height // 6 + 17)
    elif e.type == SDL_MOUSEBUTTONDOWN:
        x = canvas_width // 2
        y1 = canvas_height // 4
        y2 = canvas_height // 6 + 17
        if abs(e.x - x) <= 80:
            if abs(get_canvas_height() - e.y - 1 - y1) <= 10:
                button_confirm.play()
                select = 'start'
                gfw.push(loading_state)
            elif abs(get_canvas_height() - e.y - 1 - y2) <= 10:
                button_confirm.play()
                select = 'exit'
                gfw.quit()

def exit():
    global title_bgm, change_selection, button_confirm
    title_bgm.stop()
    gfw.sound.unload_m('res/Sound/Title.mp3')
    gfw.sound.unload_w('res/Sound/ui_change_selection.wav')
    gfw.sound.unload_w('res/Sound/ui_button_confirm.wav')
    gfw.world.clear()

def pause():
    global title_bgm
    title_bgm.stop()
    gfw.world.clear()

def resume():
    build_world()

if __name__ == '__main__':
    gfw.run_main()
