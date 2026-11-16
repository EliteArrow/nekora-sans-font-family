"""Unicode coverage manifest and per-language repertoire verification."""
import os, sys, json, unicodedata
from fontTools.ttLib import TTFont
from fontTools import unicodedata as ftud
from common import *

# characters required per language (lowercase + uppercase + language punctuation), compiled from CLDR exemplar sets
LANGS = {
 'English': 'abcdefghijklmnopqrstuvwxyz',
 'Spanish': 'abcdefghijklmnñopqrstuvwxyzáéíóúü¿¡',
 'French': 'abcdefghijklmnopqrstuvwxyzàâæçéèêëîïôœùûüÿ«»',
 'German': 'abcdefghijklmnopqrstuvwxyzäöüßẞ„“',
 'Italian': 'abcdefghijklmnopqrstuvwxyzàèéìíîòóùú',
 'Portuguese': 'abcdefghijklmnopqrstuvwxyzáâãàçéêíóôõú',
 'Dutch': 'abcdefghijklmnopqrstuvwxyzáäéëíïĳóöúü',
 'Polish': 'aąbcćdeęfghijklłmnńoóprsśtuwyzźż',
 'Czech': 'aábcčdďeéěfghiíjklmnňoópqrřsštťuúůvwxyýzž',
 'Slovak': 'aáäbcčdďeéfghiíjklĺľmnňoóôpqrŕsštťuúvwxyýzž',
 'Hungarian': 'aábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz',
 'Romanian': 'aăâbcdefghiîjklmnopqrsștțuvwxyzşţ',
 'Turkish': 'abcçdefgğhıijklmnoöprsştuüvyz',
 'Vietnamese': 'aàảãáạăằẳẵắặâầẩẫấậbcdđeèẻẽéẹêềểễếệfghiìỉĩíịjklmnoòỏõóọôồổỗốộơờởỡớợpqrstuùủũúụưừửữứựvwxyỳỷỹýỵz₫',
 'Greek': 'αάβγδεέζηήθιίϊΐκλμνξοόπρσςτυύϋΰφχψωώ',
 'Russian': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя№',
 'Ukrainian': 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя',
 'Bulgarian': 'абвгдежзийклмнопрстуфхцчшщъьюя',
 'Serbian (Cyrillic)': 'абвгдђежзијклљмнњопрстћуфхцчџш',
 'Serbian (Latin)': 'abcčćdđefghijklmnoprsštuvzž',
 # additional languages covered by the same repertoire
 'Catalan': 'aàbcçdeéèfghiíïjklŀmnoóòpqrstuúüvwxyz·',
 'Danish': 'abcdefghijklmnopqrstuvwxyzæøå', 'Norwegian': 'abcdefghijklmnopqrstuvwxyzæøåéóòâôê', 'Swedish': 'abcdefghijklmnopqrstuvwxyzåäö',
 'Finnish': 'abcdefghijklmnopqrstuvwxyzåäöšž', 'Icelandic': 'aábdðeéfghiíjklmnoóprstuúvxyýþæö', 'Estonian': 'abdefghijklmnoprsšzžtuvõäöü',
 'Latvian': 'aābcčdeēfgģhiījkķlļmnņoprsštuūvzž', 'Lithuanian': 'aąbcčdeęėfghiįyjklmnoprsštuųūvzž', 'Croatian': 'abcčćdđefghijklmnoprsštuvzž',
 'Slovenian': 'abcčdefghijklmnoprsštuvzž', 'Albanian': 'abcçdeëfghijklmnopqrstuvxyz', 'Maltese': 'abċdefġghħijklmnopqrstuvwxżz',
 'Indonesian / Malay': 'abcdefghijklmnopqrstuvwxyz', 'Filipino': 'abcdefghijklmnñopqrstuvwxyz', 'Swahili': 'abcdefghijklmnopqrstuvwxyz',
 'Welsh': 'abcdefghijlmnoprstuwyâêîôûŵŷáéíóúẃýàèìòùẁỳäëïöüẅÿ', 'Irish': 'abcdefghilmnoprstuáéíóú', 'Azerbaijani (Latin)': 'abcçdeəfgğhxıijkqlmnoöprsştuüvyz',
 'Belarusian': 'абвгдеёжзійклмнопрстуўфхцчшыьэюя', 'Macedonian': 'абвгдѓежзѕијклљмнњопрстќуфхцчџш',
}
REQUIRED = ['English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Dutch', 'Polish', 'Czech', 'Slovak', 'Hungarian', 'Romanian',
            'Turkish', 'Vietnamese', 'Greek', 'Russian', 'Ukrainian', 'Bulgarian', 'Serbian (Cyrillic)', 'Serbian (Latin)']
UNSUPPORTED_SCRIPTS = ['Arabic', 'Hebrew', 'Devanagari', 'Thai', 'Hangul', 'Hiragana', 'Katakana', 'Han', 'Bengali', 'Tamil', 'Georgian', 'Armenian']

