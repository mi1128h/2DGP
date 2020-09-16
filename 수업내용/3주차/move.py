# 캐릭터 움직이기

from pico2d import *
open_canvas()

cha = load_image('../resource/character.png')

for s in range(100,300):
    clear_canvas_now()
    for y in range(100, 501, 100):
        for x in range(s,701,100):
            cha.draw_now(x,y)
