import turtle

turtle.speed(0)

for i in range(-3,3):
	turtle.penup()
	turtle.goto(-300,i*100)
	turtle.pendown()
	turtle.forward(500)
	
turtle.setheading(90)
for i in range(-3,3):
    turtle.penup()
    turtle.goto(i*100,-300)
    turtle.pendown()
    turtle.forward(500)

turtle.exitonclick()
