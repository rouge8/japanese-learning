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


Keeping up to date with the template
------------------------------------

.. code-block:: sh

   # Add the 'template' remote if necessary
   git remote get-url template || git remote add template git@github.com:rouge8/python-template.git

   # Fetch and merge the latest changes
   git fetch template
   git merge template/main

   # Resolve any merge conflicts, run the tests, commit your changes, etc.
