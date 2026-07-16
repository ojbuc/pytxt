from enums import Area, AreaKey, Item, ItemState, Object, ObjectKey, Path

ITEM_DESCRIPTIONS = {
    Item.GARDEN_KEY: (
        "▶ A small brass Key with intricate engravings. "
        "\n▶ It looks like it might unlock a Garden door."
    ),
    Item.WATERING_CAN: {
        "empty": (
            "▶ A green metal Watering Can that's completely empty. "
            "\n▶ You can hear it echo when you shake it."
        ),
        "full": (
            "▶ A green metal Watering Can, full of water. "
            "\n▶ The water sloshes gently when you move it. Water is wet."
        ),
    },
    Item.SHED_KEY: (
        "▶ A rusty iron Key that feels heavy in your hand. "
        "\n▶ It has the word 'SHED' etched into it."
    ),
    Item.SHOVEL: (
        "▶ A sturdy steel Shovel with a wooden handle. "
        "\n▶ Perfect for digging in dirt and uncovering buried secrets."
    ),
    Item.ATTIC_KEY: (
        "▶ An ornate silver Key with scrollwork. "
        "\n▶ It looks like it belongs to something important."
    ),
    Item.BONE: (
        "▶ A well-preserved Bone of unknown origin, ideally sized for a "
        "friendly canine companion."
    ),
    Item.DOG_STATUE: (
        "▶ A hand crafted miniature Statue, in the visage of Carl the Dog."
        "\n▶ It appears to be made of moon rock, how does that work?"
    ),
    Item.UNTITLED_47: (
        "▶ An abstract painting with bold reds, blues and greens. "
        "\n▶ The chaotic swirls of color are oddly mesmerizing."
    ),
    Item.PAINTED_EYE: (
        "▶ A single Painted Eye, freshly cut from a canvas and still radiating"
        " a faint, mammalian heat.\n▶ Hold it to your face and the world "
        "unpeels itself."
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
        Item.GARDEN_KEY: "▶ Throwing the Garden Key into hot ashes "
        "seems unwise.",
    },
    Object.CARL: {
        Item.ATTIC_KEY: "▶ Carl doesn't want the Key, he gazes longingly at "
        "the clouds.",
        Item.GARDEN_KEY: "▶ Carl doesn't want the Key, he rejects the concept "
        "of keys, unlocking and confinement.",
        Item.SHED_KEY: "▶ Carl doesn't want the Key, he rejects the concept "
        "of keys, unlocking and confinement.",
        Item.SHOVEL: "▶ Digging into Carl would make quite a mess.\n▶ You feel"
        " like this is a decision that you will regret.",
        Item.WATERING_CAN: "▶ Carl doesn't want water, he feels no thirst, "
        "only a deep hunger.",
    },
    Object.GARDEN_HOSE: {
        Item.ATTIC_KEY: "▶ The Garden hose isn't locked but the Attic is...",
        Item.BONE: "▶ Wetting the Bone here has no effect.",
        Item.GARDEN_KEY: "▶ The Garden Hose isn't locked, nice try though.",
        Item.SHED_KEY: "▶ The Garden Hose isn't locked, you should use this "
        "on the shed instead.",
        Item.SHOVEL: "▶ Digging into the Garden Hose sounds like a bad idea, "
        "it provides you with precious water after all.",
        Item.UNTITLED_47: "▶ You resist the urge to damage this beautiful "
        "artwork with water.",
    },
    Object.MAGIC_PLANT: {
        Item.ATTIC_KEY: "▶ You can't unlock a Plant with a Key.",
        Item.BONE: "▶ An ancient magic force prevents you from striking the "
        "Plant with your Bone.",
        Item.GARDEN_KEY: "▶ You can't unlock a Plant with a Key.",
        Item.SHED_KEY: "▶ You can't unlock a Plant with a Key.",
        Item.SHOVEL: "▶ The plant suddenly summons forth a magical barrier, "
        "shielding it from harm.\n▶ The Shovel can't dig it.",
        Item.UNTITLED_47: "▶ The Plant glows faintly luminescent, it looks to "
        "be reacting the presence of the painting.\n▶ "
        "Perhaps the painting is important, you feel that you"
        " should hold on to it.",
    },
    Object.PEDESTAL: {
        Item.ATTIC_KEY: "▶ There's no need to unlock the Pedestal, "
        "it has no lock.",
        Item.BONE: "▶ The Bone won't fit in the groove.",
        Item.GARDEN_KEY: "▶ There's no need to unlock the Pedestal, "
        "it has no lock.",
        Item.SHED_KEY: "▶ There's no need to unlock the Pedestal, "
        "it has no lock.",
        Item.SHOVEL: "▶ You try to dig into the Pedestal, but you fail, it's "
        "made of radiant gold and literally invincible, darn.",
        Item.UNTITLED_47: "▶ The painting won't fit in the groove.",
    },
    Object.X_MARK: {
        Item.GARDEN_KEY: "▶ You can't unlock the ground with a Key, "
        "it's just dirt.",
        Item.SHED_KEY: "▶ You can't unlock the ground with a Key, "
        "it's just dirt.",
        Item.WATERING_CAN: "▶ There's no need to water the ground here.",
        Item.UNTITLED_47: "▶ You shouldn't litter here.",
    },
}

