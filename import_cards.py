from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from anki.importing import TextImporter


def importnew():
    file = "D:/Ben/Downloads/cards.txt"

    # Deck name:
    did = mw.col.decks.id("Japanese Vocab (Reading)")
    mw.col.decks.select(did)

    # Note type:
    m = mw.col.models.byName("Japanese Reading with Pitch")
    deck = mw.col.decks.get(did)
    deck['mid'] = m['id']
    mw.col.decks.save(deck)
    m['did'] = did
    mw.col.models.save(m)

    with open(file, 'r', encoding='utf-8') as f:
        card = f.readline()
        count = 0
        while card:
            if card[-1:] == '\n':
                card = card[:-1]
            card += '\t' + pitch_svg(card.split('\t')[1])
            with open('temp.txt', 'w', encoding='utf-8') as temp:
                temp.write(card)
            ti = TextImporter(mw.col, 'temp.txt')
            ti.delimiter = "\t"
            ti.allowHTML = True
            ti.importMode = 1
            ti.initMapping()
            ti.run()
            card = f.readline()
            count += 1

        if count == 1:
            showInfo('1 card added')
        else:
            showInfo(str(count) + ' cards added')


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
    add_action(mw.form.menuTools, 'Import "cards.txt"', importnew, 'Ctrl+Shift+C')

setup_menu()
