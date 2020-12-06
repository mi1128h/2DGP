import os.path
import gfw
from pico2d import *
import gobj
import title_state

canvas_width = 1280
canvas_height = 720

GAME_CLEAR = False

def enter():
    gfw.world.init(['result'])
    global end_time, change
    end_time = 0
    change = False

    global clear_bgm, over_bgm

    if GAME_CLEAR:
        clear_bgm = gfw.sound.load_m('res/Sound/S30 White Palace.mp3')
        clear = gobj.ImageObject('GameClear.png', (canvas_width // 2, canvas_height // 2))
        clear_bgm.repeat_play()
        gfw.world.add(gfw.layer.result, clear)
    else:
        over_bgm = gfw.sound.load_m('res/Sound/Hollow Shade Music.mp3')
        over = gobj.ImageObject('GameOver.png', (canvas_width // 2, canvas_height // 2))
        over_bgm.repeat_play()
        gfw.world.add(gfw.layer.result, over)

def update():
    global end_time
    end_time += gfw.delta_time

def draw():
    gfw.world.draw()

def handle_event(e):
    global end_time, change
    if end_time > 2.0:
        if change == False:
            if e.type == SDL_KEYDOWN or e.type == SDL_MOUSEBUTTONDOWN:
                change = True
                gfw.change(title_state)
            elif e.type == SDL_QUIT:
                gfw.quit()

def exit():
    global clear_bgm, over_bgm
    if GAME_CLEAR:
        clear_bgm.stop()
        gfw.sound.unload_m('res/Sound/Hollow Shade Music.mp3')
    else:
        over_bgm.stop()
        gfw.sound.unload_m('res/Sound/Hollow Shade Music.mp3')
    gfw.world.clear()

def pause():
    pass
def resume():
    pass

if __name__ == '__main__':
    gfw.run_main()
