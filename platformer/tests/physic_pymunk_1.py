import pymunk

space = pymunk.Space()
space.gravity = 0, -1000

body = pymunk.Body(1, 1666)
body.position = 50, 1000

poly = pymunk.Poly.create_box(body)
space.add(body, poly)

while True:
    space.step(0.02)