import re

_KANJI_RE = re.compile(r"[\u4E00-\u9FFF]")


def has_kanji(s: str) -> bool:
    """Whether or not a string contains Kanji."""
    return bool(re.search(_KANJI_RE, s))


def godan_verb_to_masu_form(verb: str) -> str:
    """Convert a dictionary-form Godan verb to its masu-form."""
    match verb[-1]:
        case "ぶ":
            return verb[:-1] + "びます"
        case "ぐ":
            return verb[:-1] + "ぎます"
        case "く":
            return verb[:-1] + "きます"
        case "む":
            return verb[:-1] + "みます"
        case "ぬ":
            return verb[:-1] + "にます"
        case "る":
            return verb[:-1] + "ります"
        case "す":
            return verb[:-1] + "します"
        case "つ":
            return verb[:-1] + "ちます"
        case "う":
            return verb[:-1] + "います"
        case _:
            raise ValueError(f"{verb} does not appear to be a Godan verb")
