import pygame
from assists.buttons import Button
from assists.calculate import Calculate
from assists.text import ShortText


class ChoosePopup:
    """二选一弹窗"""

    def __init__(self, ai_game, titleMsg: str, width: int = 500, height: int = 180,
                 backgroundColor: tuple = (170, 170, 170), titleColor: tuple = (150, 20, 20),
                 titleSize: int = 40,  subtitleMsg: str = None, subtitleSize: int = 27,
                 yesMsg: str = "Yes", noMsg: str = "No", colorReverse: bool = False,
                 buttonWidth: int = 170, buttonDeviation: int = 100, Ydeviation: int = 40,
                 yesColor: tuple = (128, 30, 30), yesHighlightColor: tuple = (200, 40, 40),
                 noColor: tuple = (30, 128, 30), noHighlightColor: tuple = (40, 200, 40)):
        """colorReverse是否按钮颜色互换（默认是红否绿），buttonDeviation按钮偏离中心距离"""
        self.game = ai_game
        self.screenRect: pygame.Rect = ai_game.screenRect
        self.subtitleMsg = subtitleMsg
        if self.subtitleMsg:  # 副标题存在时需要调整数据
            height += 20
            Ydeviation += 10
            self.subtitle = ShortText(
                ai_game,  Calculate.add(
                    self.screenRect.center, (0, -Ydeviation//4)),
                subtitleMsg, subtitleSize, titleColor, bold=True)
        # 背景板按钮和文本
        self.backgroundButton = Button(
            ai_game, position=self.screenRect.center, width=width, height=height,
            buttonColor=backgroundColor, edgeWidth=5)
        self.title = ShortText(
            ai_game, Calculate.add(self.screenRect.center, (0, -Ydeviation)),
            titleMsg, titleSize, titleColor, bold=True)
        if colorReverse:  # yes和no的颜色颠倒
            yesColor, noColor = noColor, yesColor
            yesHighlightColor, noHighlightColor = noHighlightColor, yesHighlightColor
        # Yes和No按钮
        self.yesButton = Button(
            ai_game, yesMsg, Calculate.add(
                self.screenRect.center, (-buttonDeviation, Ydeviation)),
            width=buttonWidth, buttonColor=yesColor, highlightColor=yesHighlightColor)
        self.noButton = Button(
            ai_game, noMsg, Calculate.add(
                self.screenRect.center, (buttonDeviation, Ydeviation)),
            width=buttonWidth, buttonColor=noColor, highlightColor=noHighlightColor)

    def draw_popup(self, mouse_pos):
        """画出弹窗"""
        self.backgroundButton.draw_button()
        self.title.draw_text()
        if self.subtitleMsg:
            self.subtitle.draw_text()
        self.yesButton.draw_button(mouse_pos)
        self.noButton.draw_button(mouse_pos)

    def get_result(self, mouse_pos):
        """获得结果，yes返回1，no返回-1，无结果返回0"""
        if self.yesButton.clicked(mouse_pos):
            return 1
        elif self.noButton.clicked(mouse_pos):
            return -1
        else:
            return 0
