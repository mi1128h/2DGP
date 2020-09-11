import turtle
turtle.speed(0)

def move(x,y):
    turtle.penup()
    turtle.goto(x,y)
    turtle.pendown()

def d_giyeok(size):
    turtle.setheading(0)
    turtle.forward(size)
    turtle.setheading(225)
    turtle.forward(size)

def d_i(size):
    turtle.setheading(270)
    turtle.forward(size)

def d_mieum(size):
    turtle.setheading(270)
    turtle.forward(size*2/3)
    turtle.setheading(0)
    turtle.forward(size)
    turtle.setheading(90)
    turtle.forward(size*2/3)
    turtle.setheading(180)
    turtle.forward(size)

def d_hieut(size):
    turtle.setheading(270)
    turtle.forward(size/5)
    turtle.setheading(0)
    turtle.penup()
    turtle.backward(size/2)
    turtle.pendown()
    turtle.forward(size)
    turtle.penup()
    turtle.backward(size/2)
    turtle.pendown()
    turtle.setheading(180)
    turtle.circle(size/3)

def d_yeo(size):
    turtle.setheading(0)
    turtle.forward(size/3)
    turtle.penup()
    turtle.backward(size/3)
    turtle.setheading(270)
    turtle.forward(size/3)
    turtle.setheading(0)
    turtle.pendown()
    turtle.forward(size/3)
    turtle.setheading(270)
    turtle.penup()
    turtle.backward(size*2/3)
    turtle.pendown()
    turtle.forward(size)

def d_nieun(size):
    turtle.setheading(270)
    turtle.forward(size/3)
    turtle.setheading(0)
    turtle.forward(size)


# 김
move(-250,150)
d_giyeok(75)

move(-150,160)
d_i(75)

move(-220,70)
d_mieum(75)

#미
move(-100,130)
d_mieum(75)

move(0,145)
d_i(90)

#현
move(70,160)
d_hieut(75)

move(110,135)
d_yeo(75)

move(70,70)
d_nieun(75)


turtle.exitonclick()
