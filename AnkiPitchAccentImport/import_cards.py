from AnkiPitchAccentImport.get_accent import pitch_svg

from aqt import mw
from aqt.utils import showInfo
from anki.decks import DeckId
from anki.models import NotetypeDict
from anki.notes import NoteFieldsCheckResult

VOCAB_CARDS_INPUT_FILENAME = "/Users/benleong/Downloads/cards.txt"
SENTENCE_CARDS_INPUT_FILENAME = "/Users/benleong/Downloads/cards_sentences.txt"


def importnew():
    deck_id, model = _get_deck_and_model(
        deck_name="Japanese Vocab::Japanese Vocab (Reading)",
        model_name="Japanese Reading with Pitch",
    )

    with open(VOCAB_CARDS_INPUT_FILENAME, "r", encoding="utf-8") as f:
        cards = [s.strip().replace("  /  ", "&nbsp; / &nbsp;") for s in f.readlines()]
        cards_with_pitch = [
            card + "\t" + pitch_svg(card.split("\t")[1]) for card in cards
        ]

        _import_cards(deck_id, model, cards_with_pitch)


def importnewsentences():
    deck_id, model = _get_deck_and_model(
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

        _import_cards(deck_id, model, cards_with_pitch)


def _get_deck_and_model(
    *, deck_name: str, model_name: str
) -> tuple[DeckId, NotetypeDict]:
    col = mw.col
    assert col is not None

    deck_id = col.decks.id_for_name(deck_name)
    model = col.models.by_name(model_name)
    assert model and deck_id

    return deck_id, model


def _import_cards(deck_id: DeckId, model: NotetypeDict, cards: list[str]):
    """Add one note per tab-separated line, skipping duplicates of the first field."""
    col = mw.col
    assert col is not None

    num_added = 0
    num_duplicates = 0
    for card in cards:
        note = col.new_note(model)
        for i, value in enumerate(card.split("\t")[: len(note.fields)]):
            note.fields[i] = value

        if note.fields_check() == NoteFieldsCheckResult.DUPLICATE:
            num_duplicates += 1
            continue

        col.add_note(note, deck_id)
        num_added += 1

    mw.reset()

    counter = "card" if num_added == 1 else "cards"
    message = f"{num_added} {counter} added"
    if num_duplicates:
        message += f" ({num_duplicates} duplicates skipped)"
    showInfo(message)
