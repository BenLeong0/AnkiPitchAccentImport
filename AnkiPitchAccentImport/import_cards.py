from AnkiPitchAccentImport.get_accent import pitch_svg

from aqt import mw
from aqt.utils import showInfo
from anki.collection import Collection
from anki.importing import TextImporter

VOCAB_CARDS_INPUT_FILENAME = "/Users/benleong/Downloads/cards.txt"
SENTENCE_CARDS_INPUT_FILENAME = "/Users/benleong/Downloads/cards_sentences.txt"


def importnew():
    collection = _get_collection(
        deck_name="Japanese Vocab::Japanese Vocab (Reading)",
        model_name="Japanese Reading with Pitch",
    )

    with open(VOCAB_CARDS_INPUT_FILENAME, "r", encoding="utf-8") as f:
        cards = [s.strip().replace("  /  ", "&nbsp; / &nbsp;") for s in f.readlines()]
        cards_with_pitch = [
            card + "\t" + pitch_svg(card.split("\t")[1]) for card in cards
        ]

        _import_cards(collection, cards_with_pitch)

        num_cards = len(cards)
        counter = "card" if num_cards == 1 else "cards"
        showInfo(f"{num_cards} {counter} added")


def importnewsentences():
    collection = _get_collection(
        deck_name="Japanese Vocab::Japanese Vocab (Sentences)",
        model_name="Japanese Reading with Sentence and Pitch",
    )

    with open(SENTENCE_CARDS_INPUT_FILENAME, "r", encoding="utf-8") as f:
        cards = [s.strip() for s in f.readlines()]
        split_cards = [card.split("\t") for card in cards]

        cards_with_pitch = [
            "\t".join(
                [
                    sentence_jp.replace(
                        suruless_word := word.replace("（する）", ""),
                        f"<strong>{suruless_word}</strong>",
                    ),
                    sentence_en,
                    word,
                    reading,
                    definition.replace("  /  ", "&nbsp; / &nbsp;"),
                    pitch_svg(reading),
                ]
            )
            for word, reading, definition, sentence_jp, sentence_en in split_cards
        ]

        _import_cards(collection, cards_with_pitch)

        num_cards = len(cards)
        counter = "card" if num_cards == 1 else "cards"
        showInfo(f"{num_cards} {counter} added")


def _get_collection(*, deck_name: str, model_name: str) -> Collection:
    mw_col = mw.col
    assert mw_col is not None

    deck = mw_col.decks.by_name(deck_name)
    m = mw_col.models.by_name(model_name)
    assert m and deck

    deck["mid"] = m["id"]
    m["did"] = deck["id"]

    mw_col.decks.select(deck["id"])
    mw_col.decks.save(deck)
    mw_col.models.save(m)

    return mw_col


def _import_cards(collection: Collection, cards: list[str]):
    tmp_filename = "/tmp/cards.txt"
    with open(tmp_filename, "w", encoding="utf-8") as temp:
        temp.writelines("\n".join(cards) + "\n")

    ti = TextImporter(collection, tmp_filename)
    ti.delimiter = "\t"
    ti.allowHTML = True
    ti.importMode = 1
    ti.initMapping()
    ti.run()