BLOCKS = [('Basic Latin', 0x20, 0x7E), ('Latin-1 Supplement', 0xA0, 0xFF), ('Latin Extended-A', 0x100, 0x17F), ('Latin Extended-B', 0x180, 0x24F),
          ('IPA Extensions', 0x250, 0x2AF), ('Spacing Modifier Letters', 0x2B0, 0x2FF), ('Combining Diacritical Marks', 0x300, 0x36F),
          ('Greek and Coptic', 0x370, 0x3FF), ('Cyrillic', 0x400, 0x4FF), ('Latin Extended Additional', 0x1E00, 0x1EFF),
          ('General Punctuation', 0x2000, 0x206F), ('Superscripts and Subscripts', 0x2070, 0x209F), ('Currency Symbols', 0x20A0, 0x20CF),
          ('Letterlike Symbols', 0x2100, 0x214F), ('Number Forms', 0x2150, 0x218F), ('Arrows', 0x2190, 0x21FF), ('Mathematical Operators', 0x2200, 0x22FF),
          ('Miscellaneous Technical', 0x2300, 0x23FF), ('Control Pictures', 0x2400, 0x243F), ('Geometric Shapes', 0x25A0, 0x25FF),
          ('Miscellaneous Symbols', 0x2600, 0x26FF), ('Dingbats', 0x2700, 0x27BF)]


def main():
    R = Report('unicode')
    f = TTFont(VF); cmap = f.getBestCmap(); order = f.getGlyphOrder()
    cps = sorted(cmap)
    blocks = {}
    for name, a, b in BLOCKS:
        have = [c for c in cps if a <= c <= b]
        assigned = [c for c in range(a, b + 1) if unicodedata.category(chr(c)) not in ('Cn', 'Co', 'Cs')]
        blocks[name] = dict(range='U+%04X-%04X' % (a, b), covered=len(have), assigned=len(assigned),
                            characters=''.join(chr(c) for c in have if unicodedata.category(chr(c))[0] not in 'ZCM'))
    other = [c for c in cps if not any(a <= c <= b for _, a, b in BLOCKS)]
    R.ok('every mapped codepoint lies in a documented block', not other, ['U+%04X' % c for c in other])
    # no codepoint maps to an empty outline unless it is a space / control
    glyf = f['glyf']
    empties = [('U+%04X' % c) for c, g in cmap.items() if glyf[g].numberOfContours == 0 and unicodedata.category(chr(c)) not in ('Zs', 'Cf', 'Cc')]
    R.ok('no mapped character has an empty outline', not empties, empties)
    # duplicated outlines are legitimate only for Latin / Greek / Cyrillic homographs and deliberate double encodings
    langs = {}
    for lang, chars in LANGS.items():
        need = set(chars) | set(chars.upper())
        need = {c for ch in need for c in unicodedata.normalize('NFC', ch)}
        miss = sorted(c for c in need if ord(c) not in cmap)
        langs[lang] = dict(required=lang in REQUIRED, characters=len(need), missing=miss)
        R.ok('language repertoire: %s%s' % (lang, ' (required)' if lang in REQUIRED else ''), not miss, miss)
    # scripts that are explicitly not supported must not be partially present
    scr = {}
    for c in cps:
        s = ftud.script_name(ftud.script(chr(c)))
        scr[s] = scr.get(s, 0) + 1
    partial = {s: n for s, n in scr.items() if s in UNSUPPORTED_SCRIPTS}
    R.ok('no partial coverage of unsupported scripts', not partial, partial)
    R.ok('script inventory is Latin, Greek, Cyrillic + common / inherited', set(scr) <= {'Latin', 'Greek', 'Cyrillic', 'Common', 'Inherited'}, scr)
    basic = [c for c in range(0x20, 0x7F) if c not in cmap]
    R.ok('Basic Latin complete', not basic, basic)
    l1 = [c for c in range(0xA0, 0x100) if c not in cmap and c != 0xAD]   # soft hyphen is a control character, deliberately unmapped
    R.ok('Latin-1 Supplement complete', not l1, ['U+%04X' % c for c in l1])
    la = [c for c in range(0x100, 0x180) if c not in cmap]
    R.ok('Latin Extended-A complete', not la, ['U+%04X' % c for c in la])
    viet = [c for c in range(0x1EA0, 0x1EFA) if c not in cmap]
    R.ok('Vietnamese block U+1EA0-1EF9 complete', not viet, ['U+%04X' % c for c in viet])
    gr = [c for c in list(range(0x391, 0x3A2)) + list(range(0x3A3, 0x3AA)) + list(range(0x3B1, 0x3CA)) + [0x386, 0x388, 0x389, 0x38A, 0x38C, 0x38E, 0x38F, 0x390, 0x3AA, 0x3AB, 0x3AC, 0x3AD, 0x3AE, 0x3AF, 0x3B0, 0x3CA, 0x3CB, 0x3CC, 0x3CD, 0x3CE] if c not in cmap]
    R.ok('Greek monotonic repertoire complete', not gr, ['U+%04X' % c for c in gr])
    cy = [c for c in range(0x400, 0x460) if c not in cmap]
    R.ok('Cyrillic U+0400-045F complete', not cy, ['U+%04X' % c for c in cy])
    unenc = [g for g in order if g not in set(cmap.values()) and g != '.notdef']
    manifest = dict(glyphs=len(order), codepoints=len(cps), unencoded_glyphs=len(unenc), scripts=scr, blocks=blocks, languages=langs,
                    unsupported_scripts=UNSUPPORTED_SCRIPTS)
    os.makedirs(os.path.join(ROOT, 'qa', 'unicode'), exist_ok=True)
    json.dump(manifest, open(os.path.join(ROOT, 'qa', 'unicode', 'coverage-manifest.json'), 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(ROOT, 'qa', 'unicode', 'codepoints.txt'), 'w') as fh:
        for c in cps:
            fh.write('U+%04X\t%s\t%s\n' % (c, cmap[c], unicodedata.name(chr(c), '?')))
    R.save(dict(glyphs=len(order), codepoints=len(cps), scripts=scr, blocks={k: (v['covered'], v['assigned']) for k, v in blocks.items()}))


if __name__ == '__main__':
    main()
