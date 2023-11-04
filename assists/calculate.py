class Calculate():
    """计算用"""

    def add(x: tuple, y: tuple):
        return tuple(i+j for i, j in zip(x, y))

    def mul(x: tuple, y: float, intize: bool = True):
        if intize:
            return tuple(int(i*y) for i in x)
        else:
            return tuple(i*y for i in x)
