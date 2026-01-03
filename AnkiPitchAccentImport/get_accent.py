from typing import Optional


def get_accent(a):
    """Splits a word up into its morae, then identifies the pitch accent pattern and outputs it
    as a series of H's and L's, both as a list and a string"""

    # Splits up into morae, ignoring spaces but keeping pitch indicators
    i = 0
    b = []
    combiners = [
        "ゃ",
        "ゅ",
        "ょ",
        "ぁ",
        "ぃ",
        "ぅ",
        "ぇ",
        "ぉ",
        "ャ",
        "ュ",
        "ョ",
        "ァ",
        "ィ",
        "ゥ",
        "ェ",
        "ォ",
    ]
    multiple_words = False

    while i < len(a):  # Making mora list
        if a[i] == " ":
            pass
        elif i + 1 < len(a) and a[i + 1] in combiners:
            b.append("{}{}".format(a[i], a[i + 1]))
            i += 1
        elif a[i] == "・":
            b.append(" ")
            b.append("・")
        else:
            b.append(a[i])
        i += 1

    # Remove brackets (both English and Japanese input)
    if b.count("（") != 0:
        del b[b.index("（") :]
    if b.count("(") != 0:
        del b[b.index("(") :]
    if b.count("<") != 0:
        del b[b.index("<") :]

    # Set pitch accent of first mora
    if len(b) == 1:
        return [b, ["L", "(H)"]]
    if b[1] == "'":
        pitch_accent = ["H"]
        # pa_str = 'H'
    else:
        pitch_accent = ["L"]
        # pa_str = 'L'

    # Assigns pitch height of each mora, detecting pitch identifiers, and adds particle accent after (in parentheses)
    height = "H"
    for i in range(1, len(b)):
        if b[i] == "'":
            height = "L"
        elif b[i] == "*":
            height = "H"
        elif b[i] == "・":
            multiple_words = True
            pitch_accent.append("(" + height + ")")
            pitch_accent.append("・")
            for h in get_accent(b[i + 1 :])[1]:
                pitch_accent.append(h)
            break
        elif b[i] == " ":
            pass
        else:
            pitch_accent.append(height)
            # pa_str += height
    if multiple_words is False:
        pitch_accent.append("(" + height + ")")
    # pa_str += "(" + height + ")"

    # Removes pitch identifiers from mora list
    for i in range(b.count("'")):
        b.remove("'")
    for i in range(b.count("*")):
        b.remove("*")

    return [b, pitch_accent]


def circle(x, y, o=False, dot=False):
    r = ('<circle r="5" cx="{}" cy="{}" style="opacity:1;fill:#000;" />').format(x, y)
    if dot:
        r = ('<circle r="0" cx="{}" cy="{}" style="opacity:1;fill:#000;" />').format(
            x, y
        )
    if o:
        r += (
            '<circle r="3.25" cx="{}" cy="{}" style="opacity:1;fill:#fff;"' "/>"
        ).format(x, y)
    return r


def text(x, mora):
    # letter positioning tested with Noto Sans CJK JP
    if len(mora) == 1:
        return (
            '<text x="{}" y="67.5" style="font-size:20px;font-family:sans-'
            'serif;fill:#000;">{}</text>'
        ).format(x, mora)
    else:
        return (
            '<text x="{}" y="67.5" style="font-size:20px;font-family:sans-'
            'serif;fill:#000;">{}</text><text x="{}" y="67.5" style="font-'
            'size:14px;font-family:sans-serif;fill:#000;">{}</text>'
        ).format(x - 5, mora[0], x + 12, mora[1])


def path(x, y, typ, step_width):
    if typ == "s":  # straight
        delta = "{},0".format(step_width)
    elif typ == "u":  # up
        delta = "{},-25".format(step_width)
    elif typ == "d":  # down
        delta = "{},25".format(step_width)
    else:
        raise ValueError("delta not assigned")
    return (
        '<path d="m {},{} {}" style="fill:none;stroke:#000;stroke-width' ':1.5;" />'
    ).format(x, y, delta)


def pitch_svg(word, silent=False):
    """Draw pitch accent patterns in SVG

    Examples:
        はし HLL (箸)
        はし LHL (橋)
        はし LHH (端)
    """

    [mora, patt] = get_accent(word)
    print([mora, patt])

    if len(patt) - len(mora) != 1 and not silent:
        print(
            ("pattern should be number of morae + 1 (got: {}, {})").format(word, patt)
        )
    positions = max(len(mora), len(patt))
    step_width = 35
    margin_lr = 16
    svg_width = max(
        0, ((positions - 1) * step_width) + (margin_lr * 2)
    )  # Setup svg object

    svg = (
        '<svg class="pitch" width="{0}px" height="150px" viewBox="0 0 {1} 75' '">'
    ).format(svg_width * 2, svg_width)

    chars = ""
    for pos, mor in enumerate(mora):
        x_center = margin_lr + (pos * step_width)
        if mor != "・":
            chars += text(x_center - 11, mor)
        else:
            chars += text(x_center - 11, " ")

    circles = ""
    paths = ""
    y_center = None
    path_typ = None
    prev_center: Optional[tuple[int, int]] = None
    for pos, accent in enumerate(patt):
        x_center = margin_lr + (pos * step_width)
        dot = o = False

        if accent in ["・"]:
            y_center = 0
            dot = True
        elif accent in ["H", "(H)"]:
            y_center = 5
        elif accent in ["L", "(L)"]:
            y_center = 30
        assert y_center is not None

        if accent in ["(H)", "(L)"]:
            o = True
        circles += circle(x_center, y_center, o, dot)
        line = True
        if pos > 0:
            if pos < len(mora):
                if mora[pos] == "・":
                    line = False
            if mora[pos - 1] == "・":
                line = False

            if line is True:
                assert prev_center is not None
                if prev_center[1] == y_center:
                    path_typ = "s"  # same
                elif prev_center[1] < y_center:
                    path_typ = "d"  # down
                elif prev_center[1] > y_center:
                    path_typ = "u"  # up
                assert path_typ is not None
                paths += path(prev_center[0], prev_center[1], path_typ, step_width)

        prev_center = (x_center, y_center)

    svg += chars
    svg += paths
    svg += circles
    svg += "</svg>"

    return svg


# s = "てんの' う・すめらみ' こと"
# print(pitch_svg(s))
