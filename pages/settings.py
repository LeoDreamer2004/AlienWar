from assists.assists import *


class SettingsPage:
    """设置页面"""

    def __init__(self, ai_game):
        """初始化内容"""
        # 文本
        self.BGMVolumeText = ShortText(
            ai_game, (140, 65), "BGM Volume:", size=30)
        self.FXVolumeText = ShortText(
            ai_game, (140, 165), "FX Volume:", size=30)
        self.frameText = ShortText(
            ai_game, (140, 265), "Speed (Frame):", size=30)
        self.settingTexts = [self.BGMVolumeText,
                             self.FXVolumeText, self.frameText]
        # 滑动条
        self.BGMVolumeSlidebar = Slidebar(
            ai_game, (300, 50), 0, 0.7,  "Silence", "Full", textSize=20, textSpace=50)
        self.BGMVolumeSlidebar.load(
            ai_game.userdata["gameSettings"]["BGMVolume"])
        self.FXVolumeSlidebar = Slidebar(
            ai_game, (300, 150), 0, 1,  "Silence", "Full", textSize=20, textSpace=50)
        self.FXVolumeSlidebar.load(
            ai_game.userdata["gameSettings"]["FXVolume"])
        self.frameSlidebar = Slidebar(
            ai_game, (300, 250), 120, 240, "Slow (120)", "Fast (240)", textSize=20, textSpace=50)
        self.frameSlidebar.load(ai_game.userdata["gameSettings"]["gameFrame"])
        self.settingSlidebars = [self.BGMVolumeSlidebar,
                                 self.FXVolumeSlidebar, self.frameSlidebar]
        # 按钮
        self.changeBGMButton = Button(
            ai_game, "Change BGMs", position=(800, 70), width=280, bold=False,
            buttonColor=(230, 160, 160), highlightColor=(200, 140, 140))
        self.setBackgroundButton = Button(
            ai_game, "Personalize the Background", position=(280, 400), width=450, bold=False,
            buttonColor=(230, 160, 160), highlightColor=(200, 140, 140))
        self.clearBackgroundButton = Button(
            ai_game, "Clear", position=(650, 400), bold=False, width=200,
            buttonColor=(230, 160, 160), highlightColor=(200, 140, 140))
        self.clearUserdataButton = Button(
            ai_game, "Clear Userdata", position=(200, 680), width=280, italic=True,
            buttonColor=(150, 40, 40), highlightColor=(200, 50, 50), )
        self.resetDefaultSettingsButton = Button(
            ai_game, "Default", position=(650, 680), width=180,
            buttonColor=(40, 40, 150), highlightColor=(50, 50, 200))
        self.settingsOKButton = Button(
            ai_game, "Finish", position=(850, 680), width=180,
            buttonColor=(40, 150, 40), highlightColor=(50, 200, 50))
        self.settingButtons = [self.changeBGMButton, self.setBackgroundButton, self.clearBackgroundButton,
                               self.clearUserdataButton, self.resetDefaultSettingsButton, self.settingsOKButton]
        # 弹窗
        self.clearUserdataPopup = ChoosePopup(
            ai_game, "Clear All the Userdata?", subtitleMsg="This operation cannot be undone.",
            titleSize=35, subtitleSize=23)
        self.clearBackgroundPopup = ChoosePopup(
            ai_game, "Use the default background?", width=600, titleSize=35)

    def draw_settings(self, ai_game, mouse_pos):
        """在屏幕上画出图形"""
        for text in self.settingTexts:
            text.draw_text()
        for button in self.settingButtons:
            button.draw_button(mouse_pos, bool(ai_game.subPage))
        for slidebar in self.settingSlidebars:
            slidebar.draw_slidebar(mouse_pos)
        if ai_game.subPage == "choose_clear_userdata":
            self.clearUserdataPopup.draw_popup(mouse_pos)
        elif ai_game.subPage == "choose_clear_background":
            self.clearBackgroundPopup.draw_popup(mouse_pos)
