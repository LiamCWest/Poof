from graphics.animation import *
a1 = AnimEvent(-1, 2, lambda x : print("a1:", x))
anim = Animation([a1], 0)
anim.updateTime(0)
anim.updateTime(0)
anim.updateTime(3)