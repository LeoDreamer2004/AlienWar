import pygame
from assists.assists import *


class IntroductionsPage:
    """介绍页面"""

    def __init__(self, ai_game):
        """初始化简要信息"""
        # 背景板
        self.page = 0
        self.backgroundPlate = Button(
            ai_game, position=ai_game.screenRect.center, width=970, height=690,
            buttonColor=(170, 170, 170), edgeWidth=5)
        # 按钮
        self.lastPageButton = Button(
            ai_game, "Last", (550, 680), 130, textSize=30,
            buttonColor=(140, 140, 20), highlightColor=(200, 200, 30))
        self.nextPageButton = Button(
            ai_game, "Next", (700, 680), 130, textSize=30,
            buttonColor=(140, 140, 20), highlightColor=(200, 200, 30))
        self.OKbutton = Button(
            ai_game, "OK", (870, 680), 170, textSize=30,
            buttonColor=(40, 150, 40), highlightColor=(50, 200, 50))
        self.introductionButtons = [
            self.lastPageButton, self.nextPageButton, self.OKbutton]

    def prep_texts(self, ai_game):
        """更新文本"""
        self.color = (150, 60, 20)
        self.texts = LongText(
            ai_game, "strings/introduction.txt", (50, 50), size=27, color=self.color).separate()
        self.pages = len(self.texts)
        self.pageText = ShortText(
            ai_game, (170, 680), size=30, color=(150, 30, 30),
            msg=f"Page {self.page + 1} / {self.pages}")

    def last_page(self):
        """翻到上一页"""
        self.page = (self.page - 1) % self.pages

    def next_page(self):
        """翻到下一页"""
        self.page = (self.page + 1) % self.pages

    def draw_introductions(self, ai_game, mouse_pos):
        """把介绍画出来"""
        self.prep_texts(ai_game)
        self.backgroundPlate.draw_button()
        self.pageText.draw_text()
        self.texts[self.page].draw_text()
        for button in self.introductionButtons:
            button.draw_button(mouse_pos)
