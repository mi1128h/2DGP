from pico2d import *

def handle_events():
    # running은 로컬이 아니라 글로벌이다. 밖에 있는 변수를 쓸 거야
    global running, dx, x, y  # global 잊지 말자!!
    # events는 로컬 변수. 함수가 종료되면 사라진다
    events = get_events()  # events 복수형으로 쓰자
    for e in events:
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
            elif e.key == SDLK_LEFT:
                dx -= 1
            elif e.key == SDLK_RIGHT:
                dx += 1
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                dx += 1
            elif e.key == SDLK_RIGHT:
                dx -= 1
        elif e.type == SDL_MOUSEMOTION:
            hide_cursor()
            x, y = e.x, get_canvas_height() - e.y - 1   # 정확하게는 1을 빼줘야해

open_canvas()   # 800, 600 디폴트

gra=load_image('../res/grass.png')
cha=load_image('../res/character.png')

x, y = get_canvas_width() // 2, 85  # 연관이 있다면 묶어서. 나눠도 되고
dx = 0
running = True

while running:     # 게임 루프
    # 렌더링 draw
    clear_canvas()
    gra.draw(400, 30)
    cha.draw(x, y)
    update_canvas()

    # 로직 update
    handle_events() # 동작의 추상화

    x += dx * 5

#    x += 2
#    if x >= get_canvas_width():
#        break

    delay(0.01)

close_canvas()

# 프로그램을 쪼갠다 -- 모듈화
    # 첫번째 모듈화 - 함수로 만든다