from model import Account

schema = schema = {
    "type": "object",
    "properties": {
        "form": {"type": "string", "minLength": 6, "maxLength": 16},
        "to": {"type": "string", "minLength": 6, "maxLength": 16},
        "text": {"type": "string", "minLength": 1, "maxLength": 120},
    },
    "required": ["form", "to"]
}

