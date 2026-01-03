from typing import cast
from AnkiPitchAccentImport.get_accent import pitch_svg

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import QAction, QKeySequence
from anki.importing import TextImporter
from anki.decks import DeckId


def importnew():
    file = "/Users/benleong/Downloads/cards.txt"

    mw_col = mw.col
    assert mw_col is not None

    deck = mw_col.decks.by_name("Japanese Vocab::Japanese Vocab (Reading)")
    m = mw_col.models.by_name("Japanese Reading with Pitch")
    assert m and deck

    deck["mid"] = m["id"]
    m["did"] = deck["id"]

    mw_col.decks.select(deck["id"])
    mw_col.decks.save(deck)
    mw_col.models.save(m)

    with open(file, "r", encoding="utf-8") as f:
        card = f.readline()
        count = 0
        while card:
            if card[-1:] == "\n":
                card = card[:-1]
            card += "\t" + pitch_svg(card.split("\t")[1])
            while card.count("  /  ") > 0:
                card = card.replace("  /  ", "&nbsp; / &nbsp;")
            with open("/tmp/cards.txt", "w", encoding="utf-8") as temp:
                temp.write(card)
            ti = TextImporter(mw_col, "/tmp/cards.txt")
            ti.delimiter = "\t"
            ti.allowHTML = True
            ti.importMode = 1
            ti.initMapping()
            ti.run()
            card = f.readline()
            count += 1

        if count == 1:
            showInfo("1 card added")
        else:
            showInfo(str(count) + " cards added")


def importnewsentences():
    file = "/Users/benleong/Downloads/cards_sentences.txt"

    mw_col = mw.col
    assert mw_col is not None

    deck = mw_col.decks.by_name("Japanese Vocab::Japanese Vocab (Sentences)")
    m = mw_col.models.by_name("Japanese Reading with Sentence and Pitch")
    assert m and deck

    deck["mid"] = m["id"]
    m["did"] = deck["id"]

    mw_col.decks.select(deck["id"])
    mw_col.decks.save(deck)
    mw_col.models.save(m)

    with open(file, "r", encoding="utf-8") as f:
        card = f.readline()
        count = 0
        while card:
            if card[-1:] == "\n":
                card = card[:-1]
            word, reading, definition, sentence_jp, sentence_en = card.split("\t")
            suruless_word = word.replace("（する）", "")
            pronunciation = pitch_svg(reading)
            definition = definition.replace("  /  ", "&nbsp; / &nbsp;")
            sentence_jp = sentence_jp.replace(
                suruless_word, f"<strong>{suruless_word}</strong>"
            )
            with open("/tmp/cards.txt", "w", encoding="utf-8") as temp:
                temp.write(
                    "\t".join(
                        [
                            sentence_jp,
                            sentence_en,
                            word,
                            reading,
                            definition,
                            pronunciation,
                        ]
                    )
                )
            ti = TextImporter(mw_col, "/tmp/cards.txt")
            ti.delimiter = "\t"
            ti.allowHTML = True
            ti.importMode = 1
            ti.initMapping()
            ti.run()
            card = f.readline()
            count += 1

        if count == 1:
            showInfo("1 card added")
        else:
            showInfo(str(count) + " cards added")


# create a new menu item, "test"
# action = QAction("Import cards.txt", mw)
# # set it to call testFunction when it's clicked
# action.triggered.connect(importnew)
# # and add it to the tools menu
# mw.form.menuTools.addAction(action)


def add_action(submenu, label, callback, shortcut=None):
    """Add action to menu"""
    action = QAction(_(label), mw)
    action.triggered.connect(callback)
    if shortcut:
        action.setShortcut(QKeySequence(shortcut))
    submenu.addAction(action)


def setup_menu():
    mw.form.menuTools.addSeparator()
    add_action(mw.form.menuTools, 'Import "cards.txt"', importnew, "Ctrl+Shift+C")
    add_action(
        mw.form.menuTools,
        'Import "cards_sentences.txt"',
        importnewsentences,
        "Ctrl+Shift+D",
    )


setup_menu()
