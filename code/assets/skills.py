import pygame
from assets.bomb import Bomb
from assets.repickle import repickle
from math import radians


class Skills:
    '''飞船技能'''

    def __init__(self, ai_game):
        '''初始化和标记一些技能信息'''
        self.completeImage: pygame.Surface
        self.coolingDownImage: pygame.Surface
        self.available = False  # 是否可用
        self.working = False  # 是否正在生效
        self.CD: int  # 总冷却时间
        self.coolTime: int  # 已冷却时间
        self.time: int  # 总生效时间
        self.workTime = 0  # 已生效时间
        self.soundFile: str

    def _update_CD(self):
        '''更新技能CD'''
        if self.coolTime < self.CD:
            self.coolTime += 1
        else:
            self.available = True

    def draw_skill(self, ai_game):
        '''将技能提示画在屏幕上'''
        startAngle = (self.coolTime/self.CD)*360
        if self.available:
            ai_game.screen.blit(self.completeImage, self.rect)
        else:
            ai_game.screen.blit(self.coolingDownImage, self.rect)
            pygame.draw.arc(ai_game.screen, (50, 50, 50), self.rect,
                            radians(startAngle), radians(360), 500)

    def use_skill(self, ai_game):
        '''发动技能'''
        if self.available:
            sound = pygame.mixer.Sound(self.soundFile)
            sound.set_volume(ai_game.FXVolume)
            sound.play()
            self.working = True
            self.reset_skill()

    def _working_skill_update(self, ai_game):
        '''技能工作时的状态更新'''
        if self.workTime <= self.time:
            self.workTime += 1
        else:  # 还原
            self.workTime = 0
            self.working = False

    def reset_skill(self):
        '''重置技能CD'''
        self.coolTime = 0
        self.available = False

    # 重定义pickle的loads,dumps
    def __getstate__(self):
        return repickle.getstate(self, "completeImage", "coolingDownImage")

    def __setstate__(self, state):
        repickle.setstate(self, state, "completeImage", "coolingDownImage")


class Skills_Frozen(Skills):
    '''技能1——冰冻'''

    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.coolingDownImage = pygame.image.load(
            "images/skills/skill1CoolingDown.png")
        self.completeImage = pygame.image.load(
            "images/skills/skill1Complete.png")
        self.rect = self.coolingDownImage.get_rect()
        self.rect.midtop = (910, 100)
        self.CD = ai_game.settings.skillsACD * ai_game.gameFrame
        self.time = ai_game.settings.skillsATime * ai_game.gameFrame
        self.coolTime = 0
        self.soundFile = "sounds/FX/frozen.ogg"


class Skills_Shield(Skills):
    '''技能2——盾牌'''

    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.coolingDownImage = pygame.image.load(
            "images/skills/skill2CoolingDown.png")
        self.completeImage = pygame.image.load(
            "images/skills/skill2Complete.png")
        self.rect = self.coolingDownImage.get_rect()
        self.rect.midtop = (950, 100)
        self.CD = ai_game.settings.skillsBCD * ai_game.gameFrame
        self.time = ai_game.settings.skillsBTime * ai_game.gameFrame
        self.coolTime = int(0.8 * self.CD)
        self.soundFile = "sounds/FX/shield.ogg"


class Skills_Firing(Skills):
    '''技能3——炸弹'''

    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.coolingDownImage = pygame.image.load(
            "images/skills/skill3CoolingDown.png")
        self.completeImage = pygame.image.load(
            "images/skills/skill3Complete.png")
        self.rect = self.coolingDownImage.get_rect()
        self.rect.midtop = (990, 100)
        self.CD = ai_game.settings.skillsCCD * ai_game.gameFrame
        self.bombTime = ai_game.settings.skillsCBombTime * ai_game.gameFrame
        self.time = ai_game.settings.skillsCTime * ai_game.gameFrame
        self.coolTime = int(0.5 * self.CD)
        self.soundFile = "sounds/FX/firing.ogg"
        self.bomb = Bomb(ai_game)
        self.playSound = False  # 是否已发生爆炸声

    def _working_skill_update(self, ai_game):
        '''技能三特制的工作时的状态更新'''
        if self.workTime <= self.time:
            self.workTime += 1
            if self.workTime >= self.bombTime:
                self.bomb.bombed = True
                ai_game._bomb_alien()
                if not self.playSound:
                    ai_game.bombSound.play()
                    self.playSound = True
        else:  # 还原
            self.bomb.bombed = False
            self.playSound = False
            self.workTime = 0
            self.working = False

    def use_skill(self, ai_game):
        '''发动技能，期间注意调整炸弹位置'''
        if self.available:
            self.working = True
            self.reset_skill()
            self.bomb.imageRect.centery = self.bomb.bombedImageRect.centery = ai_game.screenRect.centery + 100
            self.bomb.imageRect.centerx = self.bomb.bombedImageRect.centerx = ai_game.ship.rect.centerx
