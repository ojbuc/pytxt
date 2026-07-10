from enums import Area, AreaKey, Item, ItemState, Object, ObjectKey, Path


ITEM_DESCRIPTIONS = {
    Item.GARDEN_KEY: (
        "▶ A small brass key with intricate engravings. "
        "\n▶ It looks like it might unlock a garden door."
    ),
    Item.WATERING_CAN: {
        "empty": (
            "▶ A green metal watering can that's completely empty. "
            "\n▶ You can hear it echo when you shake it."
        ),
        "full": (
            "▶ A green metal watering can, full of water. "
            "\n▶ The water sloshes gently when you move it. Water is wet."
        ),
    },
    Item.SHED_KEY: (
        "▶ A rusty iron key that feels heavy in your hand. "
        "\n▶ It has the word 'SHED' etched into it."
    ),
    Item.SHOVEL: (
        "▶ A sturdy steel shovel with a wooden handle. "
        "\n▶ Perfect for digging in dirt and uncovering buried secrets."
    ),
    Item.ATTIC_KEY: (
        "▶ An ornate silver key with scrollwork. "
        "\n▶ It looks like it belongs to something important."
    ),
    Item.BONE: (
        "▶ A well-preserved dog bone, ideally sized for a friendly canine "
        "companion."
    ),
    Item.DOG_STATUE: (
        "▶ A hand crafted miniature statue, in the visage of Carl the dog."
        "\n▶ It appears to be made of moon rock, how does that work?"
    ),
    Item.UNTITLED_47: (
        "▶ An abstract painting with bold reds, blues and greens. "
        "\n▶ The chaotic swirls of color are oddly mesmerizing."
    ),
    Item.MAGIC_PLANT: (
        "▶ A peculiar flowering plant in an ornate pot. \n▶ Its leaves shimmer"
        " with an otherworldly quality, as if touched by starlight."
    ),
}

# Per-object wrong item responses. Keys are interactable names.
# Each entry can be a single string (used for all wrong items)
# or a dict mapping specific item names to responses.
# Falls back to GENERIC_WRONG_ITEM_RESPONSE if not defined here.
WRONG_ITEM_RESPONSES = {
# Example of a flat response (same message regardless of item used):
# "garden hose": "▶ That doesn't seem to work with the hose.",
#
# Example of per-item responses:
    Object.ASHES: {
        Item.GARDEN_KEY: "▶ Throwing the garden key into hot ashes "
                         "seems unwise.",
    },
    Object.CARL: {
        Item.ATTIC_KEY: "▶ Carl doesn't want the key, he gazes longingly at "
                        "the clouds.",
        Item.GARDEN_KEY: "▶ Carl doesn't want the key, he rejects the concept "
                         "of keys, unlocking and confinement.",
        Item.SHED_KEY:"▶ Carl doesn't want the key, he rejects the concept "
                         "of keys, unlocking and confinement.",
        Item.SHOVEL: "▶ Digging into Carl would make quite a mess.\n▶ You feel"
                     " like this is a decision that you will regret.",
        Item.WATERING_CAN: "▶ Carl doesn't want water, he feels no thirst, "
                           "only a deep hunger.",
    },
    Object.GARDEN_HOSE: {
        Item.ATTIC_KEY: "▶ The garden hose isn't locked but the attic is...",
        Item.BONE: "▶ Wetting the bone here has no effect.",
        Item.GARDEN_KEY: "▶ The garden hose isn't locked, nice try though.",
        Item.SHED_KEY: "▶ The garden hose isn't locked, you should use this "
                       "on the shed instead.",
        Item.SHOVEL: "▶ Digging into the garden hose sounds like a bad idea, "
                     "it provides you with precious water after all.",
        Item.UNTITLED_47: "▶ You resist the urge to damage this beautiful "
                          "artwork with water.",
    },
    Object.MAGIC_PLANT: {
        Item.ATTIC_KEY: "▶ You can't unlock a plant with a key.",
        Item.BONE: "▶ An ancient magic force prevents you from striking the "
                   "plant with your bone.",
        Item.GARDEN_KEY: "▶ You can't unlock a plant with a key.",
        Item.SHED_KEY: "▶ You can't unlock a plant with a key.",
        Item.SHOVEL: "▶ The plant suddenly summons forth a magical barrier, "
                     "shielding it from harm.\n▶ The shovel can't dig it.",
        Item.UNTITLED_47: "▶ The plant glows faintly luminescent, it looks to "
                          "be reacting the presence of the painting.\n▶ "
                          "Perhaps the painting is important, you feel that you"
                          " should hold on to it.",
    },
    Object.PEDESTAL: {
        Item.ATTIC_KEY: "▶ There's no need to unlock the pedestal, "
                        "it has no lock.",
        Item.BONE: "▶ The bone won't fit in the groove.",
        Item.GARDEN_KEY: "▶ There's no need to unlock the pedestal, "
                         "it has no lock.",
        Item.SHED_KEY: "▶ There's no need to unlock the pedestal, "
                       "it has no lock.",
        Item.SHOVEL: "▶ The shovel won't fit in the groove.",
        Item.UNTITLED_47: "▶ The painting won't fit in the groove.",
    },
    Object.X_MARK: {
        Item.GARDEN_KEY: "▶ You can't unlock the ground with a key, "
                         "it's just dirt.",
        Item.SHED_KEY: "▶ You can't unlock the ground with a key, "
                       "it's just dirt.",
        Item.WATERING_CAN: "▶ There's no need to water the ground here.",
        Item.UNTITLED_47: "▶ You shouldn't litter here.",
    },
}