GENERIC_WRONG_ITEM_RESPONSE = "▶ That doesn't seem to do anything useful here."

AREAS = {
    Area.KITCHEN: {
        AreaKey.DESCRIPTION: (
            "A small, homely Kitchen with a Refrigerator in the corner and a "
            "slightly open Drawer."
        ),
        AreaKey.EXITS: {Path.NORTH: Area.LIVING_ROOM, Path.SOUTH: Area.GARDEN},
        AreaKey.EXIT_REQUIREMENTS: {
            Path.SOUTH: {
                AreaKey.ITEM: Item.GARDEN_KEY,
                AreaKey.MESSAGE: "▶ The Garden door is locked, now what?",
            }
        },
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            Object.KITCHEN_DRAWER: {
                ObjectKey.DESCRIPTION: (
                    "▶ A wooden Drawer, you can see a shiny object"
                    " reflecting light from within."
                ),
                ObjectKey.USED_DESCRIPTION: (
                    "▶ An open wooden Drawer, now empty."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You open the Drawer and find a Garden Key!"
                ),
                ObjectKey.GIVES_ITEM: Item.GARDEN_KEY,
            },
            Object.KITCHEN_FLOOR: {
                ObjectKey.DESCRIPTION: (
                    "▶ The kitchen floor is a vast expanse of polished, bone-white"
                    " ceramic tiles, laid out in a flawless grid.\n▶ Each tile "
                    "gleams under the soft overhead lighting, so spotless it "
                    "almost acts as a mirror to the polished chrome appliances.\n"
                    "▶ The grout lines are a sharp, contrasting charcoal gray, "
                    "perfectly straight and entirely free of dirt or wear."
                ),
            },
            Object.REFRIGERATOR: {
                ObjectKey.DESCRIPTION: (
                    "▶ Standing in the corner of the dim kitchen is the Chrono-"
                    "Chill 3000.\n▶ Instead of the expected mechanical hum, it "
                    "emits a slow, rhythmic tick-tock that vibrates through the "
                    "floorboards.\n▶ it doesn't use coolant; it preserves its "
                    "contents using a localized temporal statis field."
                ),
            },
        },
    },
    Area.LIVING_ROOM: {
        AreaKey.DESCRIPTION: "A cozy Living Room with a Fireplace.",
        AreaKey.POST_ASHES_DESCRIPTION: (
            "The warmth of the Fireplace has faded, the Living Room is a bit "
            "chilly now."
        ),
        AreaKey.EXITS: {Path.SOUTH: Area.KITCHEN, Path.UP: Area.ATTIC},
        AreaKey.EXIT_REQUIREMENTS: {
            Path.UP: {
                AreaKey.ITEM: Item.ATTIC_KEY,
                AreaKey.MESSAGE: "▶ The hatch to the Attic is locked tight.",
            }
        },
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            Object.FIREPLACE: {
                ObjectKey.DESCRIPTION: (
                    "▶ A simple brick Fireplace that keeps the place warm."
                ),
                ObjectKey.USED_DESCRIPTION: (
                    "▶ A Fireplace with a button under the mantle.\n▶ You "
                    "can't help but feel that you should press it."
                ),
                ObjectKey.POST_BUTTON_DESCRIPTION: (
                    "▶ A Fireplace with burning Ashes and a Button under the "
                    "mantle.\n▶ The Ashes inside are smoldering.\n▶ The Button"
                    " has already been pressed."
                ),
                ObjectKey.POST_ASHES_DESCRIPTION: (
                    "▶ A Fireplace with damp Ashes and a Button under the "
                    "mantle.\n▶ The Ashes inside are extinguished.\n▶ The "
                    "Button has already been pressed."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The Fireplace is too hot to search through safely, but "
                    "wait...\n▶ You notice a small button hidden underneath "
                    "the mantle."
                ),
                ObjectKey.REVEALS: Object.BUTTON,
            },
            Object.BUTTON: {
                ObjectKey.DESCRIPTION: (
                    "▶ A small, worn button hidden under the Fireplace mantle."
                ),
                ObjectKey.USED_DESCRIPTION: (
                    "▶ You remember pressing this Button and unlocking the "
                    "compartment beneath the Ashes."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You press it and hear a mechanical lock *click* "
                    "underneath the hot Ashes. \n▶ The mechanism has unlocked"
                    " a hidden compartment!"
                ),
                ObjectKey.REVEALS: Object.ASHES,
                ObjectKey.VISIBLE: False,
            },
            Object.ASHES: {
                ObjectKey.DESCRIPTION: (
                    "▶ Hot, smoldering ashes in the Fireplace. Do not touch!"
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.WATERING_CAN,
                ObjectKey.REQUIRES_ITEM_STATE: ItemState.FULL,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The Ashes are too dangerous to search through safely."
                ),
                ObjectKey.FAILED_STATE_RESULT: (
                    "▶ The Watering Can is empty. "
                    "\n▶ You need water to douse the Ashes."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You douse the Ashes with water.\n▶ They cool down and "
                    "you search through them safely, finding a hidden Shed "
                    "Key!"
                ),
                ObjectKey.GIVES_ITEM: Item.SHED_KEY,
                ObjectKey.CHANGES_ITEM_STATE: {
                    Item.WATERING_CAN: ItemState.EMPTY
                },
                ObjectKey.VISIBLE: False,
            },
            Object.WOODEN_TABLE: {
                ObjectKey.DESCRIPTION: (
                    "▶ It is a sturdy, low-slung coffee table crafted from "
                    "dark oak, sitting in the center of the room.\n▶ Its "
                    "surface is polished to a soft, warm sheen that catches "
                    "the amber glow of the fireplace."
                ),
                ObjectKey.POST_ASHES_DESCRIPTION: (
                    "▶ The sturdy coffee table sits in the center of the "
                    "room, its dark oak surface now dull without the "
                    "Fireplace's glow.\n▶ A faint dusting of damp ash has "
                    "settled accross it."
                ),
            },
        },
    },
    Area.GARDEN: {
        AreaKey.DESCRIPTION: (
            "A sunny Garden with a small Shed and a coiled Hose."
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
                AreaKey.MESSAGE: "▶ The Shed is locked, you shall not pass!",
            },
            Path.UP: {
                ObjectKey.CONDITION: Object.WATERED_PLANT,
                AreaKey.MESSAGE: "▶ There's no way up from here.",
            },
        },
        AreaKey.ITEMS: {Item.WATERING_CAN: "▶ An empty green Watering Can."},
        ObjectKey.INTERACTABLES: {
            Object.GARDEN_HOSE: {
                ObjectKey.DESCRIPTION: (
                    "▶ A long green Garden Hose coiled neatly near a spigot. "
                    "\n▶ The spigot is turned on and water drips from the hose"
                    " nozzle."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.WATERING_CAN,
                ObjectKey.REQUIRES_ITEM_STATE: ItemState.EMPTY,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You need a container to fill up with water."
                ),
                ObjectKey.FAILED_STATE_RESULT: (
                    "▶ The Watering Can is already full."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You fill the Watering Can with water from the "
                    "Garden Hose."
                ),
                ObjectKey.CHANGES_ITEM_STATE: {
                    Item.WATERING_CAN: ItemState.FULL
                },
            },
            Object.MAGIC_PLANT: {
                ObjectKey.DESCRIPTION: (
                    "▶ A peculiar flowering Plant in an ornate pot."
                    "\n▶ Its leaves shimmer with an otherworldly quality, as "
                    "if touched by starlight.\n▶ It looks quite thirsty."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.WATERING_CAN,
                ObjectKey.REQUIRES_ITEM_STATE: ItemState.FULL,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The Plant doesn't look like it needs anything."
                ),
                ObjectKey.FAILED_STATE_RESULT: (
                    "▶ The Watering Can is empty. The Plant looks thirsty."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You water the Magic Plant.\n▶ It glows brilliantly and "
                    "suddenly grows into an enormous beanstalk that "
                    "reaches up into the clouds!\n▶ A set of natural steps "
                    "have formed in its trunk, creating a pathway towards the "
                    "sky."
                ),
                ObjectKey.CHANGES_ITEM_STATE: {
                    Item.WATERING_CAN: ItemState.EMPTY
                },
                ObjectKey.ENABLES_EXIT: Path.UP,
                ObjectKey.VISIBLE: False,
            },
        },
    },
    Area.SHED: {
        AreaKey.DESCRIPTION: "A Shed for storing various items.",
        AreaKey.EXITS: {Path.WEST: Area.GARDEN},
        AreaKey.ITEMS: {Item.SHOVEL: "▶ A steel tool used for digging."},
        ObjectKey.INTERACTABLES: {},
    },
    Area.YARD: {
        AreaKey.DESCRIPTION: (
            "A ground of fertile green and earthy browns. Carl the Dog roams "
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
                ObjectKey.POST_X_MARK_DIG_DESCRIPTION: ("▶ "),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.SHOVEL,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You need a tool to dig with."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You dig at the X Mark with your Shovel.\n▶ After a few "
                    "minutes of digging, your Shovel hits a hard object."
                    "\n▶ You uncover a small metal box containing an ornate "
                    "Key and a well-preserved Bone!"
                ),
                ObjectKey.GIVES_ITEM: Item.ATTIC_KEY,
                ObjectKey.ALSO_GIVES: Item.BONE,
                ObjectKey.VISIBLE: False,
            },
            Object.CARL: {
                ObjectKey.DESCRIPTION: (
                    "▶ A friendly golden retriever with bright, intelligent "
                    "eyes wags his tail when he sees you."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.BONE,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ Carl looks at you expectantly and then glances "
                    "meaningfully at a spot on the ground.\n▶ He paws at the "
                    "dirt and whines softly, as if trying to get your "
                    "attention.\n▶ 'Woof!', Carl scratches at the ground in "
                    "the shape of an X..."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You give Carl the Bone and he absolutely loses his mind"
                    " with joy!\n▶ He grabs it gently in his mouth, does three"
                    " perfect spins and then drops into a play bow with his "
                    "tail wagging so hard his whole body wiggles.\n▶ 'WOOF "
                    "WOOF!' he barks happily, then settles down to contentedly"
                    "chew his new treasure.\n▶ What a good boy!"
                ),
            },
        },
    },
    Area.ATTIC: {
        AreaKey.DESCRIPTION: (
            "A dusty Attic filled with old furniture and mysterious shadows."
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
                    "that seem to swirl and clash without pattern.\n▶ The "
                    "paint is thick in some places, thin in others, creating a"
                    " chaotic yet somehow captivating mess of color.\n▶ A "
                    "small placard below simply reads 'Untitled #47.'"
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
                    "▶ A heavy metal Safe is built here into the wall."
                    "\n▶ It has a combination lock that looks quite complex."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The Safe is locked tight.\n▶ You'll need to figure out "
                    "how to unlock it."
                ),
                ObjectKey.VISIBLE: False,
            },
        },
    },
    Area.CLOUD_47: {
        AreaKey.DESCRIPTION: (
            "The moon glows bright, you stand on a Cloud high above the "
            "surface.\nThe air shimmers with ethereal energy and strange "
            "celestial music seems to emanate from the Cloud itself."
        ),
        AreaKey.EXITS: {
            Path.DOWN: Area.GARDEN,
            Path.PORTAL: Area.CHAOS_DIMENSION,
        },
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
                    "▶ A solid golden Pedestal stands here, upon further "
                    "examination, you notice a groove at the top."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ It won't budge an inch, some unknown force from a "
                    "familiar source binds it here."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ The Statue begins to pulsate and emit a low hum...\n"
                    "▶ A swirling vortex of violet and black tears open in the"
                    " air beside the Pedestal!\n"
                    "▶ A Portal to another Dimension manifests before you."
                ),
                ObjectKey.ENABLES_EXIT: Path.PORTAL,
                ObjectKey.VISIBLE: True,
            },
        },
    },
    Area.CHAOS_DIMENSION: {
        AreaKey.DESCRIPTION: (
            "An endless expanse of churning nothing stretches in every "
            "direction.\nThe chaos doesn't rage... it simply is, vast and "
            "indifferent, older than the house, older than Carl, older than "
            "the concept of Gardens, Sheds and Keys.\nWithin in it, a hidden "
            "entity watches you. It does not seem pleased."
        ),
        AreaKey.EXITS: {
            Path.DOWN: Area.THE_VOID,
            Path.NORTH: Area.CHAOS_CORE,
            Path.EAST: Area.FRACTURED_ECHO,
            Path.WEST: Area.CRIMSON_RIFT,
        },
        AreaKey.EXIT_REQUIREMENTS: {
            Path.DOWN: {
                AreaKey.CONFIRM_PROMPT: (
                    "The ground ends here - not a cliff, just a hole where "
                    "the world forgot to keep going.\nJump, and gravity "
                    "remembers your name; you will fall through colors that "
                    "don't exist yet, unmade for one long breath before "
                    "the thing puts you back together on the other side."
                ),
                AreaKey.CONFIRM_QUESTION: "▶ Jump in? (y/n): ",
                AreaKey.CONFIRM_DECLINE_MESSAGE: (
                    "▶ You step back from The Void, not quite ready."
                ),
                AreaKey.CONFIRM_SUCCESS_MESSAGE: (
                    "▶ You take a breath and jump into The Void."
                ),
            },
        },
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            # Object.
        },
    },
    Area.THE_VOID: {
        AreaKey.DESCRIPTION: ("As you fall, time stops in this moment."),
        AreaKey.EXITS: {Path.SOUTH: Area.DEAD_ROOM},
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {},
    },
    Area.DEAD_ROOM: {
        AreaKey.DESCRIPTION: ("A decrepit Dead Room with a Well Of Grief."),
        AreaKey.EXITS: {
            Path.NORTH: Area.PIGPEN,
            Path.DOWN: Area.THE_INVERSE,
        },
        AreaKey.EXIT_REQUIREMENTS: {
            Path.DOWN: {
                AreaKey.MESSAGE: "▶ The hatch to The Inverse is locked tight.",
            },
        },
        AreaKey.ITEMS: {
            Item.PAINTED_EYE: (
                "▶ The Painted Eye lies here upon a warped wooden table.\n"
            ),
        },
        ObjectKey.INTERACTABLES: {
            Object.WELL_OF_GRIEF: {
                ObjectKey.DESCRIPTION: (
                    "▶ Where the warm, brick Fireplace once stood is now a "
                    "Well Of Grief.\n▶ A stone structure built into the floor"
                    " that goes straight down into the freezing and "
                    "suffocating dark.\n▶ {name} can see a rusted steel grater"
                    " mechanism sitting over the mouth of the Well, locked in "
                    "place by heavy iron gears.\n▶ Dense, bone-white ash "
                    "slowly flows upward out of the well like dry smoke, "
                    "spilling over the edges."
                ),
                ObjectKey.HIDDEN_DESCRIPTION_ITEM: Item.PAINTED_EYE,
                ObjectKey.HIDDEN_DESCRIPTION: (
                    "▶ Through the Eye, faint letters resolve on the Grater's "
                    'rim: "The Living consumes to create warmth. The Dead '
                    'grinds to preserve the cold."'
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.VISIBLE: True,
            },
            Object.GRATER_MECHANISM: {
                ObjectKey.DESCRIPTION: (
                    "▶ Heavy, circular plates of rusted iron sit flush over "
                    "the mouth of the well, resembling a massive, "
                    "industrailized millstone.\n▶ Its surface is pitted with "
                    "concentric rings of jagged, downward-curving teeth - "
                    "sharp enough to shred stone, yet entirely clogged with a "
                    "thick crust of ancient, bone-white ash.\n▶ A rusted iron "
                    "crank projects from the side of the masonry, connected "
                    "to a sequence of oversized, square-toothed gears."
                ),
                ObjectKey.VISIBLE: False,
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: "▶ ",
            },
            Object.SKELETAL_HAND: {
                ObjectKey.DESCRIPTION: (
                    "▶ A calcified, Skeletal Hand is jammed into the gears of "
                    "the Grater Mechanism that covers the Well Of Grief."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.VIAL_OF_CORROSIVE_BILE,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ {name} isn't strong enough to pry it loose.",
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ {name} pours the contents of the Vial on top of the "
                    "Skeletal Hand.\n▶ The thick, pale green bile contracts "
                    "the calcified fingers with a sharp, cold hiss. There is "
                    "no steam, smoke or bubbling heat. Instead, a frost-like "
                    "necrosis spreads rapidly across the bone-dry skin.\n▶ "
                    "The calcified tissue doesn't melt - it shatters. Under "
                    "the corrosive weight of the bile, the stone hard grip of "
                    "the hand loses its structural integrity.\n▶ With a sound "
                    "like crackling winter ice, the fingers splinter into a "
                    "heavy, salt-like powder, cascading down into the dark "
                    "gears below."
                ),
                ObjectKey.REVEALS: Object.GRATER_MECHANISM,
            },
        },
    },
    Area.PIGPEN: {
        AreaKey.DESCRIPTION: ("TBD"),
    },
    Area.THE_INVERSE: {
        AreaKey.DESCRIPTION: ("TBD"),
    },
    Area.CHAOS_CORE: {
        AreaKey.DESCRIPTION: ("TBD"),
        AreaKey.EXITS: {},
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {},
    },
    Area.FRACTURED_ECHO: {
        AreaKey.DESCRIPTION: ("TBD"),
        AreaKey.EXITS: {},
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {},
    },
    Area.CRIMSON_RIFT: {
        AreaKey.DESCRIPTION: ("TBD"),
        AreaKey.EXITS: {},
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {},
    },
}
