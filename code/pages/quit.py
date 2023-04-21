from assists.assists import *


class QuitPage:
    '''退出游戏页面'''

    def __init__(self, ai_game):
        if ai_game.gameActive:
            ai_game._pause_game_debug()
        pygame.mouse.set_visible(True)
        self.popup = ChoosePopup(
            ai_game, "Quit the game?", yesMsg="Exit", noMsg="Back")

    def draw_quit_page(self,mouse_pos):
        '''画出退出页面'''
        self.popup.draw_popup(mouse_pos)