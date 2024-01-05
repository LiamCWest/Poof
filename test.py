import pygame.mixer as mixer
import pygame
import time

pygame.init()
length = mixer.Sound("Song.MP3").get_length()
mixer.music.load(filename="Song.MP3")
mixer.music.play(start=length)
mixer.music.pause()

while True:
    time.sleep(0.1)
    print(mixer.music.get_pos() / 1000 + 60)