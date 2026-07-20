from enums import Area, AreaKey, Item, ItemState, Object, ObjectKey, Path

ITEM_DESCRIPTIONS = {
    Item.GARDEN_KEY: (
        "▶ A small brass Key, its teeth cut with an engraver's stubborn "
        "optimism - someone believed this shape would matter to somebody, "
        "someday.\n▶ It doesn't ask what you'll unlock. Keys never do. They "
        "just wait to become obsolete the moment they succeed."
    ),
    Item.WATERING_CAN: {
        "empty": (
            "▶ A green metal Watering Can, hollow and entirely unashamed "
            "about it. Shake it and the echo comes back sounding almost like "
            "an apology.\n▶ Emptiness has its own kind of honesty - at least "
            "it isn't pretending to be useful right now."
        ),
        "full": (
            "▶ A green metal Watering Can, heavy now with intent. The water "
            "inside sloshes with the quiet confidence of something that knows "
            "exactly what it's for.\n▶ Water is wet. You knew that already. "
            "Somehow it still felt worth confirming."
        ),
    },
    Item.SHED_KEY: (
        "▶ A rusty iron Key, heavier in the hand that its size has any right "
        "to be - as if it's been carrying the weight of the word etched into "
        "it.\n▶ SHED, it says, in case you'd forgotten what waits behind small"
        ", locked things. You hadn't."
    ),
    Item.CHAIN_CUTTERS: (
        "▶ In your hand, the Cutters sit heavier than they looked on the cans"
        ", jaws parted just enough to hint at a bite.\n▶ The hinge groans "
        "stiff with rust, but it doesn't feel broken - just waiting, the same "
        "as you are."
    ),
    Item.SHOVEL: (
        "▶ The handle is worn smooth in exactly the spot your palm falls, like"
        " it was waiting for someone with your particular grip.\n▶ A thin "
        "crust of old dirt still clings to the blade, dried into whatever "
        "shape the last dig left behind."
    ),
    Item.ATTIC_KEY: (
        "▶ An ornate silver Key, scrollwork curling across its bow like it's "
        "trying to distract you from how cold the metal is.\n▶ Dug up from "
        "dirt where someone thought it best forgotten. It looks important. "
        "Things buried usually do."
    ),
    Item.BONE: (
        "▶ A well-preserved Bone, its provenance tactfully unexamined. "
        "Someone, something, once needed this - now it's yours to give away."
        "\n▶ It doesn't smell like victory or tragedy, just old marrow and the"
        " faint promise of a wagging tail."
    ),
    Item.DOG_STATUE: (
        "▶ A hand-crafted miniature Statue in the visage of Carl the Dog, "
        "carved - impossibly - from something that catches the light like "
        "moon rock.\n▶ It shouldn't exist. It does anyway. You get the sense "
        "Carl finds this less strange than you do."
    ),
    Item.UNTITLED_47: (
        "▶ An abstract painting, all bold reds, blues and greens flung "
        "together with the kind of confidence that either means genius or "
        "total indifference to the outcome.\n▶ It shouldn't exist. It does "
        "anyway. You get the sense Carl finds this less strange than you do."
    ),
    Item.PAINTED_EYE: (
        "▶ A single Painted Eye, freshly cut from a canvas and still radiating"
        " a faint, mammalian heat.\n▶ Hold it to your face and the world "
        "unpeels itself."
    ),
}

