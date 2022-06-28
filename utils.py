import pygame

def play_sound(sound):
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()