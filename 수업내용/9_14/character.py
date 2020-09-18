# 캐릭터 띄우기

from pico2d import *
open_canvas()

cha = load_image('../res/character.png')

for y in range(100, 501, 100):
    for x in range(100,701,100):
        cha.draw_now(x,y)

delay(1)
close_canvas()