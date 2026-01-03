# AnkiPitchAccentImport

Put the addon in its own folder in `Appdata/Roaming/Anki2/addons21`.

Change the input files in `import_cards.py` to the text files where new cards are inserted.

- `Cmd+Shift+C` runs the addon for vocab cards, and `Cmd+Shift+D` for sentence cards.
- `importMode` is set to `1`, so importing will not overwrite any duplicates.

# Encoding

Pitch accent is encoded using `'` to denote a fall in pitch accent, and `*` to denote a rise in pitch accent.

A `・` character can be inserted between readings to generate multiple diagrams.

- Unless specified, it is assumed that the pitch accent rises after the first モラ.
- To make it such that both of the first two モラ are high, one can insert `'*` between them.
  - This is useful when denoting the pitch accent of suffixes, for example.
  - eg: `～側` → `～'*がわ` (this results in a `HHH(H)` pattern **including** the ～, implying the relation to the stem).

The code reads the text file at the specified location, and adds each the words to ~~the specified deck~~ a deck 🫩.

- The cards may be added to a random deck, and in this case must be manually transferred.

- The expected card setup has fields:
  - Vocab
  - Pronunciation
  - Meaning
  - Japanese sentence (for sentence cards only)
  - English sentence (for sentence cards only)
  - Pitch accent
- The text file should include data for all fields excluding pitch accent, delimited by `\t`.
- The addon will read extract the data from the pronunciation field and insert the SVG code into the pitch accent field.
  - Spaces in the pronunciation are all ignored.
  - Any duplicates are skipped (since `importMode=1`).

# Credits

This addon is an adapted version of the addon found [here](https://github.com/IllDepence/anki_add_pitch_plugin), to read my own pitch accent data rather than download from Wadoku.

- I created this adaptation for two main reasons:
  - Although extensive, Wadoku is by no means a complete source, especially with regards to uncommon, old or colloquial terms.
  - Wadoku is not always reliable. As such, I cross-check my data with [Wadoku](https://www.wadoku.de/), Suzuki-kun ([sentence](http://www.gavo.t.u-tokyo.ac.jp/ojad/eng/phrasing/index) and [vocab](http://www.gavo.t.u-tokyo.ac.jp/ojad/)) and [Forvo](https://forvo.com/).
