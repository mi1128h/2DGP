# 캐릭터 움직이기 - 더블 버퍼링

from pico2d import *
open_canvas()

cha = load_image('../resource/character.png')
gra = load_image('../resource/grass.png')

x = 0
while x < 800:
    clear_canvas_now()          # game rendering
    gra.draw_now(400, 30)
    cha.draw_now(x, 85)

    x += 2      # game logic
    delay(0.01)

close_canvas()

# game loop:
#   - update() - logic
#   - event handling
#   - draw() - render