GENERIC_WRONG_ITEM_RESPONSE = (
    "▶ That doesn't seem to do anything useful here."
)

AREAS = {
    Area.KITCHEN: {
        AreaKey.DESCRIPTION: "A small kitchen with a slightly open drawer.",
        AreaKey.EXITS: {Path.NORTH: Area.LIVING_ROOM, Path.SOUTH: Area.GARDEN},
        AreaKey.EXIT_REQUIREMENTS: {
            Path.SOUTH: {
                AreaKey.ITEM: Item.GARDEN_KEY,
                AreaKey.MESSAGE: "▶ The garden door is locked, now what?",
            }
        },
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            Object.KITCHEN_DRAWER: {
                ObjectKey.DESCRIPTION: (
                    "▶ A wooden drawer, you can see a shiny object"
                    " reflecting light from within."
                ),
                ObjectKey.USED_DESCRIPTION: (
                    "▶ An open wooden drawer, now empty."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You open the drawer and find a garden key!"
                ),
                ObjectKey.GIVES_ITEM: Item.GARDEN_KEY,
            }
        },
    },
    Area.LIVING_ROOM: {
        AreaKey.DESCRIPTION: "A cozy living room with a fireplace.",
        AreaKey.POST_ASHES_DESCRIPTION: (
            "The warmth of the fireplace has faded, the living room is a bit "
            "chilly now."
        ),
        AreaKey.EXITS: {Path.SOUTH: Area.KITCHEN, Path.UP: Area.ATTIC},
        AreaKey.EXIT_REQUIREMENTS: {
            Path.UP: {
                AreaKey.ITEM: Item.ATTIC_KEY,
                AreaKey.MESSAGE: "▶ The hatch to the attic is locked tight.",
            }
        },
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            Object.FIREPLACE: {
                ObjectKey.DESCRIPTION: (
                    "▶ A simple brick fireplace that keeps the place warm."
                    ),
                ObjectKey.USED_DESCRIPTION: (
                    "▶ A fireplace with a button under the mantle.\n▶ You "
                    "can't help but feel that you should press it."
                ),
                ObjectKey.POST_BUTTON_DESCRIPTION: (
                    "▶ A fireplace with burning ashes and a button under the "
                    "mantle.\n▶ The ashes inside are smoldering.\n▶ The button"
                    " has already been pressed."
                    ),
                ObjectKey.POST_ASHES_DESCRIPTION: (
                    "▶ A fireplace with damp ashes and a button under the "
                    "mantle.\n▶ The ashes inside are extinguished.\n▶ The "
                    "button has already been pressed."
                    ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The fireplace is too hot to search through safely, but "
                    "wait...\n▶ You notice a small button hidden underneath "
                    "the mantle."
                ),
                ObjectKey.REVEALS: Object.BUTTON,
            },
            Object.BUTTON: {
                ObjectKey.DESCRIPTION: (
                    "▶ A small, worn button hidden under the fireplace mantle."
                ),
                ObjectKey.USED_DESCRIPTION: (
                    "▶ You remember pressing this button and unlocking the "
                    "compartment beneath the ashes."
                    ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You press it and hear a mechanical lock *click* "
                    "underneath the hot ashes. \n▶ The mechanism has unlocked"
                    " something!"
                ),
                ObjectKey.REVEALS: Object.ASHES,
                ObjectKey.VISIBLE: False,
            },
            Object.ASHES: {
                ObjectKey.DESCRIPTION: (
                    "▶ Hot, smoldering ashes in the fireplace. Do not touch!"
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.WATERING_CAN,
                ObjectKey.REQUIRES_ITEM_STATE: ItemState.FULL, 
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The ashes are too dangerous to search through safely."
                ),
                ObjectKey.FAILED_STATE_RESULT: (
                    "▶ The watering can is empty. "
                    "\n▶ You need water to douse the ashes."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You douse the ashes with water.\n▶ They cool down and "
                    "you search through them safely, finding a hidden shed "
                    "key!"
                ),
                ObjectKey.GIVES_ITEM: Item.SHED_KEY,
                ObjectKey.CHANGES_ITEM_STATE: 
                    {Item.WATERING_CAN: ItemState.EMPTY},
                ObjectKey.VISIBLE: False,
            },
        },
    },
    Area.GARDEN: {
        AreaKey.DESCRIPTION: (
            "A sunny garden with a small shed and a coiled hose.",
            ),
        AreaKey.EXITS: {
            Path.NORTH: Area.KITCHEN,
            Path.EAST: Area.SHED,
            Path.WEST: Area.YARD,
            Path.UP: Area.CLOUD_47,
        },
        AreaKey.EXIT_REQUIREMENTS: {
            Path.EAST: {
                AreaKey.ITEM: Item.SHED_KEY,
                AreaKey.MESSAGE: "▶ The shed is locked, you shall not pass!"
            },
            Path.UP: {
                ObjectKey.CONDITION: Object.WATERED_PLANT,
                AreaKey.MESSAGE: "▶ There's no way up from here.",
            },
        },
        AreaKey.ITEMS: {Item.WATERING_CAN: "▶ An empty green watering can."},
        ObjectKey.INTERACTABLES: {
            Object.GARDEN_HOSE: {
                ObjectKey.DESCRIPTION: (
                    "▶ A long green garden hose coiled neatly near a spigot. "
                    "\n▶ The spigot is turned on and water drips from the hose"
                    " nozzle."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.WATERING_CAN,
                ObjectKey.REQUIRES_ITEM_STATE: ItemState.EMPTY,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You need something to fill up with water."
                ),
                ObjectKey.FAILED_STATE_RESULT: (
                    "▶ The watering can is already full."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You fill the watering can with water from the "
                    "garden hose."
                ),
                ObjectKey.CHANGES_ITEM_STATE: 
                    {Item.WATERING_CAN: ItemState.FULL}, 
            },
            Object.MAGIC_PLANT: {
                ObjectKey.DESCRIPTION: (
                    "▶ A peculiar flowering plant in an ornate pot."
                    "\n▶ Its leaves shimmer with an otherworldly quality, as "
                    "if touched by starlight.\n▶ It looks quite thirsty."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.WATERING_CAN,
                ObjectKey.REQUIRES_ITEM_STATE: ItemState.FULL,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The plant doesn't look like it needs anything."
                ),
                ObjectKey.FAILED_STATE_RESULT: (
                    "▶ The watering can is empty. The plant looks thirsty."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You water the magic plant.\n▶ It glows brilliantly and "
                    "suddenly grows into an enormous beanstalk that "
                    "reaches up into the clouds!\n▶ A set of natural steps have"
                    " formed in its trunk, creating a pathway towards the sky."
                ),
                ObjectKey.CHANGES_ITEM_STATE: 
                    {Item.WATERING_CAN: ItemState.EMPTY},
                ObjectKey.ENABLES_EXIT: Path.UP,
                ObjectKey.VISIBLE: False,
            },
        },
    },
    Area.SHED: {
        AreaKey.DESCRIPTION: "▶ A shed for storing various items.",
        AreaKey.EXITS: {Path.WEST: Area.GARDEN},
        AreaKey.ITEMS: {Item.SHOVEL: "▶ A steel tool used for digging."},
        ObjectKey.INTERACTABLES: {},
    },
    Area.YARD: {
        AreaKey.DESCRIPTION: (
            "A ground of fertile green and earthy browns. Carl the dog roams "
            "here, outside the bounds of time and space."
        ),
        AreaKey.EXITS: {Path.EAST: Area.GARDEN},
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            Object.X_MARK: {
                ObjectKey.DESCRIPTION: (
                    "▶ A suspicious X carved into the dirt.\n▶ Someone has "
                    "clearly marked this spot for a reason.\n▶ The dirt looks "
                    "like it has been disturbed recently."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.SHOVEL,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You need something to dig with.",
                    ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You dig at the X mark with your shovel.\n▶ After a few "
                    "minutes of digging, your shovel hits something hard."
                    "\n▶ You uncover a small metal box containing an ornate "
                    "attic key and a well-preserved dog bone!"
                ),
                ObjectKey.GIVES_ITEM: Item.ATTIC_KEY,
                ObjectKey.ALSO_GIVES: Item.BONE,
                ObjectKey.VISIBLE: False,
            },
            Object.CARL: {
                ObjectKey.DESCRIPTION: (
                    "▶ A friendly golden retriever with bright, intelligent "
                    "eyes wags his tail when he sees you.\n▶ It seems he's "
                    "trying to tell you something important."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.BONE,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ Carl looks at you expectantly and then glances "
                    "meaningfully at a spot on the ground.\n▶ He paws at the "
                    "dirt and whines softly, as if trying to show you "
                    "something.\n▶ 'Woof!', Carl scratches at the ground in "
                    "the shape of an X..."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You give Carl the bone and he absolutely loses his mind "
                    "with joy!\n▶ He grabs it gently in his mouth, does three "
                    "perfect spins and then drops into a play bow with his tail"
                    " wagging so hard his whole body wiggles.\n▶ 'WOOF WOOF!' "
                    " he barks happily, then settles down to contentedly chew"
                    " his new treasure.\n▶ What a good boy!"
                ),
            },
        },
    },
    Area.ATTIC: {
        AreaKey.DESCRIPTION: (
            "A dusty attic filled with old furniture and mysterious shadows."
        ),
        AreaKey.EXITS: {Path.DOWN: Area.LIVING_ROOM},
        AreaKey.ITEMS: {
            Item.DOG_STATUE: (
                "▶ An oddly familiar looking craft that requires "
                "further inspection."
            ),
        },
        ObjectKey.INTERACTABLES: {
            Object.LOOSE_PAINTING: {
                ObjectKey.DESCRIPTION: (
                    "▶ A loose abstract painting hangs askew on the wall."
                    "\n▶ Its canvas splashed with bold reds, blues and greens "
                    "that seem to swirl and clash without pattern.\n▶ The paint"
                    " is thick in some places, thin in others, creating a "
                    "chaotic yet somehow captivating mess of color.\n▶ A small "
                    "placard below simply reads 'Untitled #47.'"
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You carefully remove the painting from the wall. "
                    "\n▶ Behind, you discover a sturdy safe bolted into the "
                    "wall with the number 47 etched prominently on its front. "
                    "\n▶ The painting is light enough to carry with you."
                ),
                ObjectKey.REVEALS: Object.SAFE,
                ObjectKey.BECOMES_ITEM: Item.UNTITLED_47,
            },
            Object.SAFE: {
                ObjectKey.DESCRIPTION: (
                    "▶ A heavy metal safe is built here into the wall."
                    "\n▶ It has a combination lock that looks quite complex."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The safe is locked tight.\n▶ You'll need to figure out "
                    "how to unlock it."
                ),
                ObjectKey.VISIBLE: False,
            },
        },
    },
    Area.CLOUD_47: {
        AreaKey.DESCRIPTION: (
            "The moon glows bright, you stand on a cloud high above the surface"
            ".\n  The air shimmers with ethereal energy and strange celestial "
            "music seems to emanate from the cloud itself."
        ),
        AreaKey.EXITS: 
            {Path.DOWN: Area.GARDEN, Path.PORTAL: Area.CHAOS_DIMENSION},
        AreaKey.EXIT_REQUIREMENTS: {
            Path.PORTAL: {
                ObjectKey.CONDITION: Object.STATUE_PLACED,
                AreaKey.MESSAGE: "▶ There's nothing here but thin air.",
            }
        },
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            Object.PEDESTAL: {
                ObjectKey.REQUIRES_ITEM: Item.DOG_STATUE,
                ObjectKey.DESCRIPTION: (
                    "▶ A solid golden pedestal stands here, upon further "
                    "examination, you notice a groove at the top.\n▶ Perhaps "
                    "you could place an item there?"
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ It won't budge an inch, some unknown force from a "
                    "familiar source binds it here."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ The statue begins to pulsate and emit a low hum...\n"
                    "▶ A swirling vortex of violet and black tears open in the"
                    " air beside the pedestal!\n"
                    "▶ A portal to another dimension manifests before you."
                ),
                ObjectKey.ENABLES_EXIT: Path.PORTAL,
                ObjectKey.VISIBLE: True,
            },
        },
    },
    Area.CHAOS_DIMENSION: {
        AreaKey.DESCRIPTION: (
            "▶ An endless expanse of churning nothing stretches in every "
            "direction.\n▶ The chaos doesn't rage... it simply is, vast and "
            "indifferent, older than the house, older than Carl, older than "
            "the concept of gardens, sheds and keys.\n▶ Within in it, a hidden "
            "entity watches you. It does not seem pleased."
        ),
        AreaKey.EXITS: {},
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            #Object.     
        },
    },
}
