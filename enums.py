from enum import Enum


class Area(str, Enum):
    ATTIC =                     "attic"
    CHAOS_DIMENSION =           "chaos dimension"
    CLOUD_47 =                  "cloud 47"
    GARDEN =                    "garden"
    KITCHEN =                   "kitchen"
    LIVING_ROOM =               "living room"
    SHED =                      "shed"
    YARD =                      "yard"


class AreaKey(str, Enum):
    DESCRIPTION =               "description"
    EXIT_REQUIREMENTS =         "exit_requirements"
    EXITS =                     "exits"
    ITEM =                      "item"
    ITEMS =                     "items"
    MESSAGE =                   "message"
    POST_ASHES_DESCRIPTION =    "post_ashes_description"


class Color(str, Enum):
    BLACK =                     "\033[30m"
    BLUE =                      "\033[34m"
    CYAN =                      "\033[36m"
    GREEN =                     "\033[32m"
    MAGENTA =                   "\033[35m"
    RED =                       "\033[31m"
    RESET =                     "\033[0m"
    WHITE =                     "\033[37m"
    YELLOW =                    "\033[33m"


class Command(str, Enum):
    EX =                        "ex "
    EXAMINE =                   "examine "
    EXIT =                      "exit"
    HELP =                      "help"
    HISTORY =                   "history"
    INV =                       "inv"
    INVENTORY =                 "inventory"
    QUIT =                      "quit"
    TAKE =                      "take "
    USE =                       "use "


class Item(str, Enum):
    ATTIC_KEY =                 "attic key"
    BONE =                      "bone"
    DOG_STATUE =                "dog statue"
    GARDEN_KEY =                "garden key"
    MAGIC_PLANT =               "magic plant"
    SHOVEL =                    "shovel"
    SHED_KEY =                  "shed key"
    UNTITLED_47 =               "untitled #47"
    WATERING_CAN =              "watering can"


class ItemState(str, Enum):
    EMPTY =                     "empty"
    FULL =                      "full"


class Object(str, Enum):
    ASHES =                     "ashes"
    BUTTON =                    "button"
    CARL =                      "carl"
    FIREPLACE =                 "fireplace"
    GARDEN_HOSE =               "garden hose"
    KITCHEN_DRAWER =            "kitchen drawer"
    LOOSE_PAINTING =            "loose painting"
    MAGIC_PLANT =               "magic plant"
    PEDESTAL =                  "pedestal"
    SAFE =                      "safe"
    STATUE_PLACED =             "statue_placed"
    WATERED_PLANT =             "watered_plant"
    X_MARK =                    "x mark"


class ObjectKey(str, Enum):
    ALSO_GIVES =                "also_gives"
    BECOMES_ITEM =              "becomes_item"
    CAN_INTERACT =              "can_interact"
    CHANGES_ITEM_STATE =        "changes_item_state"
    CONDITION =                 "condition"
    DESCRIPTION =               "description"
    ENABLES_EXIT =              "enables_exit"
    FAILED_STATE_RESULT =       "failed_state_result"
    GIVES_ITEM =                "gives_item"
    INTERACTABLES =             "interactables"
    INTERACTION_RESULT =        "interaction_result"
    POST_ASHES_DESCRIPTION =    "post_ashes_description"
    POST_BUTTON_DESCRIPTION =   "post_button_description"
    REQUIRES_ITEM =             "requires_item"
    REQUIRES_ITEM_STATE =       "requires_item_state"
    REVEALS =                   "reveals"
    SUCCESS_RESULT =            "success_result"
    USED_DESCRIPTION =          "used_description"
    VISIBLE =                   "visible"


class Path(str, Enum):
    DOWN =                      "down"
    EAST =                      "east"
    NORTH =                     "north"
    PORTAL =                    "portal"
    SOUTH =                     "south"
    UP =                        "up"
    WEST =                      "west"


class Status(str, Enum):
    CONTINUE =                  "CONTINUE"
    QUIT =                      "QUIT"


class Used(str, Enum):
    BUTTON =                    "button"
    CARL =                      "carl"
    DRAWER =                    "drawer"
    FIREPLACE =                 "fireplace"
    PAINTING =                  "painting"
    PLANT =                     "plant"
    X_MARK =                    "x mark"