# Falls back to GENERIC_WRONG_ITEM_RESPONSE if not defined here.
WRONG_ITEM_RESPONSES = {
    Object.ASHES: {
        Item.GARDEN_KEY: (
            "▶ You hold the Garden Key over the Ashes and think better of "
            "it.\n▶ Whatever it might unlock, it won't do so as a puddle of "
            "molten brass."
        ),
    },
    Object.CARL: {
        Item.ATTIC_KEY: (
            "▶ You offer Carl the Attic Key. He doesn't so much as glance at "
            "it, gaze fixed on the clouds like they owe him something."
        ),
        Item.GARDEN_KEY: (
            "▶ Carl regards the Key with the mild disdain of a creature who "
            "has never once been locked out of anywhere.\n▶ Keys, locks, "
            "confinement - none of it means anything to him."
        ),
        Item.SHED_KEY: (
            "▶ Carl regards the Key with the mild disdain of a creature who "
            "has never once been locked out of anywhere.\n▶ Keys, locks, "
            "confinement - none of it means anything to him."
        ),
        Item.SHOVEL: (
            "▶ You raise the Shovel toward Carl and stop yourself just in "
            "time.\n▶ Some decisions can't be dug back out of."
        ),
        Item.WATERING_CAN: (
            "▶ You tip the Can toward Carl, but thirst was never the "
            "problem.\n▶ Whatever hunger sits behind those eyes, water won't "
            "touch it."
        ),
    },
    Object.GARDEN_HOSE: {
        Item.ATTIC_KEY: (
            "▶ The Garden Hose isn't locked. The Attic, somewhere far above "
            "you, very much is."
        ),
        Item.BONE: (
            "▶ You hold the Bone under the Hose. It gets wet. Nothing about "
            "it improves."
        ),
        Item.GARDEN_KEY: (
            "▶ You try the Key against the Hose anyway. It has nothing "
            "resembling a lock, and never did."
        ),
        Item.SHED_KEY: (
            "▶ Wrong door. The Shed Key belongs to the Shed - try it there "
            "instead."
        ),
        Item.SHOVEL: (
            "▶ You raise the Shovel toward the Hose and reconsider - it's the "
            "only thing standing between you and precious water."
        ),
        Item.UNTITLED_47: (
            "▶ You bring the painting near the running water and something "
            "in you rebels.\n▶ Some things weren't built to survive contact "
            "with anything, least of all this."
        ),
    },
    Object.MAGIC_PLANT: {
        Item.ATTIC_KEY: (
            "▶ You try the Key against the Plant's stem, aware even as you "
            "do it that a plant has never once had a lock."
        ),
        Item.BONE: (
            "▶ You swing the Bone at the Plant and it goes still in the "
            "air, caught by some old, ancient magic that refuses to let the "
            "blow land."
        ),
        Item.GARDEN_KEY: (
            "▶ You try the Key against the Plant's stem, aware even as you "
            "do it that a plant has never once had a lock."
        ),
        Item.SHED_KEY: (
            "▶ You try the Key against the Plant's stem, aware even as you "
            "do it that a plant has never once had a lock."
        ),
        Item.SHOVEL: (
            "▶ The Plant flares to life the moment the Shovel bites toward "
            "its roots, a shimmering barrier blooming out of nowhere to meet "
            "the blade.\n▶ Whatever protects it, it isn't interested in "
            "being dug up."
        ),
        Item.UNTITLED_47: (
            "▶ The Plant catches sight of the painting and glows a soft, "
            "startled luminescence, leaning toward it like something "
            "recognized.\n▶ Whatever this reaction means, the painting feels "
            "too important to let go of yet."
        ),
    },
    Object.PEDESTAL: {
        Item.ATTIC_KEY: (
            "▶ You look for a keyhole on the Pedestal and find only smooth, "
            "unbroken gold. There was never anything here to unlock."
        ),
        Item.BONE: "▶ You press the Bone into the groove. It doesn't fit, "
        "and never looks like it was going to.",
        Item.GARDEN_KEY: (
            "▶ You look for a keyhole on the Pedestal and find only smooth, "
            "unbroken gold. There was never anything here to unlock."
        ),
        Item.SHED_KEY: (
            "▶ You look for a keyhole on the Pedestal and find only smooth, "
            "unbroken gold. There was never anything here to unlock."
        ),
        Item.SHOVEL: (
            "▶ The Shovel skids uselessly off the Pedestal's surface, not "
            "so much as scratching it.\n▶ Radiant gold, it turns out, "
            "doesn't dig."
        ),
        Item.UNTITLED_47: (
            "▶ You try to press the painting into the groove. Canvas was "
            "never going to fit where something else was meant to sit."
        ),
    },
    Object.X_MARK: {
        Item.GARDEN_KEY: (
            "▶ You crouch and try the Key against the dirt anyway.\n▶ It's "
            "just ground. Ground has never once had a lock."
        ),
        Item.SHED_KEY: (
            "▶ You crouch and try the Key against the dirt anyway.\n▶ It's "
            "just ground. Ground has never once had a lock."
        ),
        Item.WATERING_CAN: (
            "▶ You tip the Can over the mark and nothing about the ground "
            "asked to be watered."
        ),
        Item.UNTITLED_47: (
            "▶ You hold the painting over the mark, considering leaving it "
            "there, and think better of littering something this strange in "
            "the dirt."
        ),
    },
}

