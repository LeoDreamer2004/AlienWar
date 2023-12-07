from assists.assists import *
from time import sleep


class LoadingPage:
    """进入游戏的加载页面"""

    def __init__(self, ai_game, statesNum: int, processText: str = ""):
        """statesNum表示总共的阶段数"""
        self.statesNum = statesNum
        self.states = 0
        self.centerx, self.centery = ai_game.screenRect.center
        self.loadingText = ShortText(
            ai_game, (self.centerx, self.centery - 50),
            "Alien Invasion", 60, (200, 40, 40), bold=True)
        # 进度条
        self.barLength = 590
        self.loadBar = pygame.Rect(
            self.centerx - self.barLength//2, self.centery + 205, 0, 30)
        self.loadBarEdge = pygame.Rect(
            self.centerx - 300, self.centery + 200, 600, 40)
        self.numberText = ShortText(
            ai_game, (self.centerx, self.centery + 220), f"{self.states}/{self.statesNum}", 30, (20, 20, 20))
        self.processText = ShortText(
            ai_game, (self.centerx, self.centery + 180), processText, 27, (20, 20, 20))

    def draw_loading(self, ai_game, sleepTime: float = 0):
        """画出加载页面并展示，sleepTime表示加载完成暂停时间"""
        ai_game.screen.fill((255, 255, 255), ai_game.screenRect)
        pygame.draw.rect(ai_game.screen, (20, 20, 20),
                         self.loadBarEdge, width=2)
        pygame.draw.rect(ai_game.screen, (200, 40, 40), self.loadBar)
        self.loadingText.draw_text()
        self.numberText.draw_text()
        self.processText.draw_text()
        pygame.display.flip()
        sleep(sleepTime)

    def update_loading(self, ai_game, processText: str = None, sleepTime: float = 0):
        """更新加载进度，processText表示加载进度的文本标识，不填表示不修改"""
        self.states += 1
        self.numberText.change_msg(f"{self.states}/{self.statesNum}")
        self.loadBar.width = self.barLength * self.states // self.statesNum
        if processText != None:
            self.processText.change_msg(processText)
        self.draw_loading(ai_game, sleepTime)

    def finish_loading(self, ai_game):
        """加载完成的淡出动画效果"""
        animationTime = 0.8
        time = ai_game.gameFrame * animationTime
        self.clock = pygame.time.Clock()
        while time > 0:
            self.clock.tick(ai_game.gameFrame)
            time -= 1
            color = int(time / ai_game.gameFrame * 255)
            if color < 0:
                color = 0
            ai_game.screen.fill((color, color, color), ai_game.screenRect)
            pygame.display.flip()
