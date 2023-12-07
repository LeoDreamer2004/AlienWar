from assists.assists import Button, ShortText, Calculate, ChoosePopup


class GamePausePage:
    """游戏暂停页面"""

    def __init__(self, ai_game):
        # 背景
        self.gamePulseBackground = Button(
            ai_game, position=ai_game.screenRect.center, width=600, height=400,
            buttonColor=(90, 100, 110),  edgeWidth=10)
        # 标题
        self.gamePulseText = ShortText(
            ai_game, Calculate.add(ai_game.screenRect.center, (0, -145)),
            "Game Paused", 65, (180, 170, 140), bold=True)
        # 按钮
        self.continueButton = Button(
            ai_game, "Continue", Calculate.add(
                ai_game.screenRect.center, (0, -60)),
            buttonColor=(30, 128, 30), highlightColor=(50, 200, 50))
        self.gameRestartButton = Button(
            ai_game, "Restart", Calculate.add(
                ai_game.screenRect.center, (0, 10)),
            buttonColor=(128, 30, 30), highlightColor=(200, 50, 50))
        self.gameSettingButton = Button(
            ai_game, "Settings", Calculate.add(
                ai_game.screenRect.center, (0, 80)),
            buttonColor=(128, 128, 128), highlightColor=(200, 200, 200))
        self.goBackMenuButton = Button(
            ai_game, "Menu", Calculate.add(
                ai_game.screenRect.center, (0, 150)),
            buttonColor=(30, 30, 128), highlightColor=(50, 50, 200))
        self.buttons = [self.continueButton, self.gameRestartButton,
                        self.gameSettingButton, self.goBackMenuButton]
        # 弹窗
        self.restartPopup = ChoosePopup(ai_game, "Restart?", noMsg="Back")
        self.goMenuPopup = ChoosePopup(
            ai_game, "Go Back to the Menu?",
            subtitleMsg="Your game will be saved.",
            titleSize=37, noMsg="Back")

    def draw_game_pause(self, mouse_pos):
        """画出游戏暂停窗口"""
        self.gamePulseBackground.draw_button()
        for button in self.buttons:
            button.draw_button(mouse_pos)
        self.gamePulseText.draw_text()
