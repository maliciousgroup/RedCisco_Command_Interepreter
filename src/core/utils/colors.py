def colors() -> dict:
    _colors: dict = {
        'red': '\x1b[31;1m',
        'green': '\x1b[32;1m',
        'bold': '\x1b[1m',
        'reset': '\x1b[0m'
    }
    return _colors
