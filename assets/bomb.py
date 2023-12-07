import pygame
from .repickle import repickle


class Bomb:
    """炸弹"""

    def __init__(self, ai_game):
        self.screenRect: pygame.Rect = ai_game.screenRect
        self.image = pygame.image.load("images/bombs/bomb.png")
        self.bombedImage = pygame.image.load("images/bombs/bombed.png")
        self.imageRect = self.image.get_rect()
        self.bombedImageRect = self.bombedImage.get_rect()
        # 物品的位置
        self.bombed = False  # 是否爆炸

    def draw_bomb(self, ai_game):
        """画出炸弹"""
        if self.bombed:
            ai_game.screen.blit(self.bombedImage, self.bombedImageRect)
        else:
            ai_game.screen.blit(self.image, self.imageRect)

    # 重定义pickle的loads,dumps
    def __getstate__(self):
        return repickle.getstate(self, "image", "bombedImage")

    def __setstate__(self, state):
        repickle.setstate(self, state, "image", "bombedImage")
