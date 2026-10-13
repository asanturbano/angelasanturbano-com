# The Notebook — personal site build prompt

## Context

You are helping me build my personal website, angelasanturbano.com. I'm Angela, a principal product manager repositioning as a "builder who ships with AI." The site is a portfolio for an active job search targeting AI-native companies, so it must impress two audiences at once: hiring managers who give it 40 seconds, and fellow builders who will poke at how it's made.

This is a from-scratch redesign, developed on the `feature/notebook` branch. The previous concept (an interactive night market) is what's live on `main`; nothing on `main` changes until I approve this direction.

## The concept

A notebook lies open on a wooden desk, seen from the front of the desk at a gentle angle. Beside it stands a brass architect's desk lamp. On a first visit, the notebook's cover swings open and a fountain pen writes, in a flowing cursive (EMS Brush) and blue-black ink, my name and then a table of contents. Below the contents, the same pen draws Franklin — my dog — in pen and ink: her outline first, then washes of diluted ink bleeding into her black markings.

The pages are vellum: translucent, so the sheets underneath show faintly through. Each contents entry opens a section; the top sheet lifts away and the section page shows through, its title written by the pen and its body printed.

Visitors can make the desk their own:

- **The lamp** — dim or brighten it (pull chain, or the dimmer on its base). More light makes the vellum more see-through.
- **Music** — a 1930s cathedral radio on the desk plays Satie's *Gymnopédie No. 1* (a public-domain recording), and the pen's nib scratches faintly as it writes. Sound is always off until the visitor turns it on.

Choices are remembered in the visitor's own browser. There is no choice screen at the door — the desk works with its defaults and the controls are part of the scene.

## Content (the same as the live site — do not change without asking)

All of it lives in one place: the `#content` markup at the top of `notebook/index.html`. The notebook builds its pages from that markup, and search engines, link previews and visitors without JavaScript read it as an ordinary page. Edit content there and nowhere else.

- **Projects**
  - Solids app (solids-weld.vercel.app) — an app to help parents navigate introducing solids to your baby, starting at 6 months. *updated oct 2026*
  - The Coffee Houses of San Francisco (asanturbano.github.io/coffee-houses-sf) — my favorite SF coffee shops as a five-volume clothbound guide; a 3D bookshelf. *updated aug 2026*
  - Neko Fortune Teller (neko-fortune-teller.up.railway.app) — a grandmotherly maneki-neko reads your Four Pillars fortune; 3D, fully voiced. *updated aug 2026*
  - Ancora (ancora.coach) — practice hard conversations out loud with an AI coach.
  - Fintech voice agent — a voice agent for financial services with evaluations built in for compliance (no link).
  - Research synthesizer — point it at an arXiv paper plus your title and company; get the top product innovation, a competitive analysis, and the engineering effort (no link).
- **Writing** — Frontier Builds (frontierbuilds.substack.com), Personal Lessons (angelasanturbano.substack.com), All the Angels (alltheangels.substack.com)
- **About** — builder PM; ten years shipping payments and AI systems at Block / Square, Meta, Brex, and Cocoon; lately deep in voice AI; prototypes her own ideas with agentic coding tools; San Francisco. Franklin is mentioned by name.
- **Reach out** — LinkedIn (linkedin.com/in/angela-santurbano), X (x.com/angelasanturb), subscribe to Frontier Builds

## Design system

The full guidelines live in `design.md`. Do not drift from them. In short:

- **Palette:** dark walnut desk, warm vellum, blue-black ink, a single warm lamp. No other light sources.
- **Type:** handwriting (single-stroke script paths, animated) for short phrases only — name, contents entries, section titles, margin notes. Everything read at length is printed in EB Garamond.
- **Motion:** one choreographed timeline, built with Motion. The pen writes like a real pen: steady speed, slower on curves, lifts between words.
- **Franklin:** a pen-and-ink drawing with ink wash, traced from the reference photo (`reference/franklin-photo.jpg`, local only and gitignored — never commit it): mostly white coat, black ears and head markings, a dark patch on her side, running toward the viewer with her tongue out. `tools/franklin.py` turns the photo into the drawing (`notebook/franklin.data.js`); only the drawing is committed.

## Engineering rules

- Vanilla JS, SVG, and CSS, plus Motion (pinned: `motion@12.4.7` from jsDelivr) and Google Fonts (EB Garamond). Ask before adding anything else, or before migrating to a framework (Astro is the likely next step if the site outgrows this).
- Where things live:
  - `notebook/index.html` — the page: content (`#content` markup), styles, and the scene (desk, lamp, radio, pages, pen, sound)
  - `notebook/ink.js` — ink and pen drawing, shared by everything that writes
  - `notebook/phrases.data.js` — the handwriting, generated by `tools/handwriting.py` from EMS Brush (to add a phrase, regenerate this file)
  - `notebook/franklin.data.js` — Franklin's drawing, generated by `tools/franklin.py` from the reference photo
  - `notebook/audio/` — the radio's recording and its credits
  - `notebook/favicon.svg`, `apple-touch-icon.png`, `og.jpg` — icons and the share image (`?still` renders the finished desk for a new share image)
  - `index.html`, `night-market.html`, `dist/` — the live night market, until go-live
- Handwriting is precomputed: a one-off script converts each fixed phrase into SVG stroke paths, and the output is committed. No font-to-path work at runtime.
- Hosting: GitHub Pages from the public repo `asanturbano/angelasanturbano-com`, custom domain angelasanturbano.com. Pages is not enabled yet and the domain still points to WordPress; the cutover is part of going live. The repo is public, so anything pushed — including feature branches — is publicly visible.
- Every change must preserve:
  - real-text equivalents for everything handwritten or drawn
  - keyboard paths: Tab through the contents, Enter opens, the arrow keys turn pages, Esc returns to the contents, and the browser's Back button pages backward
  - a skip: any click or key during the opening finishes it instantly
  - `prefers-reduced-motion`: the finished page appears with no writing, drawing, or cover animation. The lamp and sound still work.
  - first-visit-only opening: return visits land on the finished contents page, with a small "watch it written" link to replay
  - readable text at the lamp's dimmest setting (contrast at least 4.5:1)
  - a web address per section (`#projects`, `#writing`, `#about`, `#reach-out`)
  - nothing on the desk overlapping the notebook's pages (labels, the radio, the card), at any window size from a small phone to an ultrawide screen
  - a clean automated accessibility check (axe-core)
- Performance budget: 60fps on a mid-tier laptop, smooth on mobile Safari. Audio loads only when the radio is switched on.
- Work one feature at a time. Propose the approach in 2–3 sentences before writing code. After each change, list what to manually test.

## Build order (each step ends with my review)

All seven steps are done on `feature/notebook`: the design brief, the handwriting test (Brush chosen), the desk, the contents with Franklin, page turns between sections, the radio, and polish (sharing metadata, icons, a plain fallback page, an accessibility check, performance and layout checks across screen sizes).

## Going live (when I approve the notebook)

1. Move the notebook to the site root; move the night market to `/night-market/` and point the notebook's old-site links there. Give the night market a link back.
2. Remove `<meta name="robots" content="noindex">`.
3. Merge `feature/notebook` into `main` and push to GitHub.
4. Turn on GitHub Pages, add the custom domain, and move DNS from WordPress; redirect any old WordPress URLs worth keeping.
