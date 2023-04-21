from assists.assists import *


class CreateUserPage:
    '''创建用户名界面'''

    def __init__(self, ai_game, title: str):
        # 背景和输入框
        self.popup = ChoosePopup(
            ai_game, title, 450, 280, (170, 190, 200), Ydeviation=90,
            yesMsg="Set", noMsg="Back")
        self.name = ""
        self.button = Button(
            ai_game, "", ai_game.screenRect.center, 320, 60,
            buttonColor=(255, 255, 255), textSize=35, textColor=(130, 130, 40))
        # 错误提示
        self.sameName = False  # 重名
        self.sameNameText = ShortText(
            ai_game, Calculate.add(ai_game.screenRect.center, (0, 40)),
            "The name has been registered.", 20, (170, 40, 40))
        self.emptyName = False  # 空名
        self.emptyNameText = ShortText(
            ai_game, Calculate.add(ai_game.screenRect.center, (0, 40)),
            "Empty name is not allowed.", 20, (170, 40, 40))

    def _check_name(self, ai_game, name: str = None):
        '''检测名字是否合乎要求，name不填默认为输入的名字，若是返回True，否则返回False'''
        if name == None:
            name = self.name
        if not name:
            self.sameName = False
            self.emptyName = True
            return False
        elif name in ai_game.userNames:
            self.sameName = True
            self.emptyName = False
            return False
        return True

    def _new_user_input(self, event: pygame.event.Event):
        '''输入用户名字，并更新屏幕'''
        self.name = Interactions.user_input(event, self.name, limit=14)
        self.button.msg = self.name

    def draw_new_user_popup(self, mouse_pos):
        '''画出创建新用户弹窗'''
        self.popup.draw_popup(mouse_pos)
        self.button.draw_button()
        if self.sameName:
            self.sameNameText.draw_text()
        if self.emptyName:
            self.emptyNameText.draw_text()

    def event_check(self, ai_game, event: pygame.event.Event):
        '''检测事件，在点击退出后返回用户输入值，点击是则返回用户输入，点击否则返回False，没有点击不返回值'''
        self._new_user_input(event)
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.popup.get_result(mouse_pos) == 1:
                if self._check_name(ai_game):
                    return self.name
            elif self.popup.get_result(mouse_pos) == -1:
                return False
        return None
