import os.path
import gfw
from pico2d import *
import gobj
from knight import Knight, RecoilState
from crawlid import Crawlid

canvas_width = 1280
canvas_height = 720

def enter():
    gfw.world.init(['bg', 'platform', 'enemy', 'knight', 'slash', 'ui'])

    bg = gobj.ImageObject('bg.png', (canvas_width // 2, canvas_height // 2))
    gfw.world.add(gfw.layer.bg, bg)

    crawlid = Crawlid()
    gfw.world.add(gfw.layer.enemy, crawlid)

    global knight
    knight = Knight()
    gfw.world.add(gfw.layer.knight, knight)

def check_collide(e):
    global knight
    if gobj.collides_box(knight, e):
        if e.action != 'Death':
            if knight.time > Knight.Unbeatable_Time:
                if knight.mask > 1:
                    knight.time = 0.0
                    knight.mask -= 1
                    print(knight.mask)
                    knight.set_state(RecoilState)
               # elif knight.mask == 1:
                    #knight.set_state(DeathState)
                return

    for s in gfw.world.objects_at(gfw.layer.slash):
        if gobj.collides_box(s, e):
            if e.action != 'Death':
                e.health -= 5
                if knight.flip == 'h':
                    e.pos = gobj.point_add(e.pos, (100, 0))
                elif knight.flip == '':
                    e.pos = gobj.point_add(e.pos, (-100, 0))

def update():
    gfw.world.update()
    for e in gfw.world.objects_at(gfw.layer.enemy):
        check_collide(e)

def draw():
    gfw.world.draw()
    gobj.draw_collision_box()

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
