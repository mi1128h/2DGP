from pico2d import *
import helper
RES_DIR = '../res'

open_canvas()

class Grass:
    def __init__(self):
        self.image = load_image(RES_DIR + '/grass.png')
    def draw(self):
        self.image.draw(400, 30)
    def update(self):
        pass

class Boy:
    def __init__(self):
        self.x, self.y = 400, 85
        self.dx, self.dy = 0, 0
        self.fidx = 0
        self.image = load_image(RES_DIR + '/run_animation.png')
        self.speed = 1
    def draw(self):
        self.image.clip_draw(self.fidx * 100, 0, 100, 100, self.x, self.y)
    def update(self, tList):
        if len(tList) > 0:  # 목적지가 있다면
            dt = helper.delta((self.x, self.y),tList[0],self.speed)
            (self.x, self.y), done = helper.move_toward((self.x, self.y), dt, tList[0])
            if done == True:
                del(tList[0])
                self.speed = 1

    #    self.x += self.dx
    #    self.y += self.dy
        self.fidx = (self.fidx + 1) % 8

def handle_events():
    global running, targets, tList, boy
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            running = False
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            running = False
        elif e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                if len(tList) > 0:
                    # 같은 곳을 연속으로 클릭했을 때 중복으로 들어가지 않도록
                    if tList[-1] != (e.x, get_canvas_height() - e.y - 1):
                        tList.append((e.x, get_canvas_height() - e.y - 1))
                        print((e.x, get_canvas_height() - e.y - 1))
                else:
                    tList.append((e.x, get_canvas_height() - e.y - 1))
                    print((e.x, get_canvas_height() - e.y - 1))
            elif e.button == SDL_BUTTON_RIGHT:
                if len(tList) > 0:
                    boy.speed += 1

grass = Grass()
boy = Boy()
tList = []

running = True
while running:
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()

    handle_events()

    boy.update(tList)
    grass.update()

    if boy.x > get_canvas_width():
        running = False
    delay(0.01)

close_canvas()