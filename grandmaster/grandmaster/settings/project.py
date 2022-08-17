# Custom settings

GROUPS = {
    "Administrator": {
        "news": ["add", "delete", "change"],
        "video": ["add", "delete", "change"],
    },
    "Moderator": {
        "news": ["add", "delete", "change"],
        "video": ["add", "delete", "change"],
    },
    "Student": {
        "news": ["view"],
    },
    "Parent": {
        "news": ["view"],
    },
    "Trainer": {
        "news": ["view"],
        "sport group": ["add", "delete", "change"],
    },
}
