from enum import Enum


class Area(str, Enum):
    ATTIC = "attic"
    CHAOS_CORE = "chaos core"
    CHAOS_DIMENSION = "chaos dimension"
    FRACTURED_ECHO = "fractured echo"
    CRIMSON_RIFT = "crimson rift"
    CLOUD_47 = "cloud 47"
    DEAD_ROOM = "dead room"
    GARDEN = "garden"
    KITCHEN = "kitchen"
    LIVING_ROOM = "living room"
    PIGPEN = "pigpen"
    SHED = "shed"
    THE_VOID = "the void"
    THE_INVERSE = "the inverse"
    WASTELAND = "wasteland"
    YARD = "yard"


class AreaKey(str, Enum):
    CONFIRM_DECLINE_MESSAGE = "confirm_decline_message"
    CONFIRM_PROMPT = "confirm_prompt"
    CONFIRM_QUESTION = "confirm_question"
    CONFIRM_SUCCESS_MESSAGE = "confirm_success_message"
    DESCRIPTION = "description"
    EXIT_REQUIREMENTS = "exit_requirements"
    EXITS = "exits"
    ITEM = "item"
    ITEMS = "items"
    MESSAGE = "message"
    POST_ASHES_DESCRIPTION = "post_ashes_description"


class Color(str, Enum):
    BLACK = "\033[30m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    MAGENTA = "\033[35m"
    RED = "\033[31m"
    RESET = "\033[0m"
    YELLOW = "\033[33m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_WHITE = "\033[97m"
    BRIGHT_YELLOW = "\033[93m"


class Command(str, Enum):
    ABANDON = "abandon"
    DEBUG = "debug "
    EX = "ex "
    EXAMINE = "examine "
    HELP = "help"
    HISTORY = "history"
    INV = "inv"
    INVENTORY = "inventory"
    TAKE = "take "
    USE = "use "


class Item(str, Enum):
    ANCHOR = "anchor"
    ATTIC_KEY = "attic key"
    BONE = "bone"
    DOG_STATUE = "dog statue"
    GARDEN_KEY = "garden key"
    PAINTED_EYE = "painted eye"
    PIG_KEY = "pig key"
    SHOVEL = "shovel"
    SHED_KEY = "shed key"
    UNTITLED_47 = "untitled #47"
    VIAL_OF_CORROSIVE_BILE = "vial of corrosive bile"
    WATERING_CAN = "watering can"


class ItemState(str, Enum):
    EMPTY = "empty"
    FULL = "full"


class Object(str, Enum):
    ASHES = "ashes"
    BUTTON = "button"
    CARL = "carl"
    ENTITY_FRAGMENT = "entity fragment"  # Object.BECOMES_ITEM
    FIREPLACE = "fireplace"
    GARDEN_HOSE = "garden hose"
    GRATER_MECHANISM = "grater mechanism"
    KITCHEN_DRAWER = "kitchen drawer"
    KITCHEN_FLOOR = "kitchen floor"
    LOOSE_PAINTING = "loose painting"  # Object.BECOMES_ITEM
    MAGIC_PLANT = "magic plant"
    PEDESTAL = "pedestal"
    REFRIGERATOR = "refrigerator"
    SAFE = "safe"
    SKELETAL_HAND = "skeletal hand"
    STATUE_PLACED = "statue_placed"
    WATERED_PLANT = "watered_plant"
    WELL_OF_GRIEF = "well of grief"
    WOODEN_TABLE = "wooden table"
    WARPED_TABLE = "warped table"
    X_MARK = "x mark"


class ObjectKey(str, Enum):
    ALSO_GIVES = "also_gives"
    BECOMES_ITEM = "becomes_item"
    CAN_INTERACT = "can_interact"
    CHANGES_ITEM_STATE = "changes_item_state"
    CONDITION = "condition"
    DESCRIPTION = "description"
    ENABLES_EXIT = "enables_exit"
    FAILED_STATE_RESULT = "failed_state_result"
    GIVES_ITEM = "gives_item"
    HIDDEN_DESCRIPTION = "hidden_description"
    HIDDEN_DESCRIPTION_ITEM = "hidden_description_item"
    INTERACTABLES = "interactables"
    INTERACTION_RESULT = "interaction_result"
    POST_ASHES_DESCRIPTION = "post_ashes_description"
    POST_BUTTON_DESCRIPTION = "post_button_description"
    POST_X_MARK_DIG_DESCRIPTION = "post_x_mark_dig_description"
    REQUIRES_ITEM = "requires_item"
    REQUIRES_ITEM_STATE = "requires_item_state"
    REVEALS = "reveals"
    SUCCESS_RESULT = "success_result"
    USED_DESCRIPTION = "used_description"
    VISIBLE = "visible"


class Path(str, Enum):
    DOWN = "down"
    EAST = "east"
    NORTH = "north"
    PORTAL = "portal"
    SOUTH = "south"
    UP = "up"
    WEST = "west"


class Status(str, Enum):
    CONTINUE = "CONTINUE"
    QUIT = "QUIT"


class Used(str, Enum):
    BUTTON = "button"
    CARL = "carl"
    DRAWER = "drawer"
    FIREPLACE = "fireplace"
    PAINTING = "painting"
    PLANT = "plant"
    X_MARK = "x mark"
