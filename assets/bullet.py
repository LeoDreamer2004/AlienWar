import pygame


class Bullet:
    """管理飞船子弹"""

    def __init__(self, ai_game):
        self.color = ai_game.settings.bulletColor  # 读取颜色
        self.speed = ai_game.settings.bulletSpeed  # 读取速度
        if ai_game.stats.propsBTime:  # B技能发动时子弹变大
            self.rect = pygame.Rect(
                0, 0, 2*ai_game.settings.bulletWidth, 2*ai_game.settings.bulletHeight)
        else:
            self.rect = pygame.Rect(
                0, 0, ai_game.settings.bulletWidth, ai_game.settings.bulletHeight)  # 在0,0处创建矩形
        self.rect.midtop = ai_game.ship.rect.midtop  # 把子弹出发点移动到飞船正头部
        self.y = float(self.rect.y)  # 一样地，我们存一下子弹位置的浮点数

    def update(self):
        """子弹向上飞"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self, ai_game):
        """画出子弹"""
        pygame.draw.rect(ai_game.screen, self.color, self.rect)
