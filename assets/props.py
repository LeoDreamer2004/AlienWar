import pygame
from assets.repickle import repickle


class Properties:
    """游戏道具"""

    def __init__(self, ai_game):
        """初始化道具"""
        self.x, self.y = 0.0, 0.0
        self.speed = ai_game.settings.propSpeed
        self.rotateAngle = 0
        self.originalImage: pygame.Surface
        self.allSurface = ["image", "originalImage"]

    def update(self):
        """更新道具"""
        self.rotateAngle += 0.05  # 旋转动画效果
        self.image = pygame.transform.rotate(
            self.originalImage, self.rotateAngle)
        self.y += self.speed
        self.rect = self.image.get_rect(center=(self.x, self.y))  # 保中心不变的旋转

    def draw_prop(self, ai_game):
        """在屏幕上画出道具"""
        ai_game.screen.blit(self.image, self.rect)
    
    # 重定义pickle的loads,dumps
    def __getstate__(self):
        return repickle.getstate(self, "image", "originalImage")

    def __setstate__(self, state):
        repickle.setstate(self, state, "image", "originalImage")


class ExpandAttackRange(Properties):
    """扩大攻击范围"""

    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.originalImage = pygame.image.load("images/props/prop1.png")
        self.rect = self.originalImage.get_rect()
        self.image = self.originalImage


class StrengthenBullet(Properties):
    """增强子弹攻击力"""

    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.originalImage = pygame.image.load("images/props/prop2.png")
        self.rect = self.originalImage.get_rect()
        self.image = self.originalImage


class DoubleScore(Properties):
    """双倍得分"""

    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.originalImage = pygame.image.load("images/props/prop3.png")
        self.rect = self.originalImage.get_rect()
        self.image = self.originalImage
