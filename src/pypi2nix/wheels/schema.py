URL_SCHEMA = {
    "type": "object",
    "properties": {
        "sha256": {"type": "string"},
        "url": {"type": "string"},
        "__type__": {"const": "fetchurl",},
    },
    "required": ["sha256", "url", "__type__"],
}

GIT_SCHEMA = {
    "type": "object",
    "properties": {
        "sha256": {"type": "string"},
        "url": {"type": "string"},
        "rev": {"type": "string"},
        "__type__": {"const": "fetchgit"},
    },
    "required": ["sha256", "url", "rev", "__type__"],
}

INDEX_ITEM_SCHEMA = {"anyOf": [URL_SCHEMA, GIT_SCHEMA,]}

INDEX_SCHEMA = {
    "type": "object",
    "additionalProperties": INDEX_ITEM_SCHEMA,
}
