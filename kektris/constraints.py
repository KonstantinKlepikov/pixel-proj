from enum import Enum, auto


class BaseEnum(Enum):
    """Base class for enumeration
    """
    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def get_values(cls) -> list[int]:
        return [e.value for e in cls]

    @classmethod
    def get_includes(cls) -> list['BaseEnum']:
        return [i for i in cls]

    @classmethod
    def get_names(cls) -> list[str]:
        return cls._member_names_


class Direction(Enum):
    """Move or rotation directions
    """
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


class Orientation(BaseEnum):
    """Block orientation
    """
    L = auto()
    U = auto()
    R = auto()
    D = auto()


class CellState(BaseEnum):
    """Possible state of item
    """
    CLEAR = auto()
    BLOCK = auto()
    FR0ZEN = auto()


class FigureOrientation(BaseEnum):
    """All figures orientation (by longest flat side faces)
    """
    # all orientations of figure I
    I_L = (
        (False, True, False, False),
        (False, True, False, False),
        (False, True, False, False),
        (False, True, False, False),
            )
    I_U = (
        (False, False, False, False),
        (True, True, True, True),
        (False, False, False, False),
        (False, False, False, False),
            )
    I_R = (
        (False, False, True, False),
        (False, False, True, False),
        (False, False, True, False),
        (False, False, True, False),
            )
    I_D = (
        (False, False, False, False),
        (False, False, False, False),
        (True, True, True, True),
        (False, False, False, False),
            )

    # all orientations of figure O
    O = (
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False),
            )

    # all orientations of figure J
    J_L = (
        (False, True, False, False),
        (False, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
            )
    J_U = (
        (False, False, False, False),
        (True, True, True, False),
        (False, False, True, False),
        (False, False, False, False),
            )
    J_R = (
        (False, True, False, False),
        (False, True, False, False),
        (True, True, False, False),
        (False, False, False, False),
            )
    J_D = (
        (True, False, False, False),
        (True, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
            )

    # all orientations of figure L
    L_L = (
        (False, True, False, False),
        (False, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
            )
    L_U = (
        (False, False, False, False),
        (True, True, True, False),
        (False, False, True, False),
        (False, False, False, False),
            )
    L_R = (
        (True, True, False, False),
        (False, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    L_D = (
        (True, False, False, False),
        (True, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
            )

    # all orientations of figure S
    S_L = (
        (True, False, False, False),
        (True, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    S_U = (
        (False, True, True, False),
        (True, True, False, False),
        (False, False, False, False),
        (False, False, False, False),
            )
    S_R = (
        (False, True, False, False),
        (False, True, True, False),
        (False, False, True, False),
        (False, False, False, False),
            )
    S_D = (
        (False, False, False, False),
        (False, True, True, False),
        (True, True, False, False),
        (False, False, False, False),
            )

    # all orientations of figure Z
    Z_L = (
        (False, True, False, False),
        (True, True, False, False),
        (True, False, False, False),
        (False, False, False, False),
            )
    Z_U = (
        (True, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
            )
    Z_R = (
        (False, False, True, False),
        (False, True, True, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    Z_D = (
        (False, False, False, False),
        (True, True, False, False),
        (False, True, True, False),
        (False, False, False, False),
            )

    # all orientations of figure T
    T_L = (
        (False, True, False, False),
        (False, True, True, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    T_U = (
        (False, False, False, False),
        (True, True, True, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    T_R = (
        (False, True, False, False),
        (True, True, False, False),
        (False, True, False, False),
        (False, False, False, False),
            )
    T_D = (
        (False, True, False, False),
        (True, True, True, False),
        (False, False, False, False),
        (False, False, False, False),
            )


ARRIVE_TOP = [(x, -4) for x in range(30)]
ARRIVE_BOTTOM = [(x, 34) for x in range(30)]
ARRIVE_LEFT = [(-4, y) for y in range(30)]
ARRIVE_RIGHT = [(34, y) for y in range(30)]
ARRIVE = ARRIVE_TOP + ARRIVE_BOTTOM + ARRIVE_LEFT + ARRIVE_RIGHT

LEFT_FREEZE_ZONE = {(16, y) for y in range(34)}
RIGHT_FREEZE_ZONE = {(17, y) for y in range(34)}
TOP_FREEZE_ZONE = {(x, 16) for x in range(34)}
BOTTOM_FREEZE_ZONE = {(x, 17) for x in range(34)}
