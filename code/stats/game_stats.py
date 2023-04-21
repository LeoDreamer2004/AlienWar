class GameStats:
    '''跟踪游戏内所有统计信息'''

    def __init__(self, ai_game):
        '''初始化统计信息'''
        self.shipLeft = ai_game.settings.shipNumber  # 剩余船只
        self.score = 0  # 游戏分数
        self.alienWave = 0  # 游戏波数
        self.level = 1  # 游戏等级
        self.fireBullet = False  # 是否正在开火
        self.bulletCD = 0  # 子弹CD
        self.killPointScale = 1  # 击杀分数等级
        self.propsCD = 0  # 道具CD
        self.breakRecord = False  # 是否破纪录
        self.propsATime = 0  # 道具A——扩展面积
        self.propsBTime = 0  # 道具B——增强攻击力
        self.propsCTime = 0  # 道具C——双倍得分
