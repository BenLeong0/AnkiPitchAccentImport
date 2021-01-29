# AnkiPitchAccentImport

Put in own folder in `Appdata/Roaming/Anki2/addons21`.

Change file location in `importnew()` to where new cards are copied to.

`Ctrl+Shift+C` runs addon.
`importMode` set to `1`, so importing will not overwrite any duplicates.

# Encoding

Pitch accent is encoded using `'` to denote a fall in pitch accent, and `*` to denote a rise in pitch accent.

A `・` character can be inserted between readings to generate multiple diagrams.

- Unless specified, it is assumed that the pitch accent rises after the first モラ.
- To make it such that both of the first two モラ are high, one can insert `'*` between them.
  - This is useful when denoting the pitch accent of suffixes, for example.

The code reads the text file at the specified location, and adds the words one at a time to the specified deck.

- The expected card setup has fields:
  - Vocab
  - Pronunciation
  - Meaning
  - Pitch accent
- The text file should only include data for the first three fields, delimited by `\t`.
- The addon will read extract the data from the pronunciation field and insert the SVG code into the pitch accent field.
  - There is very little error handling, although any amount of spaces can be added without interfering.

# Credits

This addon is an adapted version of the addon found [here](https://github.com/IllDepence/anki_add_pitch_plugin).
