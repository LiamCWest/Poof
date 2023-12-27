import pygame
from logic.song import songPlayer
from logic.song.timingPoints import TimeSignature, TimingPoint
import time

pygame.init()

songPlayer.load(r"D:\Files\Python Projects\Poof\Poof\Song.MP3", [TimingPoint(2.108, 170, TimeSignature(4, 4))])

songPlayer.play()
songPlayer.seek(65)

time.sleep(1000000)