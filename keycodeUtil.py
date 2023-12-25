from pynput import keyboard, mouse

def onKeyPress(key):
    print(kbListener.canonical(key))

kbListener = keyboard.Listener(on_press=onKeyPress)
kbListener.start()

while True:
    continue