# --------------
# Shoot the Plane
# By Dreamer_Leo
# --------------

import pygame
import sys
import os
import shutil
import json
from tkinter import filedialog
from random import randint, choice
from time import sleep
import pickle

# 自己的运行库
from assets.assets import *
from assists.assists import *
from pages.pages import *
from stats.stats import *


class AlienInvasion:
    """管理游戏资源和游戏行为，以及主要游戏界面"""

    # ------------------预备

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        self._load_screen()
        self._load_stats()
        self._load_sounds()
        self.loadingPage.update_loading(self, "Game preparing...", 0.3)
        self._load_personal_settings()
        self._game_ready()

    def _load_screen(self):
        """加载游戏屏幕并展示加载页面"""
        self.settings = Settings()
        # 游戏窗口分辨率，赋给的属性对象self.screen是一个surface，用于显示游戏元素
        pygame.init()  # pygame初始化
        self.screen = pygame.display.set_mode(
            (self.settings.screenWidth, self.settings.screenHeight))
        self.screenRect = self.screen.get_rect()
        pygame.display.set_caption(self.settings.title)  # 窗口标题
        """ # 全屏的代码，但是我的背景是1024*768分辨率就不便再去做了
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen=(
            (self.screen.get_rect().width,self.screen.get_rect().height)) # 更新settings
        """
        self.loadingPage = LoadingPage(self, 3, "Loading statistics...")
        self.loadingPage.draw_loading(self, 1)

    def _load_stats(self):
        """建立游戏数据"""
        self.stats = GameStats(self)
        self.gameActive = False
        self.clock = pygame.time.Clock()
        self.userdataFile = self.settings.userdataFile
        with open(self.settings.defaultDataFile) as defaultDataFile:
            self.defaultData: dict = json.load(defaultDataFile)
        self.loadingPage.update_loading(self, "Loading game sounds...", 0.3)

    def _load_sounds(self):
        """加载游戏声音"""
        menuSelectdir = "sounds/BGM/menu"
        for root, dirs, files in os.walk(menuSelectdir):
            self.menuSelectSoundFile = os.path.join(root, choice(files))
        self.menuSelectSound = pygame.mixer.Sound(self.menuSelectSoundFile)
        fightingdir = "sounds/BGM/fighting"
        for root, dirs, files in os.walk(fightingdir):
            self.fightingSoundFile = os.path.join(root, choice(files))
        self.fightingSound = pygame.mixer.Sound(self.fightingSoundFile)
        self.loseGameSound = pygame.mixer.Sound("sounds/BGM/lose.mp3")
        self.breakRecordSound = pygame.mixer.Sound(
            "sounds/BGM/breakRecord.ogg")

        self.bulletSound = pygame.mixer.Sound("sounds/FX/fire_bullet.ogg")
        self.clickSound = pygame.mixer.Sound("sounds/FX/click.ogg")
        self.bombSound = pygame.mixer.Sound("sounds/FX/bomb.ogg")
        self.shipHitSound = pygame.mixer.Sound("sounds/FX/ship_hit.ogg")
        self.BGM = [self.menuSelectSound, self.fightingSound,
                    self.loseGameSound, self.breakRecordSound]
        self.FX = [self.bulletSound, self.clickSound,
                   self.bombSound, self.shipHitSound]

    def _game_ready(self):
        """游戏就绪"""
        self.menu = Menu(self)
        self.quitPage = QuitPage(self)
        self.loadingPage.update_loading(self, "Finish", 0.3)
        self.loadingPage.finish_loading(self)
        self.page = "menu"  # 游戏主页面
        self.subPage = None  # 游戏子页面
        self.quit = False  # 最高优先级的退出页面

    # ------------------主进程/开始/继续/保存/退出

    def run_game(self):
        """开始游戏主循环"""
        self.menuSelectSound.play(loops=-1, fade_ms=5000)
        while True:
            self.clock.tick(self.gameFrame)
            self.check_events()
            # 用事件循环，监视键盘和鼠标事件，并随之更新屏幕
            if not self.quit:
                if self.gameActive and self.page == "playing" and not self.subPage:
                    self.ship.update(self)
                    self._update_props()
                    self._update_bullets()
                    self._update_aliens()
                    self._update_skills()
            mouse_pos = pygame.mouse.get_pos()
            self.update_screen(mouse_pos)

    def _start_game_setup(self):
        """开始游戏的基本准备"""
        if os.path.exists(self.gamedataFile):
            os.remove(self.gamedataFile)  # 删档
        self.page = "playing"
        self.gameActive = True
        self.settings.__init__()
        self.menuSelectSound.fadeout(1000)
        self.fightingSound.stop()
        self.fightingSound.play(loops=-1, fade_ms=5000)

    def new_game(self):
        """开始新的游戏"""
        if os.path.exists(self.gamedataFile):
            self.subPage = "choose_new_game"
        else:
            # 实例创建
            self._start_game_setup()
            self.stats = GameStats(self)
            self.ship = Ship(self)
            self.bullets: list[Bullet] = []  # 创建一个子弹组
            self.aliens: list[Alien] = []
            self.props: list[Properties] = []
            self.skillA = Skills_Frozen(self)
            self.skillB = Skills_Shield(self)
            self.skillC = Skills_Firing(self)
            self.skills: list[Skills] = [self.skillA, self.skillB, self.skillC]
            # 准备就绪
            self._create_fleet()
            self.ship.center_ship(self)
            self._add_score(0)
            self.forceRefreshTime = self.settings.forceRefreshTime * self.gameFrame

    def continue_game(self):
        """继续游戏"""
        if os.path.exists(self.gamedataFile):
            with open(self.gamedataFile, "rb") as f:
                self.datas = pickle.loads(f.read())
            self.ship, self.stats, self.bullets, self.aliens, self.props, self.skills, \
                self.settings, self.refreshTime, self.forceRefreshTime = self.datas
            self.skillA, self.skillB, self.skillC = self.skills
            self.scoreboard = Scoreboard(self)  # 重新渲染计分板
            self.gameActive = True
            self.page = "playing"
            self._start_game_setup()
        else:  # 没有游戏存档
            self.subPage = "no_save"

    def save_game(self):
        """保存游戏"""
        try:
            self.datas = [self.ship, self.stats, self.bullets, self.aliens, self.props,
                          self.skills, self.settings, self.refreshTime, self.forceRefreshTime]
        except AttributeError:
            pass
        else:
            with open(self.gamedataFile, "wb") as f:
                f.write(pickle.dumps(self.datas))

    def _save_personal_userdata(self):
        """存储个人用户数据"""
        with open(self.userdataFile, "w") as userdataFile:
            self.allUserdata["playerData"][self.player] = self.userdata
            json.dump(self.allUserdata, userdataFile, indent=4)

    def _clear_userdata(self):
        """清除个人数据"""
        self.userdata = self.defaultData
        self._save_personal_userdata()
        if os.path.exists(self.gamedataFile):
            os.remove(self.gamedataFile)

    # ------------------用户

    def add_user(self, name):
        """添加用户"""
        self.player = name
        self.allUserdata["playerData"][self.player] = self.defaultData
        self._clear_userdata()
        os.makedirs(self.settings.gameFile + self.player)
        self.userNames.append(name)
        self.changeUserPage.__init__(self)

    def delete_user(self, name):
        """删除用户"""
        del self.allUserdata["playerData"][name]
        self.player = self.changeUserPage.next_player(name)
        self.allUserdata["chosenPlayer"] = self.player
        shutil.rmtree(self.settings.gameFile + name)
        with open(self.userdataFile, "w") as userdataFile:
            json.dump(self.allUserdata, userdataFile)
        self.userNames.remove(name)
        self.changeUserPage.__init__(self)

    def rename_user(self, name, rename):
        """重命名用户"""
        # 把旧的用户数据剪贴到新的用户数据当中
        self.player = rename
        del self.allUserdata["playerData"][name]
        self.allUserdata["playerData"][rename] = self.userdata
        # 创建新的个人文件夹，并把之前的逐个拷贝过去，再删掉原本的文件夹
        source = self.settings.gameFile + name
        target = self.settings.gameFile + rename
        os.makedirs(target)
        for root, dirs, files in os.walk(source):  # walk返回根目录，文件夹名列表，文件名列表
            for dir in dirs:
                shutil.copy(os.path.join(root, dir), target)  # join可以把文件名连接在一起
            for file in files:
                shutil.copy(os.path.join(root, file), target)
        shutil.rmtree(source)
        # 修改用户名单并重新初始化
        for index, username in enumerate(self.userNames):
            if username == name:
                self.userNames[index] = rename
                break
        self.changeUserPage.__init__(self)

    # ------------------游戏设置

    def _load_personal_settings(self):
        """加载个性化设置"""
        # 全部玩家信息
        with open(self.userdataFile) as userdataFile:
            self.allUserdata: dict = json.load(userdataFile)
        self.userNames = list(self.allUserdata["playerData"].keys())
        # 个人玩家信息
        self.player = self.allUserdata["chosenPlayer"]
        self.userdata: dict = self.allUserdata["playerData"][self.player]
        self.gamedataFile = self.settings.gameFile + \
            self.player + self.settings.gamedataFile
        # 音量
        self.gameFrame = self.userdata["gameSettings"]["gameFrame"]  # 游戏帧率
        self.BGMVolume = self.userdata["gameSettings"]["BGMVolume"]  # BGM音量
        self.FXVolume = self.userdata["gameSettings"]["FXVolume"]  # FX音量
        for bgm in self.BGM:
            bgm.set_volume(self.BGMVolume)
        for fx in self.FX:
            fx.set_volume(self.FXVolume)
        # 背景图片
        self.backgroundFile = self.userdata["gameSettings"]["background"]
        if not os.path.exists(self.backgroundFile):
            self.backgroundFile = self.settings.defaultBackgroundFile  # 不存在时就用默认图片
        self.background = pygame.image.load(self.backgroundFile)
        self.background = pygame.transform.scale(
            self.background, (self.settings.screenWidth, self.settings.screenHeight))
        # 最高分
        self.scoreboard = Scoreboard(self)

    def _save_settings(self):
        """保存设置"""
        page = self.settingsPage
        self.userdata["gameSettings"]["BGMVolume"] = page.BGMVolumeSlidebar.read()
        self.userdata["gameSettings"]["FXVolume"] = page.FXVolumeSlidebar.read()
        self.userdata["gameSettings"]["gameFrame"] = page.frameSlidebar.read(
            ndigits=0)
        self._save_personal_userdata()
        self._load_personal_settings()

    def _default_settings(self):
        """恢复默认设置"""
        self.userdata["gameSettings"]["BGMVolume"] = self.defaultData["gameSettings"]["BGMVolume"]
        self.userdata["gameSettings"]["BGMVolume"] = self.defaultData["gameSettings"]["BGMVolume"]
        self.userdata["gameSettings"]["gameFrame"] = self.defaultData["gameSettings"]["gameFrame"]
        self.settingsPage = SettingsPage(self)

    # ------------------操作

    def check_events(self):
        """事件管理函数，缩减run_game()长度"""
        for event in pygame.event.get():
            event = self._check_quit_event(event)
            if self.quit:
                self._check_choose_quit_events(event)
            else:
                if self.page == "menu":
                    self._check_menu_selecting_events(event)
                elif self.page == "new_game":
                    self._check_new_game_selecting_events(event)
                elif self.gameActive and self.page == "playing":
                    self._check_playing_game_events(event)
                elif self.page == "lose":
                    self._check_lose_game_events(event)
                elif self.page == "introductions":
                    self._check_showing_introduction_events(event)
                elif self.page == "settings":
                    self._check_settings_events(event)

    def _check_quit_event(self, event: pygame.event.Event):
        """退出游戏事件验证，并返回事件本身"""
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.quit = True
        return event

    def _check_choose_quit_events(self, event: pygame.event.Event):
        """退出弹窗操作"""
        page = self.quitPage
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if page.popup.get_result(mouse_pos) == 1:
                if self.gameActive:
                    self.save_game()  # 退游戏前先存档
                sys.exit()
            elif page.popup.get_result(mouse_pos) == -1:
                self.quit = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.quit = False

    def _check_menu_selecting_events(self, event: pygame.event.Event):
        """菜单页面操作"""
        page = self.menu
        if not self.subPage:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                # 这个点在矩形内部
                if page.continueGameButton.clicked(mouse_pos):
                    self.continue_game()
                elif page.newGameButton.clicked(mouse_pos):
                    self.page = "new_game"
                    self.newGamePage = NewGamePage(self)
                elif page.introButton.clicked(mouse_pos):
                    self.page = "introductions"
                    self.introductionsPage = IntroductionsPage(self)
                elif page.settingsButton.clicked(mouse_pos):
                    self.page = "settings"
                    self.settingsPage = SettingsPage(self)
                elif page.changeUserButton.clicked(mouse_pos):
                    self.changeUserPage = changeUserPage(self)
                    self.subPage = "change_user"
                elif page.quitImageRect.collidepoint(mouse_pos):
                    self.quit = True

        elif self.subPage == "no_save":  # 没有存档
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if page.noSavePopup.get_result(mouse_pos) == 1:
                    self.subPage = None
                    self.page = "new_game"
                elif page.noSavePopup.get_result(mouse_pos) == -1:
                    self.subPage = None

        elif self.subPage == "change_user":  # 更换用户
            page = self.changeUserPage
            # 在此过程中只改变self.allUserdata，最后OK退出才保存全部数据
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                for button in page.userButtons:
                    if button.clicked(mouse_pos):
                        self.player = button.msg
                        page.update_highlight(button.msg)
                if len(self.userNames) < self.settings.maxUserNum:
                    if page.addButton.clicked(mouse_pos):  # 增加用户
                        self.subPage = "new_user"
                        self.newUserPage = CreateUserPage(
                            self, "Input your name")
                if len(self.userNames) > 1:
                    if page.deleteButton.clicked(mouse_pos):  # 删除用户
                        self.subPage = "choose_delete_user"
                        self.changeUserPage._update_delete_user_popup(self)
                if page.renameButton.clicked(mouse_pos):  # 重命名
                    self.subPage = "rename_user"
                    self.renameUserPage = CreateUserPage(self, "Rename")
                elif page.OKButton.clicked(mouse_pos):  # 回到菜单
                    # 存储并重新加载全部数据
                    self.allUserdata["chosenPlayer"] = self.player
                    with open(self.userdataFile, "w") as userdataFile:
                        json.dump(self.allUserdata, userdataFile, indent=4)
                    self._load_personal_settings()
                    self.subPage = None

        elif self.subPage == "choose_delete_user":  # 删除用户的弹窗
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                popup = self.changeUserPage.deleteUserPopup
                if popup.get_result(mouse_pos) == 1:
                    self.delete_user(self.player)
                    self.subPage = "change_user"
                elif popup.get_result(mouse_pos) == -1:
                    self.subPage = "change_user"

        elif self.subPage == "new_user":  # 增加新用户的弹窗
            result = self.newUserPage.event_check(self, event)
            if result:
                self.add_user(result)
                self.subPage = "change_user"
            elif result == False:
                self.subPage = "change_user"

        elif self.subPage == "rename_user":  # 重命名用户的弹窗
            result = self.renameUserPage.event_check(self, event)
            if result:
                self.rename_user(self.player, result)
                self.subPage = "change_user"
            elif result == False:
                self.subPage = "change_user"

    def _check_new_game_selecting_events(self, event: pygame.event.Event):
        """选择难度界面事件"""
        page = self.newGamePage
        if not self.subPage:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if page.easyButton.clicked(mouse_pos):
                    self.settings = EasyMode()
                    self.new_game()
                elif page.mediumButton.clicked(mouse_pos):
                    self.settings = MediumMode()
                    self.new_game()
                elif page.hardButton.clicked(mouse_pos):
                    self.settings = HardMode()
                    self.new_game()
                elif page.backMenuButton.clicked(mouse_pos):
                    self.page = "menu"
                    
        elif self.subPage == "choose_new_game":
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if page.chooseNewGamePopup.get_result(mouse_pos) == 1:
                    os.remove(self.gamedataFile)  # 删档重开
                    self.subPage = None
                    self.new_game()
                elif page.chooseNewGamePopup.get_result(mouse_pos) == -1:
                    self.subPage = None

    def _check_playing_game_events(self, event: pygame.event.Event):
        """游戏进行时的操作"""
        if not self.subPage:
            if event.type == pygame.KEYDOWN:
                # 向左或向右移动飞船
                if event.key == pygame.K_RIGHT:
                    self.ship.movingRight = True
                elif event.key == pygame.K_LEFT:
                    self.ship.movingLeft = True
                elif event.key == pygame.K_SPACE:  # 发射子弹
                    self.stats.fireBullet = True
                elif event.key == pygame.K_ESCAPE:  # 游戏暂停
                    self._pause_game_debug()
                    pygame.mouse.set_visible(True)
                    self.subPage = "game_pause"
                    self.gamePausePage = GamePausePage(self)
                elif event.key == pygame.K_1:  # 一技能
                    self.skillA.use_skill(self)
                elif event.key == pygame.K_2:  # 二技能
                    self.skillB.use_skill(self)
                elif event.key == pygame.K_3:  # 三技能
                    self.skillC.use_skill(self)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.movingRight = False
                elif event.key == pygame.K_LEFT:
                    self.ship.movingLeft = False
                elif event.key == pygame.K_SPACE:
                    self.stats.fireBullet = False

        elif self.subPage == "game_pause":  # 游戏暂停界面
            page = self.gamePausePage
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # 回到游戏
                    self.subPage = None
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                # 回到游戏或返回菜单
                if page.continueButton.clicked(mouse_pos):
                    self.subPage = None
                if page.gameRestartButton.clicked(mouse_pos):
                    self.subPage = "choose_restart"
                if page.goBackMenuButton.clicked(mouse_pos):
                    self.subPage = "choose_go_menu"
                if page.gameSettingButton.clicked(mouse_pos):
                    self.page = "settings"
                    self.subPage = None
                    self.settingsPage = SettingsPage(self)

        elif self.subPage == "choose_restart":  # 是否重新开始
            page = self.gamePausePage
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if page.restartPopup.get_result(mouse_pos) == 1:  # 是
                    self.subPage = None
                    self.new_game()
                elif page.restartPopup.get_result(mouse_pos) == -1:  # 否
                    self.subPage = "game_pause"

        elif self.subPage == "choose_go_menu":  # 是否回到菜单
            page = self.gamePausePage
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if page.goMenuPopup.get_result(mouse_pos) == 1:  # 是
                    self.subPage = None
                    self.page = "menu"
                    self.gameActive = False
                    self.save_game()
                    self.fightingSound.fadeout(1000)
                    self.menuSelectSound.play(loops=-1, fade_ms=5000)
                elif page.goMenuPopup.get_result(mouse_pos) == -1:  # 否
                    self.subPage = "game_pause"

    def _check_lose_game_events(self, event: pygame.event.Event):
        """输掉游戏时的操作"""
        page = self.loseGamePage
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 空格回到主菜单
                self.page = "menu"
                self.breakRecordSound.fadeout(1000)
                self.loseGameSound.fadeout(1000)
                self.menuSelectSound.play(loops=-1, fade_ms=5000)
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if page.popup.get_result(mouse_pos) == 1:  # 是：重新开始
                self.page = "playing"
                self.gameActive = True
                self.breakRecordSound.fadeout(1000)
                self.loseGameSound.fadeout(1000)
                self.new_game()
            elif page.popup.get_result(mouse_pos) == -1:  # 否：返回菜单
                self.page = "menu"
                self.breakRecordSound.fadeout(1000)
                self.loseGameSound.fadeout(1000)
                self.menuSelectSound.play(loops=-1, fade_ms=5000)

    def _check_showing_introduction_events(self, event: pygame.event.Event):
        """介绍页面操作"""
        page = self.introductionsPage
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # 空格回到主菜单
                self.page = "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            # 回到主菜单
            if page.OKbutton.clicked(mouse_pos):
                self.page = "menu"
            # 翻页
            elif page.lastPageButton.clicked(mouse_pos):
                self.introductionsPage.last_page()
            elif page.nextPageButton.clicked(mouse_pos):
                self.introductionsPage.next_page()
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                for time in range(event.y):
                    self.introductionsPage.last_page()
            else:
                for time in range(-event.y):
                    self.introductionsPage.next_page()

    def _check_settings_events(self, event: pygame.event.Event):
        """设置页面操作"""
        page = self.settingsPage
        if not self.subPage:
            # 空格返回
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.gameActive:  # 游戏暂停期间
                        self.page = "playing"
                        self.subPage = "game_pause"
                        self.gameActive = True
                    else:
                        self.page = "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                # 落下鼠标检查活跃状态
                mouse_pos = pygame.mouse.get_pos()
                for slidebar in page.settingSlidebars:
                    slidebar.check_active(mouse_pos)
                # 点击OK按钮
                if page.settingsOKButton.clicked(mouse_pos):
                    if self.gameActive:  # 游戏暂停期间
                        self.page = "playing"
                        self.subPage = "game_pause"
                    else:
                        self.page = "menu"
                # 点击默认按钮
                elif page.resetDefaultSettingsButton.clicked(mouse_pos):
                    self._default_settings()
                # 点击清除个人数据按钮
                elif page.clearUserdataButton.clicked(mouse_pos):
                    self.subPage = "choose_clear_userdata"
                elif page.changeBGMButton.clicked(mouse_pos, False):
                    if self.gameActive:  # 游戏界面换BGM
                        key = "fightingSound"
                    else:  # 菜单界面换BGM
                        key = "menuSelectSound"
                    sound: pygame.mixer.Sound = self.__dict__[key]
                    sound.stop()
                    originalSoundFile = self.__dict__[key + "File"]
                    while self.__dict__[key + "File"] == originalSoundFile:
                        self._load_sounds()
                    self.__dict__[key].play(loops=-1)
                # 点击自定义背景按钮
                elif page.setBackgroundButton.clicked(mouse_pos, False):
                    backgroundFile = filedialog.askopenfilename()
                    if backgroundFile:
                        self.userdata["gameSettings"]["background"] = backgroundFile
                        self._save_personal_userdata()
                        self._load_personal_settings()
                elif page.clearBackgroundButton.clicked(mouse_pos):
                    self.subPage = "choose_clear_background"
                    
            elif event.type == pygame.MOUSEBUTTONUP :  # 抬鼠标全部取消活跃状态
                for slidebar in page.settingSlidebars:
                    slidebar.active = False
            self._save_settings()

        elif self.subPage == "choose_clear_userdata":  # 是否清除个人数据页面
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if page.clearUserdataPopup.get_result(mouse_pos) == 1:
                    self._clear_userdata()
                    self.subPage = None
                elif page.clearUserdataPopup.get_result(mouse_pos) == -1:
                    self.subPage = None

        elif self.subPage == "choose_clear_background":  # 是否清除背景
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if page.clearBackgroundPopup.get_result(mouse_pos) == 1:
                    self.userdata["gameSettings"]["background"] = ""
                    self._save_personal_userdata()
                    self._load_personal_settings()
                    self.subPage = None
                elif page.clearBackgroundPopup.get_result(mouse_pos) == -1:
                    self.subPage = None
                    
    # ------------------屏幕

    def update_screen(self, mouse_pos):
        """更新屏幕的函数，缩减run_game()长度"""
        self.screen.blit(self.background, (0, 0))  # 更新背景，当然也可以用fill()填颜色
        if self.quit:
            self.quitPage.draw_quit_page(mouse_pos)
        else:
            if self.page == "menu":
                self.menu.draw_menu(self, mouse_pos)
            elif self.page == "new_game":
                self.newGamePage.draw_new_game_page(self, mouse_pos)
            elif self.page == "introductions":
                self.introductionsPage.draw_introductions(self, mouse_pos)
            elif self.page == "settings":
                self.settingsPage.draw_settings(self, mouse_pos)
            elif self.gameActive and self.page == "playing":
                self._update_playing_game_screen(mouse_pos)
            elif self.page == "lose":
                self.loseGamePage.draw_lose_game(mouse_pos)
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _update_playing_game_screen(self, mouse_pos: tuple):
        """游戏进行时的屏幕"""
        self.ship.draw_ship(self)
        for bullet in self.bullets:
            bullet.draw_bullet(self)
        for alien in self.aliens:
            alien.draw_alien(self)
        for prop in self.props:
            prop.draw_prop(self)
        for skill in self.skills:
            skill.draw_skill(self)
        self.scoreboard.show_score(self)
        if self.skillC.working:  # C技能工作期间
            self.skillC.bomb.draw_bomb(self)
        if self.subPage == "game_pause":  # 暂停期间的屏幕
            self.gamePausePage.draw_game_pause(mouse_pos)
        elif self.subPage == "choose_restart":
            self.gamePausePage.restartPopup.draw_popup(mouse_pos)
        elif self.subPage == "choose_go_menu":
            self.gamePausePage.goMenuPopup.draw_popup(mouse_pos)
        else:
            pygame.mouse.set_visible(False)

    # !-----------------------------
    # 游戏中主要内容
    # !-----------------------------

    # ------------------道具

    def _update_props(self):
        """更新场上道具"""
        for prop in self.props:
            prop.update()
        if self.stats.propsCD >= self.settings.propCD * self.gameFrame:
            prop = choice([ExpandAttackRange(self)]*2 +
                          [StrengthenBullet(self)]*3 +
                          [DoubleScore(self)]*3 +
                          [None]*2)  # 随机抽取道具产生
            if prop:
                prop.x = randint(50, self.settings.screenWidth-50)
                self.props.append(prop)
            self.stats.propsCD = 0  # 道具计时器
        else:
            self.stats.propsCD += 1
        for prop in self.props.copy():  # 漏掉的道具及时清理
            if prop.rect.top > self.screenRect.bottom:
                self.props.remove(prop)
        self._prop_countdown()
        self._check_ship_props_collision()

    def _prop_countdown(self):
        """道具倒计时"""
        if self.stats.propsATime:
            self.stats.propsATime -= 1
        if self.stats.propsBTime:
            self.stats.propsBTime -= 1
        if self.stats.propsCTime:
            self.stats.propsCTime -= 1

    def _check_ship_props_collision(self):
        """检测船与道具的碰撞"""
        for prop in self.props.copy():
            if self.ship.rect.colliderect(prop.rect):
                self.props.remove(prop)
                if type(prop) == ExpandAttackRange:
                    self.stats.propsATime = self.settings.propsATime * self.gameFrame
                if type(prop) == StrengthenBullet:
                    self.stats.propsBTime = self.settings.propsBTime * self.gameFrame
                if type(prop) == DoubleScore:
                    self.stats.propsCTime = self.settings.propsCTime * self.gameFrame

    # ------------------子弹/炸弹和外星人

    def _update_bullets(self):
        """更新场上子弹"""
        for bullet in self.bullets:
            bullet.update()  # 小组的所有元素执行update()函数
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collison()
        self._fire_bullet()

    def _check_bullet_alien_collison(self):
        """响应子弹和外星人的碰撞"""
        for alien in self.aliens.copy():
            for bullet in self.bullets.copy():
                if alien.rect.colliderect(bullet.rect):
                    self.bullets.remove(bullet)
                    if self.stats.propsBTime:  # B道具释放时间
                        self._alien_hurt(alien, 3)
                    else:
                        self._alien_hurt(alien, 1)

    def _bomb_alien(self):
        """炸死外星人"""
        for alien in self.aliens.copy():
            if self.skillC.bomb.bombedImageRect.colliderect(alien.rect):
                self._alien_hurt(alien, 3)

    def _alien_hurt(self, alien: Alien, hurt: int):
        """一个外星人受伤"""
        alien.life -= hurt
        if alien.life <= 0:
            try:
                self.aliens.remove(alien)
            except ValueError:
                pass
            else:
                if self.stats.propsCTime:  # C道具释放时间
                    self._add_score(2*alien.killPoint *
                                    self.stats.killPointScale)
                else:
                    self._add_score(alien.killPoint *
                                    self.stats.killPointScale)

    def _fire_bullet(self):
        """发射子弹"""
        if self.stats.fireBullet:
            if self.stats.bulletCD <= 0:
                # 播放音效
                self.bulletSound.play()
                newBullet = Bullet(self)
                self.bullets.append(newBullet)
                if self.stats.propsATime:  # 技能释放时间
                    newBulletA, newBulletB = Bullet(self), Bullet(self)
                    newBulletA.rect.x += 50
                    newBulletB.rect.x -= 50
                    self.bullets.extend([newBulletA, newBulletB])
                self.stats.bulletCD = self.settings.bulletCD*self.gameFrame
            else:
                self.stats.bulletCD -= 1

    def _create_fleet(self):
        """建立一组外星人"""
        self.stats.alienWave += 1
        self._check_update_difficulty()
        for alienNumber in range(int(self.settings.alienNumber)):
            alien = Alien(self).generate_alien(self)
            alienWidth, alienHeight = alien.rect.size  # size返回矩形的宽高，是一个元组
            shipHeight = self.ship.rect.height
            availableSpaceY = self.settings.screenHeight - \
                shipHeight - self.settings.alienDistance*alienHeight  # 根据实际最多塞几行外星人？要留点空间打
            alien.x = randint(alienWidth, self.settings.screenWidth-alienWidth)
            alien.y = randint(0, int(availableSpaceY))
            alien.rect.x, alien.rect.y = alien.x, alien.y
            self.aliens.append(alien)

    def _update_aliens(self):
        """更新外星人的位置"""
        for alien in self.aliens:
            alien.update(self)
        for alien in self.aliens:
            # 外星人撞上飞机
            if self.ship.rect.colliderect(alien.rect):
                self._ship_hit(alien)
            # 外星人走到底线以下
            if alien.rect.bottom >= self.screenRect.bottom:
                self._ship_hit()
                break
        if self.aliens:  # 外星人没死光，主动刷新
            self.refreshTime = self.settings.refreshTime * self.gameFrame
            if self.forceRefreshTime <= 0:
                self._create_fleet()
                self.forceRefreshTime = self.settings.forceRefreshTime * self.gameFrame
            else:
                self.forceRefreshTime -= 1
        else:  # 外星人死光了，被动刷新
            self.forceRefreshTime = self.settings.forceRefreshTime * self.gameFrame
            if self.refreshTime <= 0:
                self._create_fleet()
            else:
                self.refreshTime -= 1

    def _ship_hit(self, alien=None):
        """外星人撞上飞船，或者走到底线以下"""
        if alien and self.skillB.working:  # 外星人撞上飞机，且B技能生效，直接更新为用完时间
            self.skillB.workTime = self.skillB.time
            self.aliens.remove(alien)
        else:  # B技能未生效，或者外星人到达底部
            self.aliens = []
            self.bullets = []
            if self.stats.shipLeft:
                # 扣血后重整旗鼓，并修改主动刷新时间
                self.stats.shipLeft -= 1
                self._create_fleet()
                self.ship.center_ship(self)
                self.scoreboard.prep_left_ship(self)
                self.shipHitSound.play()
                sleep(1)
                self.forceRefreshTime = self.settings.forceRefreshTime * self.gameFrame
                self.stats.propsATime = self.settings.protectTime * self.gameFrame  # 死亡重生保护
            else:
                self.shipHitSound.play()
                sleep(0.5)
                self.lose_game()

   # ------------------技能

    def _update_skills(self):
        """更新技能状态"""
        for skill in self.skills:
            skill._update_CD()
            if skill.working:
                skill._working_skill_update(self)

    # ------------------游戏暂停

    def _pause_game_debug(self):
        """修复游戏暂停后飞船继续的bug"""
        self.ship.movingLeft = self.ship.movingRight = False
        self.stats.fireBullet = False

    # ------------------游戏变化

    def _check_update_difficulty(self):
        """更新后检测是否提升难度"""
        if self.stats.alienWave % 3 == 1 and self.stats.alienWave > 1:
            self.stats.level += 1
            self.scoreboard.prep_level(self)
            self._increase_speed()

    def _increase_speed(self):
        """提高速度了！"""
        # 基本参数
        self.settings.forceRefreshTime /= self.settings.speedUpScale
        self.settings.shipSpeed *= self.settings.speedUpScale
        self.settings.bulletSpeed *= self.settings.speedUpScale
        self.settings.alienHorizonalSpeed *= self.settings.speedUpScale
        self.settings.alienVerticalSpeed *= self.settings.speedUpScale
        self.settings.bulletCD /= self.settings.speedUpScale
        self.settings.alienNumber += self.settings.alienNumberIncreaseScale
        # 冰冻技能
        self.settings.skillsACD /= self.settings.speedUpScale
        self.settings.skillsATime /= self.settings.speedUpScale**0.5
        # 护盾技能
        self.settings.skillsBCD /= self.settings.speedUpScale
        self.settings.skillsBTime /= self.settings.speedUpScale**0.5
        # 炸弹技能
        self.settings.skillsCCD /= self.settings.speedUpScale
        self.settings.skillsCBombTime /= self.settings.speedUpScale ** 0.8
        self.settings.skillsCTime /= self.settings.speedUpScale ** 0.8
        # 分数提高
        self.stats.killPointScale *= self.settings.killPointIncreaseScale

    def _add_score(self, addscore):
        """增加分数"""
        self.stats.score += addscore
        self.scoreboard.prep_score(self)
        self.scoreboard.update_high_score(self)

   # ------------------游戏失败

    def lose_game(self):
        """更新输掉游戏的状态"""
        self.gameActive = False
        self.page = "lose"
        self.fightingSound.fadeout(1000)
        if os.path.exists(self.gamedataFile):  # 删档
            os.remove(self.gamedataFile)
        self.loseGamePage = LoseGamePage(self)
        pygame.mouse.set_visible(True)


if __name__ == "__main__":
    # 创建游戏实例并开始游戏
    ai_game = AlienInvasion()
    ai_game.run_game()
