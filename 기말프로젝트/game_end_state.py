import os.path
import gfw
from pico2d import *
import gobj
import title_state

canvas_width = 1280
canvas_height = 720

def enter():
    gfw.world.init(['result'])

    over = gobj.ImageObject('GameOver.png', (canvas_width // 2, canvas_height // 2))
    gfw.world.add(gfw.layer.result, over)

    global end_bgm
    end_bgm = gfw.sound.load_m('res/Sound/Hollow Shade Music.mp3')
    end_bgm.repeat_play()

def update():
    pass

def draw():
    gfw.world.draw()

def handle_event(e):
   if e.type == SDL_KEYDOWN or e.type == SDL_MOUSEBUTTONDOWN:
       gfw.change(title_state)
   elif e.type == SDL_QUIT:
       gfw.quit()

def exit():
    global end_bgm
    end_bgm.stop()
    gfw.sound.unload_m('res/Sound/Hollow Shade Music.mp3')
    gfw.world.clear()

def pause():
    pass
def resume():
    pass

if __name__ == '__main__':
    gfw.run_main()
