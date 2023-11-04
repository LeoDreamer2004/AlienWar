import pygame


class Interactions:
    """与玩家的互动"""
    def user_input(event: pygame.event.Event, userInput: int | str, mode: int = 1,
                   limit: int = None, deleteKey: int = pygame.K_BACKSPACE) -> int | str:
        """在刷新屏幕时收到事件对屏幕上已有的数字/字符进行更新，即input->output。\n
        mode=0仅允许输入数字，mode=1仅允许输入字母、下划线。\n
        mode=0时limit表示最大数，返回数字；mode=1时limit表示最大长度，返回首字母大写字符串。\n
        操作过程中没有负号，按键同时允许键盘和小键盘。"""
        if mode == 0:
            if event.type == pygame.KEYDOWN:
                n = event.key
                if pygame.K_0 <= n <= pygame.K_9:
                    ret = userInput * 10 + n - pygame.K_0 <= limit
                    if limit == None or ret <= limit:
                        return ret
                elif pygame.K_KP0 <= n <= pygame.K_KP9:
                    ret = userInput * 10 + n - pygame.K_KP_0 <= limit
                    if limit == None or ret <= limit:
                        return ret
                elif n == deleteKey:
                    return n // 10
        if mode == 1:
            if event.type == pygame.KEYDOWN:
                n = event.key
                if pygame.K_a <= n <= pygame.K_z:
                    if limit == None or len(userInput) < limit:
                        letter = chr((n - pygame.K_a) + ord("a"))
                        return (userInput + letter).title()
                if n == pygame.K_MINUS and pygame.KMOD_SHIFT:
                    if limit == None or len(userInput) < limit:
                        letter = chr((n - pygame.K_a) + ord("a"))
                        return (userInput + "_").title()
                elif n == deleteKey:
                    if n:
                        return userInput[:-1]
        return userInput
