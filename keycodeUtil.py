from pynput import keyboard, mouse

def toKeyStr(key):
    global kbListener
    return str(kbListener.canonical(key))

def onKeyPress(key):
    print(toKeyStr(key))

kbListener = keyboard.Listener(on_press=onKeyPress)
kbListener.start()

while True:
    continue