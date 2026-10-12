// Ink and pen for the notebook: draws handwriting phrases (from phrases.data.js)
// as fountain-pen ink in SVG, and draws the pen itself.
// Coordinates are font units: 1000 per em, baseline at 0, y pointing down.
(() => {
  const SVGNS = 'http://www.w3.org/2000/svg';

  // A broad nib held at a fixed angle: K offset copies of each stroke make the
  // downstrokes thick and the sideways strokes hairline thin (about 5:1).
  const NIB = { width:64, angle:-35 * Math.PI / 180, copies:11, hairline:15 };
  const INK_DRY = '#1B2433', INK_WET = '#22304A';

  function el(tag, attrs, parent){
    const e = document.createElementNS(SVGNS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  // Catmull-Rom through a flat point list -> smooth cubic path data
  function smoothPath(p){
    const n = p.length / 2;
    if (n < 2) return `M${p[0]} ${p[1]}`;
    const P = (i) => { const j = 2 * Math.max(0, Math.min(n - 1, i)); return [p[j], p[j + 1]]; };
    let d = `M${p[0]} ${p[1]}`;
    for (let i = 0; i < n - 1; i++){
      const [x0, y0] = P(i - 1), [x1, y1] = P(i), [x2, y2] = P(i + 1), [x3, y3] = P(i + 2);
      d += `C${(x1 + (x2 - x0) / 6).toFixed(1)} ${(y1 + (y2 - y0) / 6).toFixed(1)} ${(x2 - (x3 - x1) / 6).toFixed(1)} ${(y2 - (y3 - y1) / 6).toFixed(1)} ${x2} ${y2}`;
    }
    return d;
  }

  function phrase(text){
    const p = window.PHRASES.phrases.find((x) => x.phrase === text);
    if (!p) throw new Error(`no handwriting for "${text}" — regenerate phrases.data.js`);
    return p;
  }

  // Time table for one stroke: slower through curves and at touch-down and lift-off.
  // `weight` is the stroke's duration in arbitrary units; the choreographer scales it.
  function timing(p){
    const n = p.length / 2, len = [0], w = [0];
    for (let i = 1; i < n; i++){
      const dx = p[2 * i] - p[2 * i - 2], dy = p[2 * i + 1] - p[2 * i - 1];
      let turn = 0;
      if (i > 1){
        const a0 = Math.atan2(p[2 * i - 1] - p[2 * i - 3], p[2 * i - 2] - p[2 * i - 4]), a1 = Math.atan2(dy, dx);
        turn = Math.abs(Math.atan2(Math.sin(a1 - a0), Math.cos(a1 - a0)));
      }
      const ds = Math.hypot(dx, dy);
      len.push(len[i - 1] + ds);
      w.push(ds + turn * 70);
    }
    const total = len[n - 1] || 1;
    let acc = 0; const time = [0];
    for (let i = 1; i < n; i++){
      const f = len[i] / total;
      acc += w[i] * ((f < .08 || f > .92) ? 1.7 : 1);
      time.push(acc);
    }
    return { len, time, total, weight:acc || 1 };
  }

  // Animatable ink: each stroke starts hidden; show() reveals a fraction of it.
  // Strokes are in font units, placed at (x, y) in the parent's coordinates at s px per unit.
  function prepare(parent, strokes, { x = 0, y = 0, s = 1 } = {}){
    const ox = Math.cos(NIB.angle) * NIB.width / 2, oy = Math.sin(NIB.angle) * NIB.width / 2;
    const g = el('g', { transform:`translate(${x} ${y}) scale(${s})`, fill:'none',
      'stroke-linecap':'round', 'stroke-linejoin':'round', 'stroke-width':NIB.hairline }, parent);
    const out = strokes.map((st) => {
      const d = smoothPath(st.pts), sg = el('g', { opacity:0, color:INK_DRY }, g);
      el('circle', { cx:st.pts[0], cy:st.pts[1], r:NIB.width * .42, fill:'currentColor', stroke:'none' }, sg);   // ink pools where the nib lands
      const copies = [];
      for (let k = 0; k < NIB.copies; k++){
        const u = k / (NIB.copies - 1) * 2 - 1;
        copies.push(el('path', { d, pathLength:1, 'stroke-dasharray':'1 1', 'stroke-dashoffset':1, stroke:'currentColor',
          transform:`translate(${(u * ox).toFixed(1)} ${(u * oy).toFixed(1)})` }, sg));
      }
      return { g:sg, copies, ref:copies[NIB.copies >> 1], refLen:0, pts:st.pts, word:st.word || 0,
        late:!!st.late, tm:timing(st.pts), x, y, s, shown:-1 };
    });
    return { g, strokes:out };
  }

  // Where the nib is when `frac` of the stroke is drawn, in the parent's coordinates.
  function at(st, frac){
    if (!st.refLen) st.refLen = st.ref.getTotalLength();
    const p = st.ref.getPointAtLength(frac * st.refLen);
    return [st.x + p.x * st.s, st.y + p.y * st.s];
  }
  function start(st){ return [st.x + st.pts[0] * st.s, st.y + st.pts[1] * st.s]; }
  function end(st){ const n = st.pts.length; return [st.x + st.pts[n - 2] * st.s, st.y + st.pts[n - 1] * st.s]; }

  // Reveal a stroke: frac < 0 hides it; `wet` (0..1) blends from dry to freshly wet ink.
  const DRY = [27, 36, 51], WET = [34, 48, 74];
  function show(st, frac, wet = 0){
    const key = frac < 0 ? -1 : `${Math.round(frac * 2000)}|${wet.toFixed(2)}`;
    if (key === st.shown) return;
    st.shown = key;
    if (frac < 0){ st.g.setAttribute('opacity', 0); return; }
    st.g.setAttribute('opacity', 1);
    const off = (1 - frac).toFixed(4);
    for (const c of st.copies) c.setAttribute('stroke-dashoffset', off);
    st.g.setAttribute('color', `rgb(${DRY.map((v, i) => Math.round(v + (WET[i] - v) * wet)).join(',')})`);
  }

  // Draw a phrase as finished, dry ink. Returns the <g> holding one group per stroke.
  function write(parent, text, { x = 0, y = 0, scale = 1 } = {}){
    const p = phrase(text);
    const ox = Math.cos(NIB.angle) * NIB.width / 2, oy = Math.sin(NIB.angle) * NIB.width / 2;
    const g = el('g', { transform:`translate(${x} ${y}) scale(${scale})`, fill:'none', stroke:INK_DRY,
      'stroke-linecap':'round', 'stroke-linejoin':'round', 'stroke-width':NIB.hairline }, parent);
    for (const s of p.strokes){
      const d = smoothPath(s.pts), sg = el('g', {}, g);
      for (let k = 0; k < NIB.copies; k++){
        const u = k / (NIB.copies - 1) * 2 - 1;
        el('path', { d, transform:`translate(${(u * ox).toFixed(1)} ${(u * oy).toFixed(1)})` }, sg);
      }
    }
    return g;
  }

  // The fountain pen, tip at (0,0), barrel along +x, in px. Pass a flat color to draw its shadow.
  function pen(g, flat){
    const f = (c) => flat || c;
    el('path', { d:'M0 0 L13 -3.2 L28 -6.2 L33 -6.6 L33 6.6 L28 6.2 L13 3.2 Z', fill:f('#C8A45C') }, g);
    if (!flat){
      el('path', { d:'M1.5 0 L21 0', stroke:'#5A4420', 'stroke-width':.8 }, g);
      el('circle', { cx:22, cy:0, r:1.3, fill:'#5A4420' }, g);
      el('path', { d:'M4 -1 L26 -5', stroke:'rgba(255,240,200,.6)', 'stroke-width':.7 }, g);
    }
    el('path', { d:'M33 -6.6 L66 -7.6 L66 7.6 L33 6.6 Z', fill:f('#14171D') }, g);
    el('rect', { x:66, y:-8, width:3.5, height:16, fill:f('#C8A45C') }, g);
    el('rect', { x:69, y:-8.6, width:150, height:17.2, rx:3, fill:f('#1B2433') }, g);
    el('rect', { x:196, y:-9.6, width:74, height:19.2, rx:9, fill:f('#161D2A') }, g);
    if (!flat){
      el('rect', { x:198, y:-9.6, width:4, height:19.2, fill:'#C8A45C' }, g);
      el('path', { d:'M206 -9.6 L206 -12 L256 -12 Q260 -12 260 -9.6', fill:'none', stroke:'#C8A45C', 'stroke-width':2.2 }, g);
      el('rect', { x:70, y:-6.8, width:190, height:2.2, rx:1, fill:'rgba(255,236,206,.22)' }, g);
      el('rect', { x:34, y:-5.4, width:31, height:1.6, fill:'rgba(255,236,206,.18)' }, g);
    }
    return g;
  }

  window.Ink = { NIB, INK_DRY, INK_WET, el, smoothPath, phrase, timing, prepare, at, start, end, show, write, pen };
})();
