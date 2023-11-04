import pygame
from assists.calculate import Calculate


class ShortText:
    """管理游戏中的短文本"""

    def __init__(self, ai_game, position: tuple, msg: str = "",
                 size: int = 40, color: tuple = (255, 255, 255),
                 fontStyle: str = "Comic Sans MS", italic: bool = False, bold: bool = False):
        self.screen: pygame.Surface = ai_game.screen
        self.font = pygame.font.SysFont(
            fontStyle, size, bold=bold, italic=italic)
        self.position = position
        self.color = color
        self.image = self.font.render(msg, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def draw_text(self):
        """渲染文本"""
        self.screen.blit(self.image, self.rect)

    def change_msg(self, msg):
        """修改文本内容并重新渲染"""
        self.image = self.font.render(msg, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.draw_text()


class LongText:
    """管理游戏中的长文本"""

    def __init__(self, ai_game, filename: str, position: tuple, lines: tuple = None,
                 fontStyle: str = "Comic Sans MS", size: int = 40, color: tuple = (0, 0, 0), rowSpacing: float = 1.2):
        """初始化，lines为(a,b)表示从a到b行，含两端，不写表示全文本；rowSpacing表示行间距"""
        self.game = ai_game
        self.screen: pygame.Surface = ai_game.screen
        self.filename = filename
        with open(filename) as file:
            self.filestrs = file.readlines()
        self.position = position  # 第一行左上角的位置
        self.fontStyle = fontStyle
        self.size = size
        self.color = color
        self.rowSpacing = rowSpacing
        if lines:
            self.filestrs = self.filestrs[lines[0]-1:lines[1]]
            self.start = lines[0]
        else:
            self.start = 1

    def separate(self, sep: str = "------"):
        """返回一个LongText列表，其中按照长文本的sep字符串隔开"""
        ret: list[LongText] = []
        startline = self.start
        for index, filestr in enumerate(self.filestrs):
            line = index + self.start
            if filestr.rstrip() == sep:  # 断开
                ret.append(LongText(self.game, self.filename, self.position,
                                    (startline, line - 1), self.fontStyle, self.size, self.color, self.rowSpacing))
                startline = line + 1
        ret.append(LongText(self.game, self.filename, self.position,
                            (startline, line), self.fontStyle, self.size, self.color, self.rowSpacing))
        return ret

    def draw_text(self):
        """渲染文本"""
        for filestr in self.filestrs:
            filestr = filestr.rstrip()
            self.font = pygame.font.SysFont(self.fontStyle, self.size)
            self.image = self.font.render(filestr, True, self.color)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.position
            self.position = Calculate.add(
                self.position, (0, self.size*self.rowSpacing))
            self.screen.blit(self.image, self.rect)
