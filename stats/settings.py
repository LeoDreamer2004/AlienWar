class Settings:
    """存储游戏设置"""

    def __init__(self):
        """初始化游戏设置"""
        # 窗口信息
        self.screenWidth, self.screenHeight = 1024, 768  # 屏幕大小
        self.title = "打灰机"  # 窗口标题

        # 用户和存档
        self.maxUserNum = 6  # 最大用户数量
        self.userdataFile = "userdata/userdata.json"  # 用户文件的文件名
        self.defaultDataFile = "userdata/default_data.json"  # 默认设置的文件位置
        self.gameFile = "userdata/"  # 游戏文件名，后接玩家名
        self.gamedataFile = "/gamedata.pkl"  # 游戏存档的文件名，前接玩家名
        self.defaultBackgroundFile = "images/background.bmp"  # 默认背景图片的文件位置
        
        # 飞船与子弹
        self.shipNumber = 3  # 补给飞船数量——[0,inf)的整数
        self.bulletWidth, self.bulletHeight = 5, 20  # 子弹尺寸
        self.bulletColor = (200, 60, 60)  # 子弹颜色
        self.shipMaxSpeed = 7  # 飞船的最大速度——(0,inf)
        self.shipSpeed = 4  # 飞船移动速度——(0,inf)
        self.bulletSpeed = 15  # 子弹速度——(0,inf)
        self.bulletCD = 0.1  # 连射子弹的时间——(0,inf)

        # 道具
        self.propCD = 17  # 道具的产生间隔时间
        self.propSpeed = 0.7  # 道具下落速度
        self.propsATime = 4  # A道具持续时间
        self.propsBTime = 6  # B道具持续时间
        self.propsCTime = 8  # C道具持续时间
        self.protectTime = 3  # 死亡重生A道具保护时间

        # 技能
        self.skillsACD: int  # A技能CD
        self.skillsATime = 2  # A技能持续时间
        self.skillsBCD: int  # B技能CD
        self.skillsBTime = 6  # B技能持续时间
        self.skillsCCD: int  # C技能CD
        self.skillsCBombTime = 0.5  # C技能爆炸所需时间
        self.skillsCTime = 1.5  # C技能持续时间

        # 外星人
        self.alienNumberIncreaseScale = 0.34  # 每一等级增加外星人数量——[0,inf)
        self.refreshTime = 0.7  # 两波外星人之间刷新时间——[0,inf)
        self.forceRefreshTime = 6  # 强制刷新时间——(0,inf)
        self.alienDistance = 6.0  # 外星人最低点离飞船的距离——(0,inf)


class EasyMode(Settings):
    """简单模式"""

    def __init__(self):
        super().__init__()
        self.alienNumber = 9  # 每波生成外星人的数量
        self.alienSpeedChaos = 0.4  # 外星人速度混乱度——(0,1)
        self.speedUpScale = 1.03  # 提高速度倍率——(1,inf)
        self.pointPlus = 1  # 得分加成
        self.killPointIncreaseScale = 1.02  # 提高得分倍率——(1,inf)
        self.alienHorizonalSpeed = 1.5  # 外星人水平移动速度——(0,inf)
        self.alienVerticalSpeed = 0.45  # 外星人竖直下落速度——(0,inf)
        self.skillsACD = 17  # A技能CD
        self.skillsBCD = 15  # B技能CD
        self.skillsCCD = 17  # C技能CD


class MediumMode(Settings):
    """中等模式"""

    def __init__(self):
        super().__init__()
        self.alienNumber = 10
        self.alienSpeedChaos = 0.45
        self.speedUpScale = 1.05
        self.pointPlus = 1.2
        self.killPointIncreaseScale = 1.1
        self.alienHorizonalSpeed = 1.8
        self.alienVerticalSpeed = 0.5
        self.skillsACD = 13
        self.skillsBCD = 10
        self.skillsCCD = 13


class HardMode(Settings):
    """困难模式"""

    def __init__(self):
        super().__init__()
        self.alienNumber = 11
        self.alienSpeedChaos = 0.5
        self.speedUpScale = 1.1
        self.pointPlus = 1.5
        self.killPointIncreaseScale = 1.2
        self.alienHorizonalSpeed = 2.0
        self.alienVerticalSpeed = 0.55
        self.skillsACD = 11
        self.skillsBCD = 8
        self.skillsCCD = 11
