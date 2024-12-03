from enum import IntEnum, auto

class State(IntEnum):
    """Conversation states for the bot."""
    URL = auto()
    LOGIN = auto()
    PASSWORD = auto()