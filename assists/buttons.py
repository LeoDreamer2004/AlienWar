import pygame
from assists.calculate import Calculate


class Button:
    """各种按钮"""

    def __init__(self, ai_game, msg: str = "", position: tuple = (0, 0),
                 width: int = 300, height: int = 50,
                 buttonColor: tuple = (0, 0, 0), textSize: int = 30,
                 textFont: str = "Comic Sans MS", textColor: tuple = (255, 255, 255),
                 edgeColor: tuple | bool = None, edgeWidth: float = 2, highlightColor: tuple = None,
                 bold: bool = True, italic: bool = False):
        """在游戏中根据需要输出msg，如果不要边框edgeColor定义为False"""
        self.screen: pygame.Surface = ai_game.screen
        self.clickSound: pygame.mixer.Sound = ai_game.clickSound
        self.screenRect = self.screen.get_rect()
        # 按钮尺寸
        self.width, self.height = width, height
        # 按钮颜色
        self.buttonColor = self.originalButtonColor = buttonColor
        self.textColor = textColor
        if edgeColor == None:  # 默认边框颜色算法
            self.edgeColor = Calculate.mul(self.buttonColor, 0.6)
        else:
            self.edgeColor = edgeColor
        self.edgeWidth = edgeWidth
        self.highlightColor = highlightColor
        # 文本特征
        self.textFont = textFont
        self.font = pygame.font.SysFont(
            self.textFont, textSize, bold=bold, italic=italic)  # 字体字号
        # 创建按钮矩形
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = position
        self.msg = msg
        self.forceHighlight = False # 是否强制高亮

    def _prep_msg(self):
        """将msg渲染为图像"""
        self.msgImage = self.font.render(
            self.msg, True, self.textColor, self.color)  # True表示抗锯齿
        self.msgImageRect = self.msgImage.get_rect()
        self.msgImageRect.center = Calculate.add(self.rect.center, (0, -2))

    def draw_button(self, mouse_pos = None, againstHighlight: bool = False):
        """在屏幕上画出按钮，againstHighlight禁止高亮"""
        # 先绘制按钮，再绘制文本
        if (mouse_pos and not againstHighlight and self.highlightColor
                and self.rect.collidepoint(mouse_pos)) or self.forceHighlight:
            self.color = self.highlightColor
        else:
            self.color = self.buttonColor
        self._prep_msg()
        self.screen.fill(self.color, self.rect)
        if self.edgeColor:
            pygame.draw.rect(self.screen, self.edgeColor,
                             self.rect, width=self.edgeWidth)
        self.screen.blit(self.msgImage, self.msgImageRect)

    def clicked(self, mouse_pos, playSound: bool = True):
        """是否被点击到了，是否播放声音"""
        if self.rect.collidepoint(mouse_pos):
            if playSound:
                self.clickSound.play()
            return True
        return False
