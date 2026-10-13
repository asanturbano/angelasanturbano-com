#!/usr/bin/env python3
"""Make Franklin's pen-and-ink drawing from a reference photo.

The photo stays out of the repo; only the drawing this writes is committed.

  * Her silhouette is traced by hand (SILHOUETTE, in photo pixels). The pen draws
    it as broken, tufted strokes, the way fur breaks an inked edge.
  * Her face (eyes, nose, mouth, tongue) is traced by hand too (FEATURES).
  * Inside the silhouette, the photo's tones become three ink washes — light,
    mid, dark — so her real markings and the shape of her ruff come through.
    Each wash is a small soft-edged alpha map, embedded as a PNG data URI.

Usage:
  python3 -I tools/franklin.py reference/franklin-photo.jpg > franklin.data.js
"""
import base64
import io
import json
import math
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BOX = (492, 58, 742, 476)   # the drawing's frame, in photo pixels

# Clockwise from the tip of her left ear (viewer's left).
SILHOUETTE = [
    543,76, 553,80, 563,88, 572,97, 580,108, 586,117, 595,117, 603,112, 606,98, 614,84, 626,72, 642,67,
    650,72, 657,84, 664,97, 672,104, 675,118, 671,130, 682,142, 694,152, 706,162, 718,178, 726,198,
    731,222, 734,248, 731,272, 724,296, 717,320, 711,345, 707,370, 698,388, 680,398, 667,410, 664,428,
    661,438, 652,442, 640,441, 634,433, 633,415, 631,401, 629,416, 620,422, 606,420, 601,410, 590,399,
    579,394, 574,410, 575,432, 576,455, 572,468, 560,472, 546,470, 539,461, 535,440, 531,415, 528,390,
    526,365, 522,335, 517,305, 511,280, 506,255, 503,230, 502,205, 503,180, 507,160, 512,140, 517,124,
    518,111, 522,98, 529,86, 536,79,
]
# Where the outline is paw rather than fur: drawn smooth, not tufted.
PAWS = [(534, 456, 580, 476), (628, 425, 668, 446), (598, 400, 636, 426)]

FEATURES = [
    [565,165, 572,161.5, 579,164.5, 572,168.5, 565,165],                 # eyes
    [609,162, 616,158.5, 623,161.5, 616,165.5, 609,162],
    [584,204, 590,199, 599,199, 606,204, 601,212, 595,214, 589,212, 584,204],   # nose
    [593,214, 582,219, 569,222],                                          # mouth
    [597,214, 605,220, 613,225],
    [584,229, 590,246, 600,251, 607,239, 611,227],                        # lower jaw
    [569,222, 564,240, 565,257, 570,267, 577,264, 581,249, 584,229],     # tongue, hanging from the mouth
    [574,230, 573,256],
    [588,118, 589,124],                                                   # the parting between her ears
    [575,395, 578,372, 583,352],                                          # the inside edges of her front legs
    [631,398, 632,376, 636,356],
]

WASH_LEVELS = [(.48, .13), (.66, .4), (.82, .8)]   # (density threshold, ink strength), lightest first

# Shapes inked regardless of the photo's tones, as ink density: the open mouth is dark,
# and the tongue — pink in life — takes a mid wash so it reads as part of her, not a hole.
FORCED = [
    (.92, [569,222, 582,219, 593,215, 605,220, 611,227, 607,238, 600,249, 590,246, 584,229]),
    (.72, [569,222, 564,240, 565,257, 570,267, 577,264, 581,249, 584,229]),
]


def outline_strokes(seed=7):
    """Break the silhouette into short strokes; fur edges end in a little outward flick."""
    rnd = random.Random(seed)
    pts = [(SILHOUETTE[i], SILHOUETTE[i + 1]) for i in range(0, len(SILHOUETTE), 2)]
    # resample evenly
    dense = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 3))
        dense += [(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n) for k in range(n)]
    in_paw = lambda p: any(a <= p[0] <= c and b <= p[1] <= d for a, b, c, d in PAWS)
    strokes, i = [], 0
    while i < len(dense):
        length = rnd.randint(5, 11)
        seg = dense[i:i + length]
        i += length + (0 if in_paw(dense[i]) else rnd.randint(1, 3))      # fur breaks the line often
        if len(seg) < 3:
            continue
        line = []
        for k, (x, y) in enumerate(seg):
            j = (rnd.random() - .5) * (0 if in_paw((x, y)) else 1.6)
            line += [round(x + j, 1), round(y + j, 1)]
        if not in_paw(seg[-1]):
            # outward normal for a clockwise outline (y down) is (dy, -dx)
            (ax, ay), (bx, by) = seg[-3], seg[-1]
            dx, dy = bx - ax, by - ay
            m = math.hypot(dx, dy) or 1
            f = rnd.uniform(3, 7)
            line += [round(bx + dx / m * f * .6 + dy / m * f, 1), round(by + dy / m * f * .6 - dx / m * f, 1)]
            # and now and then a loose wisp of fur just outside the edge
            if rnd.random() < .5:
                cx, cy = seg[len(seg) // 2]
                nx, ny = dy / m, -dx / m
                a, b = rnd.uniform(.5, 2), rnd.uniform(4, 8)
                strokes.append([round(cx + nx * a, 1), round(cy + ny * a, 1),
                                round(cx + nx * b + dx / m * b * .5, 1), round(cy + ny * b + dy / m * b * .5, 1)])
        strokes.append(line)
    return strokes


def washes(photo):
    x0, y0, x1, y1 = BOX
    im = Image.open(photo).convert('L').crop(BOX).filter(ImageFilter.GaussianBlur(1.6))
    lum = np.asarray(im).astype(float) / 255
    mask = Image.new('L', (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(mask).polygon([(SILHOUETTE[i] - x0, SILHOUETTE[i + 1] - y0) for i in range(0, len(SILHOUETTE), 2)], fill=255)
    mask = np.asarray(mask.filter(ImageFilter.GaussianBlur(2))).astype(float) / 255
    # ink density: lit white fur is paper, black fur is full ink
    white, black = np.percentile(lum[mask > .9], 92), np.percentile(lum[mask > .9], 4)
    dens = np.clip((white - lum) / (white - black), 0, 1)
    forced = Image.new('L', (x1 - x0, y1 - y0), 0)
    for d, poly in FORCED:
        ImageDraw.Draw(forced).polygon([(poly[i] - x0, poly[i + 1] - y0) for i in range(0, len(poly), 2)], fill=int(d * 255))
    forced = np.asarray(forced).astype(float) / 255
    dens = np.where(forced > 0, forced, dens)
    out = []
    for thr, strength in WASH_LEVELS:
        # graphic, not watery: round the shapes off, then cut them with a clean edge
        soft = Image.fromarray(((dens > thr) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.2))
        cut = (np.asarray(soft).astype(float) > 127) * mask
        band = Image.fromarray((cut * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.45))
        buf = io.BytesIO()
        band.save(buf, 'PNG', optimize=True)
        out.append({ 'strength':strength, 'src':'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode() })
    return out


def main(argv):
    if len(argv) != 2:
        sys.exit(__doc__)
    data = { 'box':BOX, 'strokes':outline_strokes() + FEATURES, 'outline':len(outline_strokes()), 'washes':washes(argv[1]) }
    print('// Generated by tools/franklin.py from a reference photo (kept out of the repo) — do not edit by hand.')
    print('// Franklin in pen and ink: outline and face strokes in photo pixels, and three ink washes.')
    print('window.FRANKLIN = ' + json.dumps(data, separators=(',', ':')) + ';')


if __name__ == '__main__':
    main(sys.argv)
