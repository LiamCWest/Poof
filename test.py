import keyboard

def f(ev):
    print("pressed")
    print(ev.event_type == keyboard.KEY_UP)
    
keyboard.hook_key("w", f)
while True:
    continue