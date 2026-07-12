# Night Market — Design Guidelines

## The one-line brief

The site should feel like standing in a Taiwanese night market photographed and underexposed: pockets of warm light, swarms of people walking around in front of the stalls, and a small shetland sheepdog that the user can lead from stall to stall that is at the closest foreground. The perspective is from the street level and there are quite a few stalls, only four are clickable and the dog can walk to and stand in front of.

## Design principles

1. **Light is the hierarchy.** There is no visual hierarchy from size or color contrast in the usual sense — attention goes where the light is. The most important thing on screen at any moment should be the most lit. If something needs emphasis, light it warmer or brighter; don't make it bigger or add a border.
2. **Darkness is a feature.** At least the background should be near-black. If a new element makes the scene feel "brighter overall," it's wrong.
3. **The camera is honest.** Effects are photographic, never digital: vignette, grain, bloom, bokeh, rim light, shallow-focus blur. Nothing glows in a way a lens wouldn't produce. No drop shadows that don't come from a light source, no gradients that don't describe a surface.
4. **Everything moves at the speed of physics.** Feet match ground speed. Lanterns sway like they have mass. Children take quicker steps than adults because their legs are shorter. If a motion looks "animated" rather than "filmed," slow it down and tie it to a physical cause.
5. **Charm lives in specificity.** The elderly woman shuffles at half speed. Franklin's ears tip over at exactly the top third. The child trails slightly behind his mother. Generic elements (a person, a dog, a lantern) are forgettable; specific ones get mentioned in intro calls. When adding anything, ask: what would make this particular?
6. **Never lock the door.** The adventure is optional. Every piece of content must be reachable in two clicks through the Market Directory, with keyboard, on a five-year-old phone, with motion disabled. A recruiter in a hurry is a first-class user, not a fallback case.

## Color

The palette is tungsten and nothing else:

- **Deep blacks:** `#060409` (background), `#030208` (sky top)
- **Reds:** `#E8502E`, `#C73E2A` (lanterns, accents)
- **Oranges:** `#FF8C42`, `#D65A2E` (glow, bloom, rim light)
- **Warm whites:** `#FFD9A0` (lit signage), `#F5E9D2` (UI text, warm paper)
- **Card paper:** `#F8EFDC` → `#EBDBBC` gradient, ink `#1C1310`

**Rules:** no blues, greens, purples, or neutral grays anywhere in the scene (the sky may carry a barely-perceptible cool cast at the very top, nothing more). No pure white (`#FFFFFF`) and no pure black (`#000000`) — everything warm-shifted. If a color looks acceptable under fluorescent office lighting, it's too clean for this site.

## Light

Light sources are diegetic — everything that glows exists in the scene: lantern strings, string lights on awning hems, a bare bulb inside each stall, spillover on the pavement. Each source produces three things: a bloom halo, a pool or reflection on the ground below it, and rim light on whatever stands near it. Rim light is the signature move: dark figures get a 2px warm sliver on their lit edge, nothing more. Interactive states use light too — the nearby stall's sign warms up and its interior glow intensifies; nothing ever gets an outline, underline, or color-swap to indicate hover/proximity.

## Typography

- **Fraunces (serif):** stall signage, card titles, the gate header. It carries the hand-painted-sign warmth. Never below 15px.
- **Karla (sans):** everything read at length — card body, notes, hints, buttons.

Signage is letterspaced small caps; body text is sentence case. Two families, no more. Pixel, mono, and geometric-modernist faces are all off-brand — this market is analog.

## Motion

Ambient motion should be barely noticeable: lantern sway ±4px on a ~1s period, grain shifting a few pixels, bokeh drifting slowly. If a viewer can name the animation, it's too strong. Character motion follows the distance-driven rule (stride phase advances with ground covered). `prefers-reduced-motion` kills all ambient motion and transitions but never blocks player-initiated movement — Franklin still walks when you press the key. Nothing autoplays sound, ever; audio ships muted with a visible toggle.

## The cast

Silhouettes only — no faces, no clothing color, no detail beyond profile. Identity comes entirely from posture, gait, and props (a cane, a bag, a backpack, a held hand). Figures are full human scale against the stalls: counter at the waist, head near the hanging signs. Franklin is the only fully rendered character; that contrast — one warm detailed creature among shadows — is deliberate, and no second character should ever get his treatment.

## UI surfaces (cards, buttons)

The menu cards are the one place the site becomes "product UI," and they should feel like objects from the market: warm paper, a fabric-colored stall tag, serif title, italic subtitle in the market's voice. Links are the only saturated element on the card (`#A63B22`). Buttons are pill-shaped, warm amber, dark text. No card ever contains more than ~6 items — if content outgrows a card, it links out instead of scrolling forever.

## Voice

Microcopy stays inside the market metaphor but never at the cost of clarity: "made in small batches, shipped anyway," "pull up a chair," "notes, intros, and good leads welcome." One metaphorical flourish per surface, maximum — the title or the subtitle can be playful, but link labels and instructions are always literal ("↑ browse," "Market Directory," never "peruse the wares").

## Quality bar (check before shipping any change)

- **Squint test:** with eyes half-closed, the frame should read as 4–5 warm light pools on black.
- **Screenshot test:** any random frame should look like a photo someone took, not a UI.
- **Recruiter test:** cold visitor to all four content areas in under 30 seconds via the Directory.
- **The Chanel rule:** after finishing anything, remove one element.

