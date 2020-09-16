# 캐릭터 움직이기 - 더블 버퍼링

from pico2d import *
open_canvas()

cha = load_image('../resource/animation_sheet.png')
gra = load_image('../resource/grass.png')

x = 0
frame_idx = 0
action = 0
while x < 800:
    clear_canvas()          # game rendering
    gra.draw(400, 30)
    cha.clip_draw(100 * frame_idx, 100 * action, 100, 100, x, 85)
    update_canvas()

    get_events()

    x += 2
    if x % 100 == 0:
        action = (action + 1) % 4
    frame_idx = (frame_idx + 1) % 8
    delay(0.01)

close_canvas()