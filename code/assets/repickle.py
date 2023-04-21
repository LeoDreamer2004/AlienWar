import pygame


class repickle:
    '''重写pickle'''
    def getstate(obj, *attribute_name: str):
        state = obj.__dict__.copy()
        for surface in attribute_name:
            image = state.pop(surface)
            state[surface + "Str"] = (pygame.image.tostring(
                image, "RGBA"), image.get_size())
        return state

    def setstate(obj, state, *attribute_name: str):
        for surface in attribute_name:
            imageStr, imageSize = state.pop(surface + "Str")
            state[surface] = pygame.image.fromstring(
                imageStr, imageSize, "RGBA")
        obj.__dict__.update(state)
