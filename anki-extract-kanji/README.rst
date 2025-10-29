anki-extract-kanji
==================

Find "unknown" kanji in an Anki collection.

Installation
------------

With uv:
^^^^^^^^

1. ``uv sync``

With mise:
^^^^^^^^^^

1. ``mise trust``
2. ``mise install``

Usage
-----

.. code-block:: sh

   # https://docs.ankiweb.net/files.html#user-data
   uv run anki-extract-kanji --collection PATH_TO_ANKI_COLLECTION --vocab-deck "Japanese" --kanji-deck "Kanji"
