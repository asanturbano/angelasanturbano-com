#!/usr/bin/env python3
"""Convert fixed phrases into single-stroke handwriting for the pen to write.

Reads an SVG 1.1 single-stroke font (for example the EMS fonts from
https://gitlab.com/oskay/svg-fonts, SIL Open Font License) and lays each
phrase out glyph by glyph. Output is JSON: strokes as flat point lists in
font units, y pointing down, baseline at 0.

Two touches make the result write like a hand:
  * strokes that meet the next stroke of the same word are merged, so the
    pen doesn't lift inside connected letters;
  * the dots and crosses of i, j, t, f and x are marked "late" and moved to
    the end of their word, the way a person dots and crosses afterwards.

Usage:
  python3 -I tools/handwriting.py FONT.svg "Phrase" ["Another phrase" ...]
"""
import html
import json
import re
import sys

LATE_CHARS = set('ijtfx')
JOIN_DIST = 30      # font units: closer than this and the pen stays down
CURVE_STEPS = 8     # samples per cubic segment

NUM = r'-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'


def attrs(tag):
    return dict(re.findall(r'([\w:-]+)="([^"]*)"', tag))


def parse_font(path):
    src = open(path, encoding='utf-8').read()
    font = attrs(re.search(r'<font\b[^>]*>', src).group(0))
    default_adv = float(font.get('horiz-adv-x', 500))
    meta = re.search(r'<metadata>(.*?)</metadata>', src, re.S)
    glyphs = {}
    for tag in re.findall(r'<glyph\b[^>]*>', src):
        a = attrs(tag)
        ch = html.unescape(a.get('unicode', ''))
        if len(ch) == 1:
            glyphs[ch] = (float(a.get('horiz-adv-x', default_adv)), a.get('d', ''))
    return glyphs, default_adv, (meta.group(1).strip() if meta else '')


def subpaths(d):
    """Absolute M/L/C path data -> list of point lists (cubics sampled)."""
    toks = re.findall(r'[A-Za-z]|' + NUM, d)
    out, cur, cmd, i = [], None, None, 0
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            if t not in 'MLC':
                raise ValueError(f'unsupported path command {t!r}')
            cmd, i = t, i + 1
            continue
        n = [float(v) for v in toks[i:i + (6 if cmd == 'C' else 2)]]
        if cmd == 'M':
            cur = [(n[0], n[1])]
            out.append(cur)
            cmd = 'L'
            i += 2
        elif cmd == 'L':
            cur.append((n[0], n[1]))
            i += 2
        else:
            (x0, y0), (x1, y1, x2, y2, x3, y3) = cur[-1], n
            for k in range(1, CURVE_STEPS + 1):
                s = k / CURVE_STEPS
                a, b, c, e = (1 - s) ** 3, 3 * s * (1 - s) ** 2, 3 * s * s * (1 - s), s ** 3
                cur.append((a * x0 + b * x1 + c * x2 + e * x3, a * y0 + b * y1 + c * y2 + e * y3))
            i += 6
    return out


def dist(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5


def layout(glyphs, default_adv, phrase):
    x, word = 0.0, 0
    raw = []
    for ch in phrase:
        if ch == ' ':
            x += glyphs.get(' ', (default_adv, ''))[0]
            word += 1
            continue
        if ch not in glyphs:
            raise KeyError(f'font has no glyph for {ch!r}')
        adv, d = glyphs[ch]
        for si, sp in enumerate(subpaths(d)):
            pts = [(px + x, -py) for px, py in sp]
            raw.append({'pts': pts, 'word': word, 'late': ch in LATE_CHARS and si > 0})
        x += adv

    strokes = []
    for w in range(word + 1):
        main = [s for s in raw if s['word'] == w and not s['late']]
        late = [s for s in raw if s['word'] == w and s['late']]
        merged = []
        for s in main:
            if merged and dist(merged[-1]['pts'][-1], s['pts'][0]) < JOIN_DIST:
                merged[-1]['pts'].extend(s['pts'][1:])
            else:
                merged.append({'pts': list(s['pts']), 'word': w})
        strokes += merged + [{'pts': s['pts'], 'word': w, 'late': True} for s in late]

    for s in strokes:
        dedup = [s['pts'][0]]
        for p in s['pts'][1:]:
            if dist(p, dedup[-1]) > 0.5:
                dedup.append(p)
        s['pts'] = [round(v, 1) for p in dedup for v in p]

    xs = [v for s in strokes for v in s['pts'][0::2]]
    ys = [v for s in strokes for v in s['pts'][1::2]]
    return {'phrase': phrase, 'bbox': [min(xs), min(ys), max(xs), max(ys)], 'strokes': strokes}


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    glyphs, default_adv, meta = parse_font(argv[1])
    out = {'font': meta.splitlines()[0].split(':', 1)[-1].strip() if meta else argv[1],
           'license': meta,
           'phrases': [layout(glyphs, default_adv, p) for p in argv[2:]]}
    json.dump(out, sys.stdout, separators=(',', ':'))


if __name__ == '__main__':
    main(sys.argv)
