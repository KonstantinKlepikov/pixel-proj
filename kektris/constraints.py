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


class Direction(Enum):
    """Move or rotation directions
    """
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


class Shape(BaseEnum):
    """Block shape
    """
    I = 0
    O = 1
    J = 2
    L = 3
    T = 4
    S = 5
    Z = 6


class Orientation(BaseEnum):
    """Block orientation
    """
    L = 0
    U = 1
    R = 2
    D = 3


class CellState(BaseEnum):
    """Possible state of item
    """
    CLEAR = 0
    BLOCK = 1
    FR0ZEN = 2


class CellPlace(BaseEnum):
    """Placement of cell
    """
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3


class BlockOrientation(Enum):
    """All block orientation

    Order of clockwise rotation -->
    left, up, right, down
    all block will start from position (0, 3)
    config is wrt top left tile of grid (0, 0)
    """
    # all orientations of block I
    I_L = {(1, 0), (1, 1), (1, 2), (1, 3)}
    I_U = {(0, 2), (1, 2), (2, 2), (3, 2)}
    I_R = {(2, 0), (2, 1), (2, 2), (2, 3)}
    I_D = {(0, 1), (1, 1), (2, 1), (3, 1)}

    # all orientations of block O
    O_L = {(0, 1), (0, 2), (1, 1), (1, 2)}
    O_U = {(0, 1), (0, 2), (1, 1), (1, 2)}
    O_R = {(0, 1), (0, 2), (1, 1), (1, 2)}
    O_D = {(0, 1), (0, 2), (1, 1), (1, 2)}

    # all orientations of block J
    J_L = {(0, 0), (1, 0), (1, 1), (1, 2)}
    J_U = {(0, 2), (0, 1), (1, 1), (2, 1)}
    J_R = {(2, 2), (1, 0), (1, 1), (1, 2)}
    J_D = {(2, 0), (0, 1), (1, 1), (2, 1)}

    # all orientations of block L
    L_L = {(0, 2), (1, 0), (1, 1), (1, 2)}
    L_U = {(2, 2), (0, 1), (1, 1), (2, 1)}
    L_R = {(2, 0), (1, 0), (1, 1), (1, 2)}
    L_D = {(0, 0), (0, 1), (1, 1), (2, 1)}

    # all orientations of block S
    S_L = {(0, 1), (0, 2), (1, 0), (1, 1)}
    S_U = {(0, 1), (1, 1), (1, 2), (2, 2)}
    S_R = {(1, 1), (1, 2), (2, 0), (2, 1)}
    S_D = {(0, 0), (1, 0), (1, 1), (2, 1)}

    # all orientations of block Z
    Z_L = {(0, 0), (0, 1), (1, 1), (1, 2)}
    Z_U = {(0, 2), (1, 1), (1, 2), (2, 1)}
    Z_R = {(1, 0), (1, 1), (2, 1), (2, 2)}
    Z_D = {(0, 1), (1, 0), (1, 1), (2, 0)}

    # all orientations of block T
    T_L = {(1, 0), (1, 1), (1, 2), (0, 1)}
    T_U = {(0, 1), (1, 1), (2, 1), (1, 2)}
    T_R = {(1, 0), (1, 1), (1, 2), (2, 1)}
    T_D = {(0, 1), (1, 1), (2, 1), (1, 0)}


class FigureOrientation(Enum):
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
    O_L = (
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False),
            )
    O_U = (
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False),
            )
    O_R = (
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False),
            )
    O_D = (
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
