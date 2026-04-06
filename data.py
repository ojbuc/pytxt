from enums import Area, Item, Object, Path


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
# "ashes": {
#     "shovel": "▶ Digging through hot ashes seems unwise.",
#     "bone":   "▶ The ashes don't want your bone.",
# },
}

GENERIC_WRONG_ITEM_RESPONSE = (
    "▶ That doesn't seem to do anything useful here."
)

AREAS = {
    Area.KITCHEN: {
        Area.DESCRIPTION: "A small kitchen with a slightly open drawer.",
        Area.EXITS: {Path.NORTH: Area.LIVING_ROOM, Path.SOUTH: Area.GARDEN},
        Area.EXIT_REQUIREMENTS: {
            Path.SOUTH: {
                Area.ITEM: Item.GARDEN_KEY,
                Area.MESSAGE: "▶ The garden door is locked, now what?",
            }
        },
        Area.ITEMS: {},
        Object.INTERACTABLES: {
            Object.KITCHEN_DRAWER: {
                Object.DESCRIPTION: (
                    "▶ A wooden drawer, you can see a shiny object"
                    " reflecting light from within."
                ),
                Object.USED_DESCRIPTION: (
                    "▶ An open wooden drawer, now empty."
                ),
                Object.CAN_INTERACT: True,
                Object.INTERACTION_RESULT: (
                    "▶ You open the drawer and find a garden key!"
                ),
                Object.GIVES_ITEM: Item.GARDEN_KEY,
                Object.USED: False,
            }
        },
    },
    Area.LIVING_ROOM: {
        Area.DESCRIPTION: "A cozy living room with a fireplace.",
        Area.EXITS: {Path.SOUTH: Area.KITCHEN, Path.UP: Area.ATTIC},
        Area.EXIT_REQUIREMENTS: {
            Path.UP: {
                Area.ITEM: Item.ATTIC_KEY,
                Area.MESSAGE: "▶ The hatch to the attic is locked tight.",
            }
        },
        Area.ITEMS: {},
        Object.INTERACTABLES: {
            Object.FIREPLACE: {
                Object.DESCRIPTION: (
                    "▶ A simple brick fireplace that keeps the place warm."
                    ),
                Object.USED_DESCRIPTION: (
                    "▶ A fireplace with a button under the mantle.\n▶ You "
                    "can't help but feel that you should press it."
                ),
                Object.POST_BUTTON_DESCRIPTION: (
                    "▶ A fireplace with burning ashes and a button under the "
                    "mantle.\n▶ The ashes inside are smoldering.\n▶ The button"
                    " has already been pressed."
                    ),
                Object.POST_ASHES_DESCRIPTION: (
                    "▶ A fireplace with damp ashes and a button under the "
                    "mantle.\n▶ The ashes inside are extinguisehd.\n▶ The "
                    "button has already been pressed."
                    ),
                Object.CAN_INTERACT: True,
                Object.INTERACTION_RESULT: (
                    "▶ The fireplace is too hot to search through safely, but "
                    "wait...\n▶ You notice a small button hidden underneath "
                    "the mantle."
                ),
                Object.REVEALS: Object.BUTTON,
                Object.USED: False,
            },
            Object.BUTTON: {
                Object.DESCRIPTION: (
                    "▶ A small, worn button hidden under the fireplace mantle."
                ),
                Object.USED_DESCRIPTION: (
                    "▶ You remember pressing this button and unlocking the "
                    "compartment beneath the ashes."
                    ),
                Object.CAN_INTERACT: True,
                Object.INTERACTION_RESULT: (
                    "▶ You press it and hear a mechanical lock *click* "
                    "underneath the hot ashes. \n▶ The mechanism has unlocked"
                    " something!"
                ),
                Object.REVEALS: Object.ASHES,
                Object.VISIBLE: False,
                Object.USED: False,
            },
            Object.ASHES: {
                Object.DESCRIPTION: (
                    "▶ Hot, smoldering ashes in the fireplace. Do not touch!"
                ),
                Object.CAN_INTERACT: True,
                Object.REQUIRES_ITEM: Item.WATERING_CAN,
                Object.REQUIRES_ITEM_STATE: "full",
                Object.INTERACTION_RESULT: (
                    "▶ The ashes are too dangerous to search through safely."
                ),
                Object.FAILED_STATE_RESULT: (
                    "▶ The watering can is empty. "
                    "\n▶ You need water to douse the ashes."
                ),
                Object.SUCCESS_RESULT: (
                    "▶ You douse the ashes with water.\n▶ They cool down and "
                    "you search through them safely, finding a hidden shed "
                    "key!"
                ),
                Object.GIVES_ITEM: Item.SHED_KEY,
                Object.CHANGES_ITEM_STATE: {Item.WATERING_CAN: "empty"},
                Object.VISIBLE: False,
                Object.USED: False,
            },
        },
    },
    Area.GARDEN: {
        Area.DESCRIPTION: "A sunny garden with a small shed and a coiled hose.",
        Area.EXITS: {
            Path.NORTH: Area.KITCHEN,
            Path.EAST: Area.SHED,
            Path.WEST: Area.YARD,
            Path.UP: Area.CLOUD_47,
        },
        Area.EXIT_REQUIREMENTS: {
            Path.EAST: {
                Area.ITEM: Item.SHED_KEY,
                Area.MESSAGE: "▶ The shed is locked, you shall not pass!"
            },
            Path.UP: {
                Object.CONDITION: Object.WATERED_PLANT,
                Area.MESSAGE: "▶ There's no way up from here.",
            },
        },
        Area.ITEMS: {Item.WATERING_CAN: "▶ An empty green watering can."},
        Object.INTERACTABLES: {
            Object.GARDEN_HOSE: {
                Object.DESCRIPTION: (
                    "▶ A long green garden hose coiled neatly near a spigot. "
                    "\n▶ The spigot is turned on and water drips from the hose"
                    " nozzle."
                ),
                Object.CAN_INTERACT: True,
                Object.REQUIRES_ITEM: Item.WATERING_CAN,
                Object.INTERACTION_RESULT: (
                    "▶ You need something to fill up with water."
                ),
                Object.SUCCESS_RESULT: (
                    "▶ You fill the watering can with water from the "
                    "garden hose."
                ),
                Object.CHANGES_ITEM_STATE: {Item.WATERING_CAN: "full"},
                Object.USED: False,
            },
            Object.MAGIC_PLANT: {
                Object.DESCRIPTION: (
                    "▶ A peculiar flowering plant in an ornate pot."
                    "\n▶ Its leaves shimmer with an otherworldly quality, as "
                    "if touched by starlight.\n▶ It looks quite thirsty."
                ),
                Object.CAN_INTERACT: True,
                Object.REQUIRES_ITEM: Item.WATERING_CAN,
                Object.REQUIRES_ITEM_STATE: "full",
                Object.INTERACTION_RESULT: (
                    "▶ The plant doesn't look like it needs anything."
                ),
                Object.FAILED_STATE_RESULT: (
                    "▶ The watering can is empty. The plant looks thirsty."
                ),
                Object.SUCCESS_RESULT: (
                    "▶ You water the magic plant.\n▶ It glows brilliantly and "
                    "suddenly grows into an enormous beanstalk that "
                    "reaches up into the clouds!\n▶ A set of natural steps have"
                    " formed in its trunk, creating a pathway to the sky."
                ),
                Object.CHANGES_ITEM_STATE: {Item.WATERING_CAN: "empty"},
                Object.ENABLES_EXIT: Path.UP,
                Object.VISIBLE: False,
                Object.USED: False,
            },
        },
    },
    Area.SHED: {
        Area.DESCRIPTION: "▶ A shed for storing various items.",
        Area.EXITS: {Path.WEST: Area.GARDEN},
        Area.ITEMS: {Item.SHOVEL: "▶ A steel tool used for digging."},
        Object.INTERACTABLES: {},
    },
    Area.YARD: {
        Area.DESCRIPTION: (
            "A ground of fertile green and earthy browns. Carl the dog roams "
            "here, outside the bounds of time and space."
        ),
        Area.EXITS: {Path.EAST: Area.GARDEN},
        Area.ITEMS: {},
        Object.INTERACTABLES: {
            Object.X_MARK: {
                Object.DESCRIPTION: (
                    "▶ A suspicious X carved into the dirt.\n▶ Someone has "
                    "clearly marked this spot for a reason.\n▶ The dirt looks "
                    "like it has been disturbed recently."
                ),
                Object.CAN_INTERACT: True,
                Object.REQUIRES_ITEM: Item.SHOVEL,
                Object.INTERACTION_RESULT: "▶ You need something to dig with.",
                Object.SUCCESS_RESULT: (
                    "▶ You dig at the X mark with your shovel.\n▶ After a few "
                    "minutes of digging, your shovel hits something hard."
                    "\n▶ You uncover a small metal box containing an ornate "
                    "attic key and a well-preserved dog bone!"
                ),
                Object.GIVES_ITEM: Item.ATTIC_KEY,
                Object.ALSO_GIVES: Item.BONE,
                Object.VISIBLE: False,
                Object.USED: False,
            },
            Object.CARL: {
                Object.DESCRIPTION: (
                    "▶ A friendly golden retriever with bright, intelligent "
                    "eyes wags his tail when he sees you.\n▶ It seems he's "
                    "trying to tell you something important."
                ),
                Object.CAN_INTERACT: True,
                Object.REQUIRES_ITEM: Item.BONE,
                Object.INTERACTION_RESULT: (
                    "▶ Carl looks at you expectantly and then glances "
                    "meaningfully at a spot on the ground.\n▶ He paws at the "
                    "dirt and whines softly, as if trying to show you "
                    "something.\n▶ 'Woof!', Carl scratches at the ground in "
                    "the shape of an X..."
                ),
                Object.SUCCESS_RESULT: (
                    "▶ You give Carl the bone and he absolutely loses his mind "
                    "with joy!\n▶ He grabs it gently in his mouth, does three "
                    "perfect spins and then drops into a play bow with his tail"
                    " wagging so hard his whole body wiggles.\n▶ 'WOOF WOOF!' "
                    " he barks happily, then settles down to contentedly chew"
                    " his new treasure.\n▶ What a good boy!"
                ),
                Object.USED: False,
            },
        },
    },
    Area.ATTIC: {
        Area.DESCRIPTION: (
            "A dusty attic filled with old furniture and mysterious shadows."
        ),
        Area.EXITS: {Path.DOWN: Area.LIVING_ROOM},
        Area.ITEMS: {
            Item.DOG_STATUE: (
                "▶ An oddly familiar looking craft that requires "
                "further inspection."
            ),
        },
        Object.INTERACTABLES: {
            Object.LOOSE_PAINTING: {
                Object.DESCRIPTION: (
                    "▶ A loose abstract painting hangs askew on the wall."
                    "\n▶ Its canvas splashed with bold reds, blues and greens "
                    "that seem to swirl and clash without pattern.\n▶ The paint"
                    " is thick in some places, thin in others, creating a "
                    "chaotic yet somehow captivating mess of color.\n▶ A small "
                    "placard below simply reads 'Untitled #47.'"
                ),
                Object.CAN_INTERACT: True,
                Object.INTERACTION_RESULT: (
                    "▶ You carefully remove the painting from the wall. "
                    "\n▶ Behind, you discover a sturdy safe bolted into the "
                    "wall with the number 47 etched prominently on its front. "
                    "\n▶ The painting is light enough to carry with you."
                ),
                Object.REVEALS: Object.SAFE,
                Object.BECOMES_ITEM: Item.UNTITLED_47,
                Object.USED: False,
            },
            Object.SAFE: {
                Object.DESCRIPTION: (
                    "▶ A heavy metal safe is built here into the wall."
                    "\n▶ It has a combination lock that looks quite complex."
                ),
                Object.CAN_INTERACT: True,
                Object.INTERACTION_RESULT: (
                    "▶ The safe is locked tight.\n▶ You'll need to figure out "
                    "how to unlock it."
                ),
                Object.VISIBLE: False,
                Object.USED: False,
            },
        },
    },
    Area.CLOUD_47: {
        Area.DESCRIPTION: (
            "The moon glows bright, you stand on a cloud high above the surface"
            ".\n  The air shimmers with ethereal energy and strange celestial "
            "music seems to emanate from the cloud itself."
        ),
        Area.EXITS: {Path.DOWN: Area.GARDEN, Path.PORTAL: Area.CHAOS_DIMENSION},
        Area.EXIT_REQUIREMENTS: {
            Path.PORTAL: {
                Object.CONDITION: Object.STATUE_PLACED,
                Area.MESSAGE: "▶ There's nothing here but thin air.",
            }
        },
        Area.ITEMS: {},
        Object.INTERACTABLES: {
            Object.PEDESTAL: {
                Object.REQUIRES_ITEM: Item.DOG_STATUE,
                Object.DESCRIPTION: (
                    "▶ A solid golden pedestal stands here, upon further "
                    "examination, you notice a groove at the top.\n▶ Perhaps "
                    "you could place an item there?"
                ),
                Object.CAN_INTERACT: True,
                Object.INTERACTION_RESULT: (
                    "▶ It won't budge an inch, some unknown force from a "
                    "familiar source binds it here."
                ),
                Object.SUCCESS_RESULT: (
                    "▶ The statue begins to pulsate and emit a low hum...\n"
                    "▶ A swirling vortex of violet and black tears open in the"
                    " air beside the pedestal!\n"
                    "▶ A portal to another dimension manifests before you."
                ),
                Object.ENABLES_EXIT: Path.PORTAL,
                Object.VISIBLE: True,
                Object.USED: False,
            },
        },
    },
    Area.CHAOS_DIMENSION: {
        Area.DESCRIPTION: (
            ""
        ),
        Area.EXITS: {},
        Area.ITEMS: {},
        Object.INTERACTABLES: {},
    },
}
