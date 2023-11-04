from assists.assists import *


class LoseGamePage:
    """输掉游戏界面"""

    def __init__(self, ai_game):
        # 弹窗和音乐
        score = int(ai_game.stats.score)
        if ai_game.stats.breakRecord:
            ai_game.breakRecordSound.play(loops=-1, fade_ms=5000)
            self.popup = ChoosePopup(
                ai_game, "Congratulations! New record!", 600,
                subtitleMsg=f"New Best: {score}", titleSize=37,
                yesMsg="Restart", noMsg="Menu", colorReverse=True)
        else:
            ai_game.loseGameSound.play(loops=-1, fade_ms=5000)
            self.popup = ChoosePopup(
                ai_game, "You lose!", subtitleMsg=f"Score: {score}",
                yesMsg="Restart", noMsg="Menu", colorReverse=True)

    def draw_lose_game(self, mouse_pos):
        """把页面画在屏幕上"""
        self.popup.draw_popup(mouse_pos)
