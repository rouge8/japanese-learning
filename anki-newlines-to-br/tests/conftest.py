# Resolve circular imports by importing the Anki collection early
from anki.collection import Collection  # noqa: F401
