from assists.assists import *
from pages.change_user import changeUserPage
from pages.new_user import CreateUserPage


class Menu:
    """主菜单"""

    def __init__(self, ai_game):
        # 选择按钮
        self.continueGameButton = Button(ai_game, "Continue", position=Calculate.add(
            ai_game.screenRect.center, (0, -160)),
            buttonColor=(20, 128, 20), highlightColor=(50, 200, 50))
        self.newGameButton = Button(ai_game, "New Game", position=Calculate.add(
            ai_game.screenRect.center, (0, -80)),
            buttonColor=(128, 20, 20), highlightColor=(200, 50, 50))
        self.introButton = Button(ai_game, "Introdutions", position=Calculate.add(
            ai_game.screenRect.center, (0, 0)),
            buttonColor=(20, 20, 128), highlightColor=(50, 50, 200))
        self.settingsButton = Button(ai_game, "Settings", position=Calculate.add(
            ai_game.screenRect.center, (0, 80)),
            buttonColor=(100, 100, 100), highlightColor=(180, 180, 180))
        self.changeUserButton = Button(ai_game, "Change User", position=Calculate.add(
            ai_game.screenRect.center, (0, 160)),
            buttonColor=(128, 20, 128), highlightColor=(200, 50, 200))
        self.buttons = [self.continueGameButton, self.newGameButton,
                        self.introButton, self.settingsButton, self.changeUserButton]
        # 退出按钮
        self.quitImage = pygame.image.load("images/menu/quit.png")
        self.quitSelectedImage = pygame.image.load(
            "images/menu/quitSelected.png")
        self.quitImageRect = self.quitImage.get_rect()
        self.quitImageRect.center = (800, 650)
        self.quitFont = ShortText(
            ai_game, (860, 650), "Quit", 25, (160, 30, 30), bold=True)
        # 弹窗
        self.noSavePopup = ChoosePopup(
            ai_game, "No save to continue.", yesMsg="New Game", noMsg="Go Back",
            width=570, buttonWidth=230, buttonDeviation=130)

    def draw_menu(self, ai_game, mouse_pos):
        """画出菜单"""
        for button in self.buttons:
            button.draw_button(mouse_pos, bool(ai_game.subPage))
        if self.quitImageRect.collidepoint(mouse_pos) and not ai_game.subPage:
            ai_game.screen.blit(self.quitSelectedImage, self.quitImageRect)
            self.quitFont.draw_text()
        else:
            ai_game.screen.blit(self.quitImage, self.quitImageRect)
        if ai_game.subPage == "no_save":
            self.noSavePopup.draw_popup(mouse_pos)
        elif ai_game.subPage == "change_user":
            page1: changeUserPage = ai_game.changeUserPage
            page1.draw_change_user_page(mouse_pos)
        elif ai_game.subPage == "choose_delete_user":
            page2: changeUserPage = ai_game.changeUserPage
            page2.draw_delete_user_popup(mouse_pos)
        elif ai_game.subPage == "new_user":
            page3: CreateUserPage = ai_game.newUserPage
            page3.draw_new_user_popup(mouse_pos)
        elif ai_game.subPage == "rename_user":
            page4: CreateUserPage = ai_game.renameUserPage
            page4.draw_new_user_popup(mouse_pos)


class NewGamePage:
    """选择新游戏的页面"""

    def __init__(self, ai_game):
        # 按钮
        self.easyButton = Button(ai_game, "Easy", position=Calculate.add(
            ai_game.screenRect.center, (0, -135)),
            buttonColor=(20, 128, 20), highlightColor=(50, 200, 50))
        self.mediumButton = Button(ai_game, "Medium", position=Calculate.add(
            ai_game.screenRect.center, (0, -45)),
            buttonColor=(128, 128, 20), highlightColor=(200, 200, 50))
        self.hardButton = Button(ai_game, "Hard", position=Calculate.add(
            ai_game.screenRect.center, (0, 45)),
            buttonColor=(128, 20, 20), highlightColor=(200, 50, 50))
        self.backMenuButton = Button(ai_game, "Back", position=Calculate.add(
            ai_game.screenRect.center, (0, 135)),
            buttonColor=(20, 20, 128), highlightColor=(50, 50, 200))
        self.buttons = [
            self.easyButton, self.mediumButton, self.hardButton, self.backMenuButton]
        # 弹窗
        self.chooseNewGamePopup = ChoosePopup(
            ai_game, "New Game?", subtitleMsg="Your last save will be deleted.")

    def draw_new_game_page(self, ai_game, mouse_pos):
        """画出新游戏页面"""
        for button in self.buttons:
            button.draw_button(mouse_pos, bool(ai_game.subPage))
        if ai_game.subPage == "choose_new_game":
            self.chooseNewGamePopup.draw_popup(mouse_pos)
