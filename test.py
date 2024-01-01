from graphics.animation import *

a = AnimEvent(0, 1, lambda x:print(x), "a1")
anim = Animation([a], 0)
anim.updateTime(0.5)
#anim.removeEvent(a)
anim.updateTime(0.6)