"""Character repertoire: precomposed characters built from base + marks."""
import unicodedata

RANGES = [
    (0x00C0, 0x00FF),            # Latin-1 Supplement
    (0x0100, 0x017F),            # Latin Extended-A
    (0x01A0, 0x01B0),            # O / U with horn (Vietnamese)
    (0x01CD, 0x01DC),            # Pinyin tone letters
    (0x01E6, 0x01EB),            # G caron, K caron, O ogonek
    (0x01F4, 0x01F5), (0x01FC, 0x01FF),
    (0x0218, 0x021B),            # Romanian comma-below letters
    (0x0232, 0x0233),            # Y macron
    (0x1E80, 0x1E85),            # Welsh W grave / acute / dieresis
    (0x1EA0, 0x1EF9),            # Vietnamese
    (0x0386, 0x03CE),            # Greek (monotonic)
    (0x0400, 0x045F),            # Cyrillic
]
SKIP = {0x0149, 0x0344, 0x0387}
COMPOSED = [cp for a, b in RANGES for cp in range(a, b + 1)
            if cp not in SKIP and len(unicodedata.normalize('NFD', chr(cp))) > 1]

# glyphs composed outside Unicode decomposition: name -> (base, [marks], [codepoints])
EXTRA_COMPOSITES = {}


def uni_name(cp):
    return 'uni%04X' % cp
