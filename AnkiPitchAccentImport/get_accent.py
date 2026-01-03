from functools import reduce
from typing import Iterable, Literal, Optional


PathType = Literal["flat", "down", "up"]

COMBINERS = "ゃゅょぁぃぅぇぉャュョァィゥェォ"


def get_accent(reading: Iterable[str]):
    """Splits a word up into its morae, then identifies the pitch accent pattern and outputs it
    as a series of H's and L's, both as a list and a string"""

    # Splits up into morae, ignoring spaces but keeping pitch indicators

    morae = reduce(
        lambda prev, next: (
            prev[:-1] + [f"{prev[-1]}{next}"]  # combine
            if next in COMBINERS
            else prev + [" ", "・"]
            if next == "・"
            else prev + [next]
        ),
        [c for c in reading if c != " "],
        [],
    )

    # Remove brackets (both English and Japanese input)
    if "（" in morae:
        del morae[morae.index("（") :]
    if "(" in morae:
        del morae[morae.index("(") :]
    if "<" in morae:
        del morae[morae.index("<") :]

    # Set pitch accent of first mora
    if len(morae) == 1:
        return [morae, ["L", "(H)"]]
    if morae[1] == "'":
        pitches = ["H"]
    else:
        pitches = ["L"]

    # Assigns pitch height of each mora, detecting pitch identifiers, and adds particle accent after (in parentheses)
    current_height = "H"
    multiple_words = False
    for i, current_mora in list(enumerate(morae))[1:]:
        if current_mora == "'":
            current_height = "L"
        elif current_mora == "*":
            current_height = "H"
        elif current_mora == "・":
            multiple_words = True
            pitches.append("(" + current_height + ")")
            pitches.append("・")
            pitches.extend(get_accent(morae[i + 1 :])[1])
            break
        elif current_mora == " ":
            pass
        else:
            pitches.append(current_height)

    if multiple_words is False:
        pitches.append("(" + current_height + ")")

    # Removes pitch identifiers from mora list
    morae = [mora for mora in morae if mora not in "'*"]

    return [morae, pitches]


def circle(x: int, y: int, is_o: bool = False, is_dot: bool = False):
    r = f'<circle r="5" cx="{x}" cy="{y}" style="opacity:1;fill:#000;" />'
    if is_o:
        r += f'<circle r="3.25" cx="{x}" cy="{y}" style="opacity:1;fill:#fff;"' "/>"
    if is_dot:
        r = f'<circle r="0" cx="{x}" cy="{y}" style="opacity:1;fill:#000;" />'
    return r


def text(x: int, mora: str):
    # letter positioning tested with Noto Sans CJK JP
    if len(mora) == 1:
        return f'<text x="{x}" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">{mora}</text>'
    else:
        return (
            f'<text x="{x-5}" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">{mora[0]}</text>'
            f'<text x="{x+12}" y="67.5" style="font-size:14px;font-family:sans-serif;fill:#000;">{mora[1]}</text>'
        )


def path(x: int, y: int, path_type: PathType, step_width: int):
    if path_type == "flat":
        delta = f"{step_width},0"
    elif path_type == "up":
        delta = f"{step_width},-25"
    elif path_type == "down":
        delta = f"{step_width},25"
    return f'<path d="m {x},{y} {delta}" style="fill:none;stroke:#000;stroke-width:1.5;" />'


def pitch_svg(word: str, silent=False):
    """Draw pitch accent patterns in SVG

    Examples:
        はし HLL (箸)
        はし LHL (橋)
        はし LHH (端)
    """
    STEP_WIDTH = 35
    X_MARGIN = 16

    [morae, pitches] = get_accent(word)
    print([morae, pitches])
    if len(pitches) - len(morae) != 1 and not silent:
        print(f"pattern should be number of morae + 1 (got: {word}, {pitches})")

    chars = [
        text(X_MARGIN + (idx * STEP_WIDTH) - 11, " " if mora == "・" else mora)
        for idx, mora in enumerate(morae)
    ]

    circles = []
    paths = []
    prev_center: Optional[tuple[int, int]] = None
    for idx, pitch in enumerate(pitches):
        x_center = X_MARGIN + (idx * STEP_WIDTH)

        if pitch in ["・"]:
            y_center = 0
        elif pitch in ["H", "(H)"]:
            y_center = 5
        elif pitch in ["L", "(L)"]:
            y_center = 30
        else:
            assert prev_center is not None
            y_center = prev_center[1]

        is_o = pitch in ["(H)", "(L)"]
        is_dot = pitch == "・"
        circles.append(circle(x_center, y_center, is_o=is_o, is_dot=is_dot))

        if (
            idx > 0
            and morae[idx - 1] != "・"
            and not (idx < len(morae) and morae[idx] == "・")
        ):
            assert prev_center is not None
            if prev_center[1] == y_center:
                path_typ = "flat"
            elif prev_center[1] < y_center:
                path_typ = "down"
            elif prev_center[1] > y_center:
                path_typ = "up"
            else:
                raise ArithmeticError()
            paths.append(path(*prev_center, path_typ, STEP_WIDTH))

        prev_center = (x_center, y_center)

    num_positions = max(len(morae), len(pitches))
    svg_width = max(0, ((num_positions - 1) * STEP_WIDTH) + (X_MARGIN * 2))
    return (
        f'<svg class="pitch" width="{svg_width * 2}px" height="150px" viewBox="0 0 {svg_width} 75">'
        f"{''.join(chars + paths + circles)}"
        f"</svg>"
    )
