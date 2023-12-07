import pygame
from .repickle import repickle
from random import randint, choice


class Alien:
    """外星人！"""

    def __init__(self, ai_game):
        """初始化外星人并把它放在合适的位置"""
        # 初始速度和方向
        self.speedChaos = randint(
            100 - ai_game.settings.alienSpeedChaos*100, 100 + ai_game.settings.alienSpeedChaos*100)/100
        self.horizonalSpeed = ai_game.settings.alienHorizonalSpeed * self.speedChaos
        self.verticalSpeed = ai_game.settings.alienVerticalSpeed * self.speedChaos
        self.x, self.y = 0.0, 0.0  # 存储精确位置
        self.direction = choice([-1, 1])
        self.life: int
        self.killPoint: int
        self.rect: pygame.Rect
        self.imageFile: pygame.Surface

    def _check_edges(self, ai_game):
        """检查外星人是不是到边缘了，如果是，那么调转方向"""
        screenRect = ai_game.screen.get_rect()
        if self.rect.left <= 0 or self.rect.right >= screenRect.right:
            self.direction *= -1

    def update(self, ai_game):
        """外星人移动"""
        if not ai_game.skillA.working:  # 冰冻技能发动期间不再移动
            self._check_edges(ai_game)
            self.x += self.horizonalSpeed*self.direction
            self.y += self.verticalSpeed
            self.rect.x = self.x
            self.rect.y = self.y

    def generate_alien(self, ai_game):
        return choice([AlienA(ai_game)]*6 + [AlienB(ai_game)]*3 + [AlienC(ai_game)])

    def draw_alien(self, ai_game):
        ai_game.screen.blit(self.image, self.rect)

    # 重定义pickle的loads,dumps
    def __getstate__(self):
        return repickle.getstate(self, "image")

    def __setstate__(self, state):
        repickle.setstate(self, state, "image")


class AlienA(Alien):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.life = 1
        # 加载图片生成矩形
        self.image = pygame.image.load("images/aliens/alienA.png")
        self.rect = self.image.get_rect()
        self.killPoint = 50 * ai_game.settings.pointPlus


class AlienB(Alien):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.life = 2
        self.image = pygame.image.load("images/aliens/alienB.png")
        self.rect = self.image.get_rect()
        self.killPoint = 70 * ai_game.settings.pointPlus


class AlienC(Alien):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.life = 3
        self.image = pygame.image.load("images/aliens/alienC.png")
        self.rect = self.image.get_rect()
        self.killPoint = 100 * ai_game.settings.pointPlus
