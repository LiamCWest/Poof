import pygame
import logic.song.songPlayer as songPlayer
import time

pygame.init()

songPlayer.test()

oldNextBeat = None
while True:    
    nextBeat = songPlayer.getNextBeat(0.5)
    if nextBeat != oldNextBeat:
        print(nextBeat, end="")
        if oldNextBeat is not None:
            print(" ", nextBeat - oldNextBeat)
    oldNextBeat = nextBeat
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()