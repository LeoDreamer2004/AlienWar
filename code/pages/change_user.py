from assists.assists import *


class changeUserPage:
    '''更换用户的界面'''

    def __init__(self, ai_game):
        # 标题文本
        self.changeUserText = ShortText(
            ai_game, Calculate.add(ai_game.screenRect.center, (0, -210)), "Who are you?", size=50,
            color=(128, 40, 40), bold=True)
        # 按钮
        self.background = Button(
            ai_game, position=ai_game.screenRect.center, width=400, height=540,
            buttonColor=(170, 190, 200), edgeWidth=5)
        self.deleteButton = Button(
            ai_game, "Delete", (415, 570), 175, 44, textSize=25,
            buttonColor=(150, 40, 40), highlightColor=(200, 50, 50))
        self.addButton = Button(
            ai_game, "Add", (609, 570), 175, 44, textSize=25,
            buttonColor=(40, 40, 150), highlightColor=(50, 50, 200))
        self.renameButton = Button(
            ai_game, "Rename", (415, 620), 175, 44, textSize=25,
            buttonColor=(150, 150, 40), highlightColor=(200, 200, 50))
        self.OKButton = Button(
            ai_game, "OK", (609, 620), 175, 44, textSize=25,
            buttonColor=(40, 150, 40), highlightColor=(50, 200, 50))
        # 用户按钮和所有用户名称
        self.maxUserNum = ai_game.settings.maxUserNum
        self.userButtons: list[Button] = []
        self.userNames: list[str] = ai_game.userNames
        width, height = self.background.width - self.background.edgeWidth*2, 50
        for index, user in enumerate(self.userNames):
            position = Calculate.add(
                ai_game.screenRect.center, (0, -130 + index*height))
            button = Button(
                ai_game, user, position, width, textSize=25, textColor=(130, 130, 40),
                buttonColor=(170, 190, 200), highlightColor=(150, 170, 180), edgeColor=False)
            self.userButtons.append(button)
        position = Calculate.add(
            ai_game.screenRect.center, (0, -130 + (index+1)*height))
        self.buttons = [self.deleteButton, self.addButton,
                        self.renameButton, self.OKButton] + self.userButtons
        self.update_highlight(ai_game.player)
        self._update_delete_user_popup(ai_game)

    def draw_change_user_page(self, mouse_pos):
        '''画出更换玩家的页面'''
        self.background.draw_button()
        if len(self.userNames) > 1:
            self.deleteButton.draw_button(mouse_pos)
        if len(self.userNames) < self.maxUserNum:
            self.addButton.draw_button(mouse_pos)
        self.renameButton.draw_button(mouse_pos)
        self.OKButton.draw_button(mouse_pos)
        for button in self.userButtons:
            button.draw_button(mouse_pos)
        self.changeUserText.draw_text()

    def update_highlight(self, name):
        '''高亮按钮更新'''
        self.chosenUser = name
        for button in self.userButtons:
            if button.msg == name:
                button.forceHighlight = True
            else:
                button.forceHighlight = False

    def next_player(self, name):
        '''（因为删除玩家）找到下一名玩家的名字，若仅剩此一人返回None'''
        userNum = len(self.userNames)
        if userNum == 1:
            return None
        index = (self.userNames.index(name) + 1) % userNum
        return self.userNames[index]

    def _update_delete_user_popup(self, ai_game):
        '''更新删除用户的弹窗'''
        self.deleteUserPopup = ChoosePopup(
            ai_game, "Delete User?", subtitleMsg=f"Username: {ai_game.player}",
            yesMsg="Delete", noMsg="Back", backgroundColor=self.background.buttonColor)

    def draw_delete_user_popup(self, mouse_pos):
        '''画出删除用户的弹窗'''
        self.deleteUserPopup.draw_popup(mouse_pos)
