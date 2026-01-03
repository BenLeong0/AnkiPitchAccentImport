from typing import Callable, Optional

from aqt import QMenu, mw
from aqt.qt import QAction, QKeySequence

from AnkiPitchAccentImport.import_cards import importnew, importnewsentences


def set_up_menu():
    mw.form.menuTools.addSeparator()
    _add_action(
        mw.form.menuTools,
        'Import "cards.txt"',
        importnew,
        "Ctrl+Shift+C",
    )
    _add_action(
        mw.form.menuTools,
        'Import "cards_sentences.txt"',
        importnewsentences,
        "Ctrl+Shift+D",
    )


def _add_action(
    submenu: QMenu,
    label: str,
    callback: Callable[[], None],
    shortcut: Optional[str] = None,
):
    """Add action to menu"""
    action = QAction(label, mw)  # noqa # type: ignore
    action.triggered.connect(callback)
    if shortcut:
        action.setShortcut(QKeySequence(shortcut))
    submenu.addAction(action)