GENERIC_WRONG_ITEM_RESPONSE = (
    "▶ Nothing happens - whatever you had in mind, this isn't the thing it "
    "works on."
)

AREAS = {
    Area.KITCHEN: {
        AreaKey.DESCRIPTION: (
            "A small Kitchen that used to feel homely. A Refrigerator ticks "
            "quietly in the corner, and a Wooden Drawer sits slightly ajar, "
            "its brass handle catching what little light finds its way in."
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
                    "▶ A weathered wooden Drawer built into the counter, its "
                    "brass handle tarnished with age.\n▶ It hangs slightly "
                    "ajar, and something metallic within catches the light and"
                    " throws it back at you."
                ),
                ObjectKey.USED_DESCRIPTION: (
                    "▶ The wooden Drawer sits open and empty, its brass handle"
                    " still slightly warm from your grip.\n▶ Dust motes drift "
                    "lazily through the space where the Key used to gleam."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You slide the Drawer open with a soft wooden groan.\n▶ "
                    "Nestled among old receipts and loose string, a Garden Key"
                    " gleams back at you!"
                ),
                ObjectKey.GIVES_ITEM: Item.GARDEN_KEY,
            },
            Object.KITCHEN_FLOOR: {
                ObjectKey.DESCRIPTION: (
                    "▶ The Kitchen Floor is a vast expanse of polished, "
                    "bone-white ceramic tiles, laid out in a flawless grid.\n▶"
                    " Each tile gleams under the soft overhead lighting, so "
                    "spotless it almost acts as a mirror to the polished "
                    "chrome appliances.\n▶ The grout lines are a sharp, "
                    "contrasting charcoal gray, perfectly straight and "
                    "entirely free of dirt or wear."
                ),
            },
            Object.REFRIGERATOR: {
                ObjectKey.DESCRIPTION: (
                    "▶ Standing in the corner of the dim Kitchen is the "
                    "Chrono-Chill 3000.\n▶ Instead of the expected mechanical "
                    "hum, it emits a slow, rhythmic tick-tock that vibrates "
                    "through the floorboards.\n▶ It doesn't use coolant; it "
                    "preserves its contents using a localized temporal "
                    "statis field."
                ),
            },
        },
    },
    Area.LIVING_ROOM: {
        AreaKey.DESCRIPTION: (
            "A Living Room that's trying hard to be cozy. A brick "
            "Fireplace crackles in the corner, its glow spilling warm "
            "across a low wooden table."
        ),
        AreaKey.ASHES_EXTINGUISHED: (
            "The Fireplace has gone quiet, its warmth spent. Without it, "
            "the Living Room feels a little colder, a little emptier than "
            "before."
        ),
        AreaKey.EXITS: {Path.SOUTH: Area.KITCHEN, Path.UP: Area.ATTIC},
        AreaKey.EXIT_REQUIREMENTS: {
            Path.UP: {
                AreaKey.ITEM: Item.ATTIC_KEY,
                AreaKey.MESSAGE: (
                    "▶ The hatch to the Attic sits flush in the ceiling, "
                    "sealed by a lock that has no intention of hearing your "
                    "case."
                ),
            }
        },
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            Object.FIREPLACE: {
                ObjectKey.DESCRIPTION: (
                    "▶ A brick Fireplace crackles quietly, its flames dancing "
                    "gold and amber against soot-blackened stone.\n▶ Warmth "
                    "pours from the hearth in slow, steady waves and the "
                    "mantle above bears the smooth wear of years spent close "
                    "to the fire."
                ),
                ObjectKey.USED_DESCRIPTION: (
                    "▶ The Fireplace still crackles behind its brick facade, "
                    "but now a small, worn button catches your eye, tucked "
                    "just beneath the mantle.\n▶ Something about it pulls at "
                    "you - you can't shake the feeling that you should press "
                    "it."
                ),
                ObjectKey.BUTTON_PRESSED: (
                    "▶ The Fireplace's flames have died down to a bed of "
                    "smoldering Ashes, the Button beneath the mantle sitting "
                    "still and spent.\n▶ Heat still radiates faintly from the "
                    "coals and a thin curl of smoke drifts up where the fire "
                    "once roared.\n▶ You've already pressed the Button - the "
                    "mechanism has done its work."
                ),
                ObjectKey.ASHES_EXTINGUISHED: (
                    "▶ The Fireplace stands cold now, its Ashes damp and gray "
                    "where the Watering Can's water settled over them.\n▶ The "
                    "Button beneath the mantle rests dark and still, its work "
                    "long finished.\n▶ Only the faint, wet smell of "
                    "extinguished embers lingers in the brick."
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
                    "▶ A small, worn button hidden under the Fireplace mantle,"
                    " its brass surface dulled and pitted from years of heat."
                    "\n▶ It sits flush with the stone, but a faint give "
                    "beneath your fingertip tells you it still has one press "
                    "left in it."
                ),
                ObjectKey.USED_DESCRIPTION: (
                    "▶ The button rests still and spent beneath the mantle, "
                    "its spring long since given out.\n▶ You remember the "
                    "mechanical *click* that answered from deep in the hearth"
                    " when you pressed it, unlocking the compartment beneath "
                    "the Ashes."
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
                    "▶ Hot, smoldering ashes fill the base of the Fireplace, "
                    "embers pulsing dull orange beneath a shifting layer of "
                    "gray.\n▶ Heat rolls off them in visible waves - close "
                    "enough to sift through, but not without paying for it."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.WATERING_CAN,
                ObjectKey.REQUIRES_ITEM_STATE: ItemState.FULL,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You reach toward the Ashes, but the heat pushes back "
                    "before your fingers get close.\n▶ Whatever's buried in "
                    "there will have to wait until it cools."
                ),
                ObjectKey.FAILED_STATE_RESULT: (
                    "▶ The Watering Can is empty and rattles uselessly in your"
                    " hand.\n▶ You need water to douse the Ashes before you "
                    "can search them safely."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You tip the Watering Can and a rush of water hisses "
                    "against the coals, sending up a curtain of steam.\n▶ The "
                    "Ashes collapse into a cool, sodden heap, and buried "
                    "within them you find a hidden Shed Key!"
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
                ObjectKey.ASHES_EXTINGUISHED: (
                    "▶ The sturdy coffee table sits in the center of the "
                    "room, its dark oak surface now dull without the "
                    "Fireplace's glow.\n▶ A faint dusting of damp ash has "
                    "settled across it."
                ),
            },
        },
    },
    Area.GARDEN: {
        AreaKey.DESCRIPTION: (
            "A sunny Garden, hedges overgrown just enough to notice. A "
            "weathered Shed sits shut at the far end, and a coiled Hose drips"
            " a slow, steady rhythm beside the spigot."
        ),
        AreaKey.MAGIC_PLANT_REVEALED: (
            "A sunny Garden, hedges overgrown just enough to notice. A "
            "weathered Shed sits shut at the far end, and a coiled Hose drips"
            " a slow rhythm beside a Plant that shimmers like it isn't quite "
            "finished growing."
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
                AreaKey.MESSAGE: (
                    "▶ The Shed door holds fast behind a heavy padlock, "
                    "entirely indifferent to your dramatic declarations "
                    "of passage."
                ),
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
                    "▶ A long green Garden Hose lies coiled in loose rings "
                    "beside a rusted brass spigot.\n▶ The valve sits half open"
                    ", and a steady drip taps out a slow rhythm against the "
                    "nozzle, catching the sunlight in small silver beads."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.WATERING_CAN,
                ObjectKey.REQUIRES_ITEM_STATE: ItemState.EMPTY,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ Water taps steadily against the nozzle, but your hands "
                    "alone can't hold it.\n▶ You'll need a container to catch "
                    "what the Hose is offering."
                ),
                ObjectKey.FAILED_STATE_RESULT: (
                    "▶ The Watering Can already sloshes with water, full to "
                    "the brim.\n▶ There's no room left for more."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You press the nozzle into the Watering Can and the "
                    "Hose surges to life, filling it in a rush of cool water."
                    "\n▶ Droplets spatter across your hands and the can grows "
                    "pleasantly heavy in your grip."
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
                    "▶ The Plant's shimmering leaves droop slightly, unmoved "
                    "by whatever you're holding - it isn't what it desires."
                ),
                ObjectKey.FAILED_STATE_RESULT: (
                    "▶ The Watering Can rattles empty in your hand while the "
                    "Plant's leaves curl inward, still waiting for water it "
                    "isn't getting."
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
        AreaKey.DESCRIPTION: (
            "A cramped Shed, its walls lined with sagging shelves and the "
            "mingled smell of motor oil and turned earth.\nHalf-used cans of "
            "Civic Duty Semi-Gloss sit stacked in the corner, gathering the "
            "kind of dust that means nobody's needed any of this - until now."
            "\nEverything in here has been waiting for something. You get the "
            "feeling it might be you."
        ),
        AreaKey.EXITS: {Path.WEST: Area.GARDEN},
        AreaKey.ITEMS: {
            Item.CHAIN_CUTTERS: (
                "▶ A pair of Chain Cutters, heavy-handled and freckled with "
                "rust, sits forgotten atop a stack of Civic Duty Semi-Gloss "
                "paint cans.\n▶ They were built for exactly one purpose: to "
                "open something that very badly wants to stay closed.\n▶ You "
                "don't know what that is yet. The Cutters, for their part, "
                "are in no hurry to tell you."
            ),
            Item.SHOVEL: (
                "▶ A shovel leans against the wall, its steel head dulled by "
                "years of quiet, unglamorous labor.\n▶ It has no opinion on "
                "what's buried out there, or why you need to know so badly. It"
                " just digs. That part - the *needing* - is entirely yours."
            ),
        },
        ObjectKey.INTERACTABLES: {},
    },
    Area.YARD: {
        AreaKey.DESCRIPTION: (
            "A ground of fertile green and earthy browns. Carl the Dog roams "
            "here, outside the bounds of time and space."
        ),
        AreaKey.DOG_STATUE_TAKEN: (
            "A ground of fertile green and earthy browns."
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
                ObjectKey.X_MARK_DUG: (
                    "▶ A shallow hole sits where the X used to be, a small "
                    "metal box resting open and empty beside it.\n▶ Whatever "
                    "this spot was hiding, it's already given it up."
                ),
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
                    "eyes, he wags his tail rapidly when he sees you."
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
                    " chews his new treasure.\n▶ What a good boy!"
                ),
                ObjectKey.CONSUMES_ITEM: True,
                ObjectKey.CONSUME_MESSAGE: "gave Carl the",
            },
        },
    },
    Area.ATTIC: {
        AreaKey.DESCRIPTION: (
            "A dusty Attic, thick with the particular quiet of a room nobody "
            "visits anymore. Old furniture huddles under drop cloths, and a "
            "Painting hangs slightly askew on the far wall, as if something "
            "behind it wants out."
        ),
        AreaKey.UNTITLED_47_TAKEN: (
            "A dusty Attic, thick with the particular quiet of a room nobody "
            "visits anymore. Old furniture huddles under drop cloths, and "
            "where the Painting used to hang, a heavy metal safe sits bolted "
            "into the wall, the number 47 etched plainly into its face."
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
                ObjectKey.CONSUMES_ITEM: True,
                ObjectKey.CONSUME_MESSAGE: "placed the",
                ObjectKey.CONSUME_SUFFIX: " on the Pedestal",
            },
        },
    },
    Area.CHAOS_DIMENSION: {
        AreaKey.DESCRIPTION: (
            "An endless expanse of churning nothing stretches in every "
            "direction.\nThe chaos doesn't rage... it simply is, vast and "
            "indifferent, older than the house, older than Carl, older than "
            "the concept of Gardens, Sheds and Keys.\nWithin it, a hidden "
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
                    "forgets your name; you will fall through colors that "
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
            Path.NORTH: {
                ObjectKey.CONDITION: Object.CHAOS_CORE_UNLOCKED,
                AreaKey.MESSAGE: (
                    "▶ The way North dissolves before you can take a step. "
                    "Not yet."
                ),
            },
            Path.EAST: {
                ObjectKey.CONDITION: Object.FRACTURED_ECHO_UNLOCKED,
                AreaKey.MESSAGE: (
                    "▶ The East holds together for a moment, then unravels "
                    "back into churn. Not yet."
                ),
            },
            Path.WEST: {
                ObjectKey.CONDITION: Object.CRIMSON_RIFT_UNLOCKED,
                AreaKey.MESSAGE: (
                    "▶ Something to the West refuses to let you near. Not yet."
                ),
            },
        },
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {
            # Object.
        },
    },
    Area.THE_VOID: {
        AreaKey.DESCRIPTION: (
            "Time doesn't pass here so much as it holds its breath. You fall "
            "through nothing at all, and something in the dark seems to be "
            "waiting to hear who you are before it lets go."
        ),
        AreaKey.EXITS: {Path.DOWN: Area.DEAD_ROOM},
        AreaKey.ITEMS: {},
        ObjectKey.INTERACTABLES: {},
    },
    Area.DEAD_ROOM: {
        AreaKey.DESCRIPTION: (
            "A decrepit Dead Room, the air gone thin and cold. Where warmth "
            "should be, a Well Of Grief sinks into the floor, sealed shut by "
            "a rusted iron mechanism that hasn't turned in a long, long time."
        ),
        AreaKey.EXITS: {
            Path.NORTH: Area.PIGPEN,
            Path.DOWN: Area.BASEMENT_ALT,
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
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The Grater Mechanism seals the mouth of the Well shut, "
                    "its iron gears frozen in place by the calcified hand "
                    "still jammed within them.\n▶ {name} can't force it - not"
                    " by hand, not by will. Whatever holds those gears still "
                    "has a grip."
                ),
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
                ObjectKey.INTERACTION_RESULT: (
                    "▶ With the hand gone, the Grater's crank turns freely, "
                    "grinding the last of the ash-crust away with a dry, "
                    "metallic shriek.\n▶ The teeth beneath are bare now, "
                    "hungry and clearly built to consume something more than "
                    "air."
                ),
            },
            Object.SKELETAL_HAND: {
                ObjectKey.DESCRIPTION: (
                    "▶ A calcified, Skeletal Hand is jammed into the gears of "
                    "the Grater Mechanism that covers the Well Of Grief."
                ),
                ObjectKey.HIDDEN_DESCRIPTION_ITEM: Item.PAINTED_EYE,
                ObjectKey.HIDDEN_DESCRIPTION: (
                    "▶ Through the Painted Eye, the calcified knuckles seem to"
                    ' refrain: "What warmth cannot melt, cold need not fight -'
                    ' it need only remember what the body forgot: to rot."'
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_ITEM: Item.VIAL_OF_CORROSIVE_BILE,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ {name} isn't strong enough to pry it loose."
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
            Object.WARPED_TABLE: {
                ObjectKey.DESCRIPTION: (
                    "▶ A low, Warped Table squats in the center of the room, "
                    "its grain twisted like it tried to grow away from itself "
                    "and only managed to buckle.\n▶ No warmth reaches this "
                    "surface - no glow, no sheen, just the cold, flat color "
                    "of something left in the dark long enough to forget it "
                    "was ever a tree. A Painted Eye rests atop it, watching "
                    "you back."
                ),
                ObjectKey.PAINTED_EYE_TAKEN: (
                    "▶ A low, Warped Table squats in the center of the room, "
                    "its grain twisted like it tried to grow away from itself "
                    "and only managed to buckle.\n▶ No warmth reaches this "
                    "surface - no glow, no sheen, just the cold, flat color "
                    "of something left in the dark long enough to forget it "
                    "was ever a tree. Whatever watched you from its surface is"
                    " gone now."
                ),
                ObjectKey.HIDDEN_DESCRIPTION_ITEM: Item.PAINTED_EYE,
                ObjectKey.HIDDEN_DESCRIPTION: (
                    "▶ Through the Painted Eye, the table's warp isn't wood "
                    "bending - it's wood remembering a shape it hasn't taken "
                    "yet. Faint outlines flex accross the surface, almost like"
                    " fingers, almost like a face, pressing outward from the "
                    "inside of the grain."
                ),
            },
        },
    },
    Area.PIGPEN: {
        AreaKey.DESCRIPTION: (
            "A filthy Pigpen, the air thick with rot and something wetter than"
            " mud. A cracked Feeding Trough leans against the wall, and "
            "somewhere in the muck, something that used to be a Pig watches "
            "you back."
        ),
        AreaKey.EXITS: {
            Path.NORTH: Area.WASTELAND,
            Path.SOUTH: Area.DEAD_ROOM,
        },
        ObjectKey.INTERACTABLES: {
            Object.FEEDING_TROUGH: {
                ObjectKey.DESCRIPTION: (
                    "▶ Collapsed against the cracked tile wall is the Feeding "
                    "Trough.\n▶ Instead of the mechanical ticking of a "
                    "temporal field, it emits a wet, rhythmic bubbling that "
                    "vibrates through the mud underfoot.\n▶ It doesn't "
                    "preserve its contents; it sits in a state of rapid, "
                    "perpetual decay, liquefying whatever is thrown into its "
                    "pulsing gelatinous sludge."
                ),
                ObjectKey.REQUIRES_ITEM: Item.SOME_FOOD,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ You need something worth feeding it before it'll pay "
                    "you any mind."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You tip the food into the Trough. The sludge inside "
                    "swallows it almost instantly, the Pig shuffles over, "
                    "snuffling contentedly at the mess."
                ),
                ObjectKey.CONSUMES_ITEM: True,
                ObjectKey.CONSUME_MESSAGE: "fed the",
                ObjectKey.CONSUME_SUFFIX: " to the Pig",
            },
            Object.GUTTER_MEAT: {
                ObjectKey.DESCRIPTION: (
                    "▶ Half-submerged in the muck, a Pig watches you with damp"
                    ", glassy eyes, grotesquely swollen along one flank.\n▶ "
                    "loose strips of something meat-like hang off it, wet and "
                    "translucent, twitching faintly even though nothing here "
                    "has any business still moving.\n▶ It doesn't flinch when "
                    "you get close. It just chews, slow and endless, on "
                    "something that used to have a shape."
                ),
                ObjectKey.CAN_INTERACT: True,
                ObjectKey.REQUIRES_OBJECT_USED: Object.FEEDING_TROUGH,
                ObjectKey.REQUIRES_OBJECT_USED_MESSAGE: (
                    "▶ The Pig backs away into the mud, still starving and "
                    "unwilling to let anything near it."
                ),
                ObjectKey.REQUIRES_ITEM: Item.EMPTY_VIAL,
                ObjectKey.INTERACTION_RESULT: (
                    "▶ The Pig is fed and docile now, but you have nothing on "
                    "hand to collect anything with."
                ),
                ObjectKey.SUCCESS_RESULT: (
                    "▶ You press the Empty Vial against the weeping flank and "
                    "it fills, thick and pale green, sealing itself shut the "
                    "moment it's full.\n▶ The Pig doesn't react at all."
                ),
                ObjectKey.GIVES_ITEM: Item.VIAL_OF_CORROSIVE_BILE,
                ObjectKey.CONSUMES_ITEM: True,
                ObjectKey.CONSUME_MESSAGE: "used the",
                ObjectKey.CONSUME_SUFFIX: " on the Pig",
            },
            Object.PIGPEN_FLOOR: {
                ObjectKey.DESCRIPTION: (
                    "▶ The Muddy Floor is a vast expanse of wet, black mud, "
                    "shifting in a chaotic, uneven sludge.\n▶ Each patch pools"
                    " under the dim, low-hanging light, so swallowed by filth "
                    "it almost acts as a grave to the buried, contrasting "
                    "bone-white, perfectly broken and entirely choked with "
                    "rot and hair."
                ),
            },
        },
    },
    Area.WASTELAND: {},
    Area.BASEMENT_ALT: {
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
