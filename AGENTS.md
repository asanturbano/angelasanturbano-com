# Night Market — personal site build prompt

## Context

You are helping me build my personal website, angelasanturbano.com. I'm Angela, a principal product manager repositioning as a "builder who ships with AI." The site is a portfolio for an active job search targeting AI-native companies, so it must impress two audiences at once: hiring managers who give it 40 seconds, and fellow builders who will poke at how it's made.

## The concept

The site is an interactive night market, rendered like an underexposed night photograph. Visitors steer Franklin, my Shetland Sheepdog, down a market street with arrow keys (or tap-to-walk on mobile). Four stalls hold the content:

- **Projects** — Ancora (ancora.coach), a customer support voice agent (demo on request)
- **Writing** — Frontier Builds newsletter (frontierbuilds.substack.com), the archive (angelasanturbano.substack.com), Angel investing ([https://alltheangels.substack.com/](https://alltheangels.substack.com/))
- **About Me** — Product manager for 10+ years at Block, Meta, Brex, Cocoon; currently deep in voice AI; San Francisco
- **Reach Out** — LinkedIn (linkedin.com/in/angela-santurbano), X (x.com/angelasanturb), newsletter subscribe

Walking up to a stall highlights the stall, pressing up opens a paper menu card with that stall's links or you can click on the stall directly. A three lines menu button (top right) is the permanent escape hatch: every link on one card, no strolling required. **Never remove it.**

## Design system — do not drift from this

- **Grade:** underexposed night photo. Near-black backdrop, tungsten palette only (reds `#E8502E`/`#C73E2A`, oranges `#FF8C42`/`#D65A2E`, warm whites `#FFD9A0`/`#F5E9D2`). No cool or fluorescent colors. Pockets of light in darkness — stalls and lanterns are the light sources, everything else falls to shadow. Heavy vignette + animated film grain on top.
- **Type:** Fraunces (signage, card titles), Karla (body, UI). No pixel fonts.
- **Scale:** pedestrians are full human scale against the stalls (waist at counter height); Franklin is genuinely dog-sized.
- **Animation rules:** all walk cycles are distance-driven (stride phase advances with ground covered — no foot-sliding). `prefers-reduced-motion` must disable ambient motion (grain shift, bokeh drift, foreground passer-by, lantern flicker) but never player-initiated movement.
- **Cast:** the crowd is six silhouette archetypes with warm rim light (two-pass draw: warm copy offset toward the nearest light, dark body on top): tall man (long coat, pockets), stooped elderly woman (headscarf, cane, half speed), mother + child holding hands (child's shorter legs step faster), ponytail woman with swinging shopping bag, backpacker in beanie, man in cap. A large blurred figure occasionally crosses the extreme foreground.
- **Franklin:** anatomically a blue merle Shetland sheepdog walking around in the nightmarket. Almond eyes, small ears with folded tips, white mane frill with tufted edges, tucked belly, fluffy rear pants, hocked rear legs, slim legs, low bushy tail with white tip, warm rim light on his back.

## Current state

Everything lives in one file, `night-market-v3.html`: vanilla JS + Canvas at 1600×900 internal resolution, zero dependencies beyond two Google Fonts. Read it fully before changing anything. All content is in the `STALLS` and `DIRECTORY` arrays; the crowd is in `ARCHETYPES`; Franklin is `drawFranklin()`.

## Engineering rules

- Keep it dependency-free vanilla JS/Canvas unless a task genuinely demands more. If we outgrow one file, migrate to Astro with the canvas scene as an island — ask before restructuring.
- Target: Cloudflare Pages, custom domain angelasanturbano.com (currently on WordPress — cutover is a roadmap item).
- Every change must preserve: keyboard controls (arrows/WASD, Esc), tap-to-walk with auto-open, the menu button, reduced-motion support, and focus management on the dialog card.
- Performance budget: 60fps on a mid-tier laptop, smooth on mobile Safari. Profile before and after anything touching the render loop.
- Work one feature at a time. Propose the approach in 2–3 sentences before writing code. After each change, list what to manually test.

## Roadmap (roughly in order)

1. **Mobile polish** — portrait layout, touch ergonomics, canvas perf on iOS Safari
2. **Real content pass** — final bio copy, reorg essay URL, project screenshots/demo links inside the cards
3. **SEO + sharing** — meta tags, OG image (a still of the market), favicon (Franklin), semantic fallback content for crawlers, page title/description
4. **Accessibility audit** — screen-reader path through the menu, focus trap on the card, contrast check on card text, make sure no text runs over the borders
5. **Ambience** — optional market soundscape with a mute toggle (off by default), Franklin idle animations (sniffing, sitting when idle >10s)
6. **Depth** — subtle parallax between skyline / lantern string / stalls / street
7. **Deploy** — repo, Cloudflare Pages, DNS cutover from WordPress, redirect any old URLs worth keeping
8. **Later** — a fifth stall for "Now" (what I'm currently exploring), analytics (privacy-friendly, e.g. Plausible), AI-generated painted background layers if we want the final photorealism jump

