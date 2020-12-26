import os.path
import gfw
from pico2d import *
import gobj
from knight import Knight, RecoilState, DeathState
from crawlid import Crawlid
from hornet import Hornet
from HUD import Frame
import game_end_state
from background import FixedBackground
from pf import Platform
import landform

canvas_width = 1280
canvas_height = 720

def enter():
    gfw.world.init(['bg_base', 'bg_back', 'bg_platform', 'platform', 'enemy', 'hornet', 'needle', 'knight', 'slash', 'bg_front', 'ui'])

    bg_base = FixedBackground('res/map/base.png')
    gfw.world.add(gfw.layer.bg_base, bg_base)
    bg_back = FixedBackground('res/map/back.png')
    gfw.world.add(gfw.layer.bg_back, bg_back)
    bg_platform = FixedBackground('res/map/platform.png')
    gfw.world.add(gfw.layer.bg_platform, bg_platform)
    bg_front = FixedBackground('res/map/front.png')
    gfw.world.add(gfw.layer.bg_front, bg_front)

    global platform
    platform = Platform('res/map/platform.json')
    for r in platform.rects:
        r.bg = bg_platform
        gfw.world.add(gfw.layer.platform, r)

    crawlid = Crawlid()
    crawlid.bg = bg_platform
    gfw.world.add(gfw.layer.enemy, crawlid)

    global knight
    knight = Knight()
    knight.bg = bg_platform

    bg_back.target = knight
    bg_platform.target_bg = bg_back
    bg_front.target_bg = bg_back

    bg_back.update()
    bg_platform.update()
    bg_front.update()
    gfw.world.add(gfw.layer.knight, knight)

    global frame
    frame = Frame(knight)
    gfw.world.add(gfw.layer.ui, frame)

    global hornet
    hornet = Hornet()
    hornet.bg = bg_platform
    hornet.target = knight
    gfw.world.add(gfw.layer.hornet, hornet)

    global bgm, opening_sting, enemy_damaged
    bgm = gfw.sound.load_m('res/Sound/cave_wind_loop.mp3')
    opening_sting = gfw.sound.load_w('res/Sound/S75 Opening Sting-08.wav')
    enemy_damaged = gfw.sound.load_w('res/Sound/enemy_damage.wav')

    opening_sting.set_volume(50)
    bgm.repeat_play()
    opening_sting.play()

def knight_damaged_by(e):
    if knight.time > Knight.Unbeatable_Time and knight.mask > 0:
        knight.time = 0.0
        knight.mask -= 1
        frame.mask_stack[knight.mask].set_action('Break')
        if knight.mask > 0:
            knight.set_state(RecoilState)
            if knight.pos[0] <= e.pos[0]:
                knight.flip = 'h'
                knight.delta = (-2, 1)
            else:
                knight.flip = ''
                knight.delta = (2, 1)
        else:
            knight.set_state(DeathState)

def check_collide(e):
    global knight, frame
    if gobj.collides_box(knight, e):
        if e.action != 'Death':
            knight_damaged_by(e)

    for s in gfw.world.objects_at(gfw.layer.slash):
        if gobj.collides_box(s, e):
            if e.action != 'Death' and e.slashed != s:
                enemy_damaged.play()
                e.slashed = s
                e.health -= 5
                if s.flip == 'h':
                    temp = e.delta
                    e.delta = (100, 0)
                    landform.move(e)
                    e.delta = temp
                elif s.flip == '':
                    temp = e.delta
                    e.delta = (-100, 0)
                    landform.move(e)
                    e.delta = temp

def check_collides_needle():
    global knight, hornet
    if hornet.ball is not None:
        if gobj.collides_distance(knight, hornet.ball):
            knight_damaged_by(hornet.ball)
    elif hornet.th_needle is not None:
        if gobj.collides_box(knight, hornet.th_needle):
            knight_damaged_by(hornet.th_needle)


def update():
    gfw.world.update()
    for e in gfw.world.objects_at(gfw.layer.enemy):
        check_collide(e)
        d = abs(gobj.distance(knight.pos, e.pos))
        v = int(clamp(0, 50 - d, 50))
        e.sounds['crawler.wav'].set_volume(v)

    global hornet
    check_collide(hornet)
    check_collides_needle()
    if hornet.death_time >= 2.5:
        game_end_state.GAME_CLEAR = True
        gfw.change(game_end_state)

    global frame
    if frame.cracked_time >= 1.5:
        game_end_state.GAME_CLEAR = False
        gfw.change(game_end_state)

def draw():
    gfw.world.draw()
    #gobj.draw_collision_box()

def handle_event(e):
    global knight, frame
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
        elif e.key == SDLK_a:
            if knight.mask > 0:
                knight.mask = 5
                frame.refill_all()

    knight.handle_event(e)

def exit():
    global bgm, opening_sting
    bgm.stop()
    gfw.sound.unload_m('res/Sound/cave_wind_loop.mp3')
    gfw.sound.unload_w('res/Sound/S75 Opening Sting-08.wav')

    for e in gfw.world.objects_at(gfw.layer.enemy):
        for w in e.sounds:
            e.sounds[w].set_volume(0)

    gfw.world.clear()

def pause():
    pass
def resume():
    pass

if __name__ == '__main__':
    gfw.run_main()
