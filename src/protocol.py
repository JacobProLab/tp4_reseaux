import enum
import typing


class MyProtocol(enum.IntEnum):
    """
    Declaration des entetes dans une enumeration.
    Le type "enum.IntEnum" indique que les valeurs sont
    des entiers, et peuvent donc etre stockees dans un JSON.
    """
    GREET = enum.auto()
    TELL = enum.auto()
    OK = enum.auto()
    QUIT = enum.auto()


class Message(typing.TypedDict, total=True):
    """
    Format des message envoyes.
    """
    header: MyProtocol
    payload: str

