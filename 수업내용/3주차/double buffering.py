# 캐릭터 움직이기 - 더블 버퍼링

from pico2d import *
open_canvas()

cha = load_image('../resource/character.png')
gra = load_image('../resource/grass.png')

x = 0
while x < 800:
    clear_canvas()          # game rendering
    gra.draw(400, 30)
    cha.draw(x, 85)
    update_canvas()

    get_events()

    x += 2
    delay(0.01)

close_canvas()