import pygame
from .text import ShortText
from .calculate import Calculate
from .buttons import Button


class Slidebar:
    """滑动条"""

    def __init__(self, ai_game, position: tuple, startNum: float, endNum: float,
                 startMsg: str = None, endMsg: str = None, height: int = 30, width: int = 300,
                 barColor: tuple = (200, 200, 200), blockColor: tuple = (128, 0, 0),
                 highlightColor: tuple = (200, 0, 0), textColor: tuple = (255, 255, 255),
                 textSize: int = 30, textSpace: int = 60, textStyle: str = "Comic Sans MS"):
        # 开始和结束两端点
        self.startNum = startNum
        self.endNum = endNum
        self.startX = position[0]
        self.endX = position[0] + width
        if startMsg is None:
            self.startMsg = str(self.startNum)
        else:
            self.startMsg = startMsg
        if endMsg is None:
            self.endMsg = str(self.endNum)
        else:
            self.endMsg = endMsg
        self.startNumImage = ShortText(ai_game, Calculate.add(
            position, (0, textSpace)), self.startMsg, textSize, textColor, textStyle)
        self.endNumImage = ShortText(ai_game, Calculate.add(
            position, (width, textSpace)), self.endMsg, textSize, textColor, textStyle)
        # 实例创建
        self.screen: pygame.Surface = ai_game.screen
        self.barRect = pygame.Rect(position[0], position[1], width, height)
        self.block = Button(ai_game, position=(0, 0),
                            width=15, height=height*1.25, buttonColor=blockColor, edgeColor=False,
                            highlightColor=highlightColor)
        # 颜色存储
        self.originalBlockColor = blockColor
        self.highlightBlockColor = highlightColor
        self.barColor = barColor

        # 表示是否正在移动
        self.active = False

    def load(self, number):
        """根据数字加载滑块位置"""
        self.addX = (self.endX - self.startX) * (number -
                                                 self.startNum) / (self.endNum - self.startNum)
        self.block.rect.center = Calculate.add(
            self.barRect.midleft, (self.addX, 0))

    def draw_slidebar(self, mouse_pos):
        """画出滑动条"""
        self.update(mouse_pos)
        self.screen.fill(self.barColor, self.barRect)
        if self.active:  # 活跃状态下强制高亮
            self.block.buttonColor = self.highlightBlockColor
        else:
            self.block.buttonColor = self.originalBlockColor
        self.block.draw_button(mouse_pos)
        self.startNumImage.draw_text()
        self.endNumImage.draw_text()

    def check_active(self, mouse_pos):
        """检测是否变为活跃状态"""
        if self.block.rect.collidepoint(mouse_pos):
            self.active = True

    def update(self, mouse_pos):
        """更新位置"""
        if self.active:
            if self.startX <= mouse_pos[0] <= self.endX:
                self.block.rect.centerx = mouse_pos[0]
            elif mouse_pos[0] < self.startX:
                self.block.rect.centerx = self.startX
            elif mouse_pos[0] > self.endX:
                self.block.rect.centerx = self.endX

    def read(self, ndigits: int = None):
        """读数"""
        self.ratio = (self.block.rect.centerx - self.startX) / \
            (self.endX-self.startX)
        self.number = self.startNum + \
            (self.endNum - self.startNum) * self.ratio
        if ndigits is None:
            return self.number
        else:
            return round(self.number, ndigits)
