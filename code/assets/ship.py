import pygame
from assets.repickle import repickle


class Ship:
    '''管理飞船'''

    def __init__(self, ai_game):  # 实际上ai_game是AlienInvasion类的东西
        '''初始化飞船并设置好初始位置'''
        # 加载飞船图像并获取外接矩形
        self.image = pygame.image.load("images/ship.png")
        self.shieldImage = pygame.image.load("images/shield.png")
        self.rect = self.image.get_rect()
        self.shieldRect = self.shieldImage.get_rect()
        # 放在底部中间
        # 矩形对象有center,centerx,centery,top,bottom,left,right等等可以设置
        self.rect.midbottom = ai_game.screenRect.midbottom
        # 移动的标志，引入是为了便于长按
        self.movingRight = False
        self.movingLeft = False
        # 跟踪飞船位置
        self.x = float(self.rect.x)

    def draw_ship(self, ai_game):
        '''画飞船'''
        ai_game.screen.blit(self.image, self.rect)  # 绘制到rect的位置
        if ai_game.skillB.working:
            self.shieldRect.center = self.rect.center
            ai_game.screen.blit(self.shieldImage, self.shieldRect)

    def update(self, ai_game):
        '''根据移动位置调整飞船的位置'''
        if self.movingRight and self.rect.right < ai_game.screenRect.right:  # 别跑出去了
            self.x += ai_game.settings.shipSpeed
        if self.movingLeft and self.rect.left > ai_game.screenRect.left:
            self.x -= ai_game.settings.shipSpeed
        self.rect.x = self.x  # 这么绕一圈是因为rect矩形的x坐标只能是整数...所以中转一下

    def center_ship(self, ai_game):
        '''（因为死亡）把飞船移动到屏幕底部正中央'''
        self.rect.midbottom = ai_game.screenRect.midbottom
        self.x = float(self.rect.x)

    # 重定义pickle的loads,dumps
    def __getstate__(self):
        return repickle.getstate(self, "image", "shieldImage")

    def __setstate__(self, state):
        repickle.setstate(self, state, "image", "shieldImage")
