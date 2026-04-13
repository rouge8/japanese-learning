# shirabe-jisho-to-anki

## Setup

1. `mise run setup`
2. `mise run download_jmdict`

## Usage

```
shirabe-jisho-to-anki --jmdict-xml data/JMdict_e \
  --anki-collection ~/Library/Application\ Support/Anki2/User\ 1/collection.anki2 \
  --anki-deck Japanese \
  --shirabe-jisho-csv ~/Downloads/Butter\ Chapter\ 1.csv
```

## Testing and type-checking

`tox`
