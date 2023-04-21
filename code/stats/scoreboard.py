import pygame
import json


class LeftShip:
    '''剩下的船只'''

    def __init__(self):
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()
        self.width = self.rect.width

    def draw_ship(self, ai_game):
        '''画船'''
        ai_game.screen.blit(self.image, self.rect)
        

class Scoreboard:
    '''计分板，烂完了懒得重写了'''

    def __init__(self, ai_game):
        '''初始化显示得分涉及的属性'''
        self.screenRect: pygame.Rect = ai_game.screen.get_rect()
        # 显示得分信息时使用的字体设置
        self.textColor = (200, 0, 0)
        self.font = pygame.font.SysFont("Comic Sans MS", 25, bold=True)
        # 准备文件
        self.userdata = ai_game.userdata

    def prep_score(self, ai_game):
        '''渲染当前分'''
        scoreStr = "Score: " + str(int(ai_game.stats.score))
        self.scoreImage = self.font.render(scoreStr, True, self.textColor)
        self.scoreRect = self.scoreImage.get_rect()
        self.scoreRect.right = self.screenRect.right - 20
        self.scoreRect.top = 20

    def prep_high_score(self, ai_game):
        '''渲染最高分'''
        if ai_game.stats.breakRecord:
            highScoreStr = "New Best! Go ahead!"
        else:
            highScoreStr = "Best: " + str(self.userdata["highScore"])
        self.highScoreImage = self.font.render(
            highScoreStr, True, self.textColor)
        self.highScoreRect = self.highScoreImage.get_rect()
        self.highScoreRect.centerx = self.screenRect.centerx
        self.highScoreRect.top = 20

    def prep_level(self, ai_game):
        '''渲染分数'''
        levelStr = "Level: " + str(ai_game.stats.level)
        self.levelImage = self.font.render(levelStr, True, self.textColor)
        self.levelRect = self.levelImage.get_rect()
        self.levelRect.right = self.scoreRect.right
        self.levelRect.top = self.scoreRect.bottom

    def update_high_score(self, ai_game):
        '''更新最高分，顺便重新渲染最高分'''
        if ai_game.stats.score > self.userdata["highScore"]:
            if not ai_game.stats.breakRecord:  # 播放破纪录音效
                congratulate = pygame.mixer.Sound("sounds/FX/break_record.ogg")
                congratulate.set_volume(ai_game.FXVolume)
                congratulate.play()
            ai_game.stats.breakRecord = True
            self.userdata["highScore"] = int(ai_game.stats.score)
            ai_game._save_personal_userdata()
            self.prep_high_score(ai_game)

    def prep_left_ship(self, ai_game):
        '''准备渲染剩余的船只'''
        self.ships = []
        for shipNumber in range(ai_game.stats.shipLeft):
            ship = LeftShip()
            ship.rect.left = 20 + shipNumber*ship.width
            ship.rect.top = 20
            self.ships.append(ship)

    def show_score(self, ai_game):
        '''显示到屏幕上'''
        self.prep_score(ai_game)
        self.prep_high_score(ai_game)
        self.prep_level(ai_game)
        self.prep_left_ship(ai_game)
        ai_game.screen.blit(self.scoreImage, self.scoreRect)
        ai_game.screen.blit(self.highScoreImage, self.highScoreRect)
        ai_game.screen.blit(self.levelImage, self.levelRect)
        for ship in self.ships:
            ship.draw_ship(ai_game)
