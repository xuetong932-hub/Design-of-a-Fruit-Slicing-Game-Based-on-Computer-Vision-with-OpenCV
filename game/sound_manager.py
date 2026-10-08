import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.slice = pygame.mixer.Sound("assets/sounds/slice.wav")
        self.combo2 = pygame.mixer.Sound("assets/sounds/combo2.wav")
        self.combo3 = pygame.mixer.Sound("assets/sounds/combo3.wav")
        self.bomb = pygame.mixer.Sound("assets/sounds/bomb.wav")
        self.game_over = pygame.mixer.Sound("assets/sounds/game_over.wav")

    def play_slice(self):
        self.slice.play()

    def play_combo(self, count):
        if count == 2:
            self.combo2.play()
        elif count >= 3:
            self.combo3.play()

    def play_bomb(self):
        self.bomb.play()

    def play_game_over(self):
        self.game_over.play()
