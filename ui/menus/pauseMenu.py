from ui.button import Button
from ui.text import Text
import graphics.gui as gui

def show():
    pass

def hide():
    pass

def draw():
    objects.sort(key = lambda x : x.z)
    for object in objects:
        object.draw(gui.screen)
    for text in texts:
        text.draw()
        
def update():
    for object in objects:
        object.update()      

title = "Pause"
objects = [Button("Resume", 200, 262, 200, 100, (0, 255, 0), (255, 0, 0), lambda: gui.setScreen("game"), particles=True),
           Button("Main Menu", 200, 375, 200, 100, (0, 255, 0), (255, 0, 0), lambda: gui.setScreen("main")),
           Button("Settings", 200, 487, 200, 100, (0, 255, 0), (255, 0 ,0), lambda: gui.setScreen("settings")),
           Button("Quit", 200, 600, 200, 100, (0, 255, 0), (255, 0, 0), quit),]
texts = [Text(title, 400, 150, (255, 0, 0), 100)]