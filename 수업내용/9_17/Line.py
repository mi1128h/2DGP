from math import cos, sin

### line
# dx,dy 로 각도와 속도를 결정할 수 있다.
#dx = 0.1
#dy = 0.05

# 각도와 속도를 다른 방법으로 정해보자
angle = 30
length = 0.1
dx = length * cos(30 * 3.141592 / 180)
dy = length * sin(30 * 3.141592 / 180)

x = 100
y = 200
dx = 0

#while True:
#    x += dx
#    y += dy

### jump
while True:
    x += dx
    y += dy
    if jump:
        dy = 100
    dy -= 1     # 중력이 잡아당긴다
    if y < 85:
        dy = 0