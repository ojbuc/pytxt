ITEM_DEFINITIONS = {
    "garden key": (
        "▶ A small brass key with intricate engravings. "
        "\n▶ It looks like it might unlock a garden door."
    ),
    "watering can": {
        "empty": (
            "▶ A green metal watering can that's completely empty. "
            "\n▶ You can hear it echo when you shake it."
        ),
        "full": (
            "▶ A green metal watering can, full of water. "
            "\n▶ The water sloshes gently when you move it. Water is wet."
        ),
    },
    "shed key": (
        "▶ A rusty iron key that feels heavy in your hand. "
        "\n▶ It has the word 'SHED' etched into it."
    ),
    "shovel": (
        "▶ A sturdy steel shovel with a wooden handle. "
        "\n▶ Perfect for digging in dirt and uncovering buried secrets."
    ),
    "attic key": (
        "▶ An ornate silver key with scrollwork. "
        "\n▶ It looks like it belongs to something important."
    ),
    "bone": (
        "▶ A well-preserved dog bone, ideally sized for a friendly canine "
        "companion."
    ),
    "dog statue": (
        "▶ A hand crafted miniature statue, in the visage of Carl the dog."
        "\n▶ It appears to be made of moon rock, how does that work?"
    ),
    "untitled #47": (
        "▶ An abstract painting with bold reds, blues and greens. "
        "\n▶ The chaotic swirls of color are oddly mesmerizing."
    ),
    "magic plant": (
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
    "kitchen": {
        "description": "A small kitchen with a slightly open drawer.",
        "exits": {"north": "living room", "south": "garden"},
        "exit_requirements": {
            "south": {
                "item": "garden key",
                "message": "▶ The garden door is locked, now what?",
            }
        },
        "items": {},
        "interactables": {
            "kitchen drawer": {
                "description": (
                    "▶ A wooden drawer, you can see a shiny object"
                    " reflecting light from within."
                ),
                "used_description": (
                    "▶ An open wooden drawer, now empty."
                ),
                "can_interact": True,
                "interaction_result": (
                    "▶ You open the drawer and find a garden key!"
                ),
                "gives_item": "garden key",
                "used": False,
            }
        },
    },
    "living room": {
        "description": "A cozy living room with a fireplace.",
        "exits": {"south": "kitchen", "up": "attic"},
        "exit_requirements": {
            "up": {
                "item": "attic key",
                "message": "▶ The hatch to the attic is locked tight.",
            }
        },
        "items": {},
        "interactables": {
            "fireplace": {
                "description": (
                    "▶ A simple brick fireplace that keeps the place warm."
                    ),
                "used_description": (
                    "▶ A fireplace with a button under the mantle.\n▶ You "
                    "can't help but feel that you should press it."
                ),
                "post_button_description": (
                    "▶ A fireplace with burning ashes and a button under the "
                    "mantle.\n▶ The ashes inside are smoldering.\n▶ The button"
                    " has already been pressed."
                    ),
                "post_ashes_description": (
                    "▶ A fireplace with damp ashes and a button under the "
                    "mantle.\n▶ The ashes inside are extinguisehd.\n▶ The "
                    "button has already been pressed."
                    ),
                "can_interact": True,
                "interaction_result": (
                    "▶ The fireplace is too hot to search through safely, but "
                    "wait...\n▶ You notice a small button hidden underneath "
                    "the mantle."
                ),
                "reveals": "button",
                "used": False,
            },
            "button": {
                "description": (
                    "▶ A small, worn button hidden under the fireplace mantle."
                ),
                "used_description": (
                    "▶ You remember pressing this button and unlocking the "
                    "compartment beneath the ashes."
                    ),
                "can_interact": True,
                "interaction_result": (
                    "▶ You press it and hear a mechanical lock *click* "
                    "underneath the hot ashes. \n▶ The mechanism has unlocked"
                    " something!"
                ),
                "reveals": "ashes",
                "visible": False,
                "used": False,
            },
            "ashes": {
                "description": (
                    "▶ Hot, smoldering ashes in the fireplace. Do not touch!"
                ),
                "can_interact": True,
                "requires_item": "watering can",
                "requires_item_state": "full",
                "interaction_result": (
                    "▶ The ashes are too dangerous to search through safely."
                ),
                "failed_state_result": (
                    "▶ The watering can is empty. "
                    "\n▶ You need water to douse the ashes."
                ),
                "success_result": (
                    "▶ You douse the ashes with water.\n▶ They cool down and "
                    "you search through them safely, finding a hidden shed "
                    "key!"
                ),
                "gives_item": "shed key",
                "changes_item_state": {"watering can": "empty"},
                "visible": False,
                "used": False,
            },
        },
    },
    "garden": {
        "description": "A sunny garden with a small shed and a coiled hose.",
        "exits": {
            "north": "kitchen",
            "east": "shed",
            "west": "yard",
            "up": "cloud 47",
        },
        "exit_requirements": {
            "east": {
                "item": "shed key",
                "message": "▶ The shed is locked, you shall not pass!"
            },
            "up": {
                "condition": "watered_plant",
                "message": "▶ There's no way up from here.",
            },
        },
        "items": {"watering can": "▶ An empty green watering can."},
        "interactables": {
            "garden hose": {
                "description": (
                    "▶ A long green garden hose coiled neatly near a spigot. "
                    "\n▶ The spigot is turned on and water drips from the hose"
                    " nozzle."
                ),
                "can_interact": True,
                "requires_item": "watering can",
                "interaction_result": (
                    "▶ You need something to fill up with water."
                ),
                "success_result": (
                    "▶ You fill the watering can with water from the "
                    "garden hose."
                ),
                "changes_item_state": {"watering can": "full"},
                "used": False,
            },
            "magic plant": {
                "description": (
                    "▶ A peculiar flowering plant in an ornate pot."
                    "\n▶ Its leaves shimmer with an otherworldly quality, as "
                    "if touched by starlight.\n▶ It looks quite thirsty."
                ),
                "can_interact": True,
                "requires_item": "watering can",
                "requires_item_state": "full",
                "interaction_result": (
                    "▶ The plant doesn't look like it needs anything."
                ),
                "failed_state_result": (
                    "▶ The watering can is empty. The plant looks thirsty."
                ),
                "success_result": (
                    "▶ You water the magic plant.\n▶ It glows brilliantly and "
                    "suddenly grows into an enormous beanstalk that "
                    "reaches up into the clouds!\n▶ A set of natural steps have"
                    " formed in its trunk, creating a pathway to the sky."
                ),
                "changes_item_state": {"watering can": "empty"},
                "enables_exit": "up",
                "visible": False,
                "used": False,
            },
        },
    },
    "shed": {
        "description": "▶ A shed for storing various items.",
        "exits": {"west": "garden"},
        "items": {"shovel": "▶ A steel tool used for digging."},
        "interactables": {},
    },
    "yard": {
        "description": (
            "A ground of fertile green and earthy browns. Carl the dog roams "
            "here, outside the bounds of time and space."
        ),
        "exits": {"east": "garden"},
        "items": {},
        "interactables": {
            "x mark": {
                "description": (
                    "▶ A suspicious X carved into the dirt.\n▶ Someone has "
                    "clearly marked this spot for a reason.\n▶ The dirt looks "
                    "like it has been disturbed recently."
                ),
                "can_interact": True,
                "requires_item": "shovel",
                "interaction_result": "▶ You need something to dig with.",
                "success_result": (
                    "▶ You dig at the X mark with your shovel.\n▶ After a few "
                    "minutes of digging, your shovel hits something hard."
                    "\n▶ You uncover a small metal box containing an ornate "
                    "attic key and a well-preserved dog bone!"
                ),
                "gives_item": "attic key",
                "also_gives": "bone",
                "visible": False,
                "used": False,
            },
            "carl": {
                "description": (
                    "▶ A friendly golden retriever with bright, intelligent "
                    "eyes wags his tail when he sees you.\n▶ It seems he's "
                    "trying to tell you something important."
                ),
                "can_interact": True,
                "requires_item": "bone",
                "interaction_result": (
                    "▶ Carl looks at you expectantly and then glances "
                    "meaningfully at a spot on the ground.\n▶ He paws at the "
                    "dirt and whines softly, as if trying to show you "
                    "something.\n▶ 'Woof!', Carl scratches at the ground in "
                    "the shape of an X..."
                ),
                "success_result": (
                    "▶ You give Carl the bone and he absolutely loses his mind "
                    "with joy!\n▶ He grabs it gently in his mouth, does three "
                    "perfect spins and then drops into a play bow with his tail"
                    " wagging so hard his whole body wiggles.\n▶ 'WOOF WOOF!' "
                    " he barks happily, then settles down to contentedly chew"
                    " his new treasure.\n▶ What a good boy!"
                ),
                "used": False,
            },
        },
    },
    "attic": {
        "description": (
            "A dusty attic filled with old furniture and mysterious shadows."
        ),
        "exits": {"down": "living room"},
        "items": {
            "dog statue": (
                "▶ An oddly familiar looking craft that requires "
                "further inspection."
            ),
        },
        "interactables": {
            "loose painting": {
                "description": (
                    "▶ A loose abstract painting hangs askew on the wall."
                    "\n▶ Its canvas splashed with bold reds, blues and greens "
                    "that seem to swirl and clash without pattern.\n▶ The paint"
                    " is thick in some places, thin in others, creating a "
                    "chaotic yet somehow captivating mess of color.\n▶ A small "
                    "placard below simply reads 'Untitled #47.'"
                ),
                "can_interact": True,
                "interaction_result": (
                    "▶ You carefully remove the painting from the wall. "
                    "\n▶ Behind, you discover a sturdy safe bolted into the "
                    "wall with the number 47 etched prominently on its front. "
                    "\n▶ The painting is light enough to carry with you."
                ),
                "reveals": "safe",
                "becomes_item": "untitled #47",
                "used": False,
            },
            "safe": {
                "description": (
                    "▶ A heavy metal safe is built here into the wall."
                    "\n▶ It has a combination lock that looks quite complex."
                ),
                "can_interact": True,
                "interaction_result": (
                    "▶ The safe is locked tight.\n▶ You'll need to figure out "
                    "how to unlock it."
                ),
                "visible": False,
                "used": False,
            },
        },
    },
    "cloud 47": {
        "description": (
            "The moon glows bright, you stand on a cloud high above the surface"
            ".\n  The air shimmers with ethereal energy and strange celestial "
            "music seems to emanate from the cloud itself."
        ),
        "exits": {"down": "garden", "portal": "chaos dimension"},
        "exit_requirements": {
            "portal": {
                "condition": "statue_placed",
                "message": "▶ There's nothing here but thin air.",
            }
        },
        "items": {},
        "interactables": {
            "pedestal": {
                "requires_item": "dog statue",
                "description": (
                    "▶ A solid golden pedestal stands here, upon further "
                    "examination, you notice a groove at the top.\n▶ Perhaps "
                    "you could place an item there?"
                ),
                "can_interact": True,
                "interaction_result": (
                    "▶ It won't budge an inch, some unknown force from a "
                    "familiar source binds it here."
                ),
                "success_result": (
                    "▶ The statue begins to pulsate and emit a low hum...\n"
                    "▶ A swirling vortex of violet and black tears open in the"
                    " air beside the pedestal!\n"
                    "▶ A portal to another dimension manifests before you."
                ),
                "enables_exit": "portal",
                "visible": True,
                "used": False,
            },
        },
    },
    "chaos dimension": {
        "description": (),
        "exits": {},
        "items": {},
        "interactables": {},
    },
}
