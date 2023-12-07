import pygame


class Interactions:
    """与玩家的互动输入框"""

    def input_number(event: pygame.event.Event, userInput: int,
                     maxNumber: int = None, deleteKey: int = pygame.K_BACKSPACE) -> int:
        if event.type == pygame.KEYDOWN:
            n = event.key
            if n == deleteKey:
                return userInput // 10
            if maxNumber is not None and n > maxNumber:
                return userInput

            if pygame.K_0 <= n <= pygame.K_9:
                ret = userInput * 10 + n - pygame.K_0 <= maxNumber
            elif pygame.K_KP0 <= n <= pygame.K_KP9:
                ret = userInput * 10 + n - pygame.K_KP_0 <= maxNumber
            return ret

        return userInput

    def input_string(event: pygame.event.Event, userInput: str,
                     maxLen: int = None, deleteKey: int = pygame.K_BACKSPACE) -> str:
        if event.type == pygame.KEYDOWN:
            n = event.key
            if n == deleteKey and n:
                return userInput[:-1]
            if maxLen is not None and len(userInput) >= maxLen:
                return userInput

            if pygame.K_a <= n <= pygame.K_z:
                letter = chr((n - pygame.K_a) + ord("a"))
                return (userInput + letter).title()
            if n == pygame.K_MINUS and pygame.KMOD_SHIFT:
                return (userInput + "_").title()

        return userInput
