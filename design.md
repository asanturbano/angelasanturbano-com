# The Notebook — Design Guidelines

## The one-line brief

A notebook open on a walnut desk under a single lamp, seen from the front of the desk at a gentle angle. A fountain pen writes Angela's name and a table of contents in blue-black ink on vellum; below it, the same pen draws Franklin in pen and ink. The visitor can turn the lamp up or down and switch on the rain. Everything about the craft should feel like a real desk on a real evening — and the work should be two clicks away for anyone in a hurry.

## Design principles

1. **The page is the interface.** Navigation is the table of contents; controls are objects on the desk (the lamp, the radio, a ribbon bookmark). No floating toolbars, no hamburger, no modal dialogs.
2. **Ink is earned.** Handwriting is for short phrases only: the name, contents entries, section titles, margin notes. Anything read at length is printed. If a visitor has to decipher cursive to learn something, it's wrong.
3. **Write at the speed of a hand.** The pen moves like a pen: steady, slower through curves, lifting between words, dotting the i's and crossing the t's after finishing the word. If it feels like a progress bar, slow it down and give it a physical reason.
4. **One light.** The lamp is the only light source. Light falls off with distance from it; the far corner of the desk is in shadow. Interactive emphasis comes from the pen (it underlines) and from ink, never from glows, outlines, or color swaps.
5. **Translucency is the signature.** Vellum lets the next page show faintly through. Use it: the ghost of the section beneath, a hint of what's coming. More lamp, more show-through.
6. **Charm lives in specificity.** A pooled dot of ink where the nib first touches. Ink that dries from glossy to matte. Franklin's tongue out mid-run, exactly as in the photo. Generic choices are forgettable; specific ones get mentioned in intro calls.
7. **Never lock the door.** Any click or key during the opening finishes it instantly. Contents entries are clickable the moment they're written. Return visits skip the opening. Every section is reachable with keyboard, on a five-year-old phone, with motion turned off, and with the lamp at its dimmest. A recruiter in a hurry is a first-class user.

## The scene

- **Camera:** sitting at the front of the desk, looking down at about 32° from overhead (about 22° on phones) — enough to see that the lamp stands up off the desk, gentle enough that writing stays legible. The opening starts straight overhead and close on the closed notebook, then pulls back and tilts once, as the cover opens, revealing the lamp. The camera doesn't move after that. (For review, `?tilt=N` overrides the angle.)
- **The lamp:** a brass architect's lamp — a beveled, weighted base behind and left of the notebook, a jointed arm, and a conical enamel shade (blue-black, like the ink) angled down toward the page, with lamplight catching the lip of its rim. A cone, not a dome: seen from above, a dome reads as a ball.
- **Layout (desktop):** the open notebook sits centered. The lamp stands off the top-left corner — a right-handed writer keeps the lamp on the left so the hand doesn't shadow the page, and the pen comes in from the right. The lamp's cord runs down the left side of the desk, with the dimmer on it. The pen rests on the desk to the right of the notebook; a small radio will sit in the bottom-right corner.
- **The spread:** the left side is the inside of the front cover, where the name is written — the way you'd write your name inside a new notebook. The first page, on the right, holds the contents.
- **Layout (phone, portrait):** a single page fills the width (the notebook is shown one page at a time). The camera opens on the name page, then — once the name is written — pans across to the contents page and rests there, since the contents are the navigation. The lamp sits in the top-left corner, the dimmer at the bottom left, and the radio will tuck into the bottom right.
- **The ribbon bookmark:** a cloth ribbon hangs from the notebook's spine. On any section page, it is the way back to the contents (as are Esc and the browser's Back button).

## Color

- **Desk:** dark walnut — `#241912` (shadow) to `#3A2A20` (lit), with a fine grain.
- **Vellum:** `#EFE9DC`, slightly translucent, with faint fibers. Sheets beneath show through.
- **Ink (blue-black):** `#1B2433` when dry; `#22304A` with a soft sheen while wet.
- **Lamp light:** warm `#FFD9A0` at the center of the pool, falling off to the desk's shadow tones.
- **Ink wash:** the same blue-black, diluted — about 15–45% strength — for Franklin's markings and shadows. No other pigment anywhere.

**Rules:** no pure white (`#FFFFFF`) and no pure black (`#000000`). The only saturated element on the page is ink. No accent colors for UI — links are ink, emphasized by the pen.

## The lamp

- Brightness ranges from 25% to 100%; the default is 70%. The dimmest setting is lamplight turned low, never darkness — body text stays at a contrast ratio of at least 4.5:1 at every setting.
- Brightness changes three things together: the size and warmth of the light pool, how far the desk falls into shadow, and how much the vellum shows through (ghosted pages at about 6% opacity when dim, about 14% when bright).
- Controls: click or tap the lamp's shade to toggle between the visitor's last setting and 25%, or slide the dimmer on the lamp's cord. (A pull chain wouldn't read from the camera's angle, so the dimmer lives on the cord.) For keyboard and screen readers, the shade is a labeled button and the dimmer is a real slider with a label.
- The setting is remembered in the visitor's browser.

## Paper (vellum)

- Each page is a sheet stacked on the ones beneath it, offset by a pixel or two at the edges.
- The ghost of the next page is the real content of that page, rendered faintly — not decoration.
- Pages have clean edges (vellum isn't deckled) and a slight sheen near the lamp.

## Handwriting and the pen

- **Style:** EMS Brush, a single-stroke script derived from Alex Brush (SIL Open Font License) — flowing and connected, with a sweeping capital A. Chosen in the step 2 handwriting test over Capitol and Neato.
- **Technique:** each phrase is a set of single-stroke SVG paths, precomputed. The visible ink line is drawn with a broad nib held at a fixed angle (about 35°), so downstrokes run thick and side strokes thin, roughly 5:1. The contrast should be visible at a glance, not just up close.
- **Speed:** two tempos. **The name is the showpiece:** each stroke is written at a quarter of a brisk hand's speed, so "Angela Santurbano" takes about 7.5 seconds. Pen lifts between strokes stay natural (scaled by only half as much) — a slow writer forms letters slowly but doesn't hover between them. **Everything else** (contents, section titles, margin notes) is written at about 7 letters per second. The i-dots and t-crosses come after the word, as a person would write them.
- **Ink behavior:** a small pooled dot where the nib first touches down; the line dries from wet to matte over about 1.2s.
- **The pen:** a fountain pen, cap posted, nib touching the paper at the stroke's leading point, tilted toward the lower right. It casts a soft shadow that grows when the pen lifts. When it isn't writing, it rests in the margin.
- **Hover and focus:** on a contents entry or link, the pen glides over and writes an underline beneath it (and erases nothing — the underline fades when focus leaves).

## Type

- **Handwriting:** the precomputed script paths above. Never set as a webfont for running text.
- **EB Garamond:** everything printed — the subtitle under the name, section bodies, notes, dates, the lamp and sound labels. Body at 17–19px, line height about 1.55. Small caps, lightly letterspaced, for labels.

Two voices, no more: the hand and the printed page.

## Motion

Motion is the experience here, so it is choreographed as one timeline (built with the Motion library), not a pile of separate transitions.

### The opening (first visit only)

| Time | What happens |
|---|---|
| 0.0s | Close on the closed notebook; the lamp is already on. |
| 0.4–1.4s | The cover swings open; the camera pulls back to show the lamp's pool. |
| 1.5–9.0s | The pen slowly writes "Angela Santurbano," then a short underline flourish. |
| 9.0s | The printed subtitle fades in: *builder who ships with AI · San Francisco*. |
| 9.3–11.7s | The pen writes, at the quicker tempo, "Contents" and the four entries, each with a dotted leader (the pen taps out each dot) and a lowercase roman numeral, i–iv — a cursive capital I reads as a J. Each entry becomes clickable as soon as it's written. |
| 11.7–13.5s | The pen draws Franklin below the contents; ink washes bleed into her markings. |
| 13.5s | The pen comes to rest in the margin. |

Any click or key during the opening finishes it instantly, and a small printed line at the foot of the desk — *click anywhere to skip* — fades in two seconds into the opening so first-time visitors know. Return visits land on the finished page; the same line then reads "watch it written" and replays the opening.

### Everywhere else

- **Opening a section:** the pen ticks the entry; the top sheet lifts (a soft spring, about 0.5s) and slides away up and to the left, its shadow widening as it rises. The section page beneath — already faintly visible — comes into full view.
- **Section page:** the pen writes the title (about 0.9s), then printed lines fade up one after another, about 40ms apart.
- **Returning to the contents:** the sheet lays back down, the reverse of the lift.
- **Ambient motion** (barely noticeable — if a visitor can name the animation, it's too strong): a faint flicker in the lamp's filament, rain streaks in the window-light on the desk when the rain is on, the pen's slow idle sway in the margin.

### Reduced motion

`prefers-reduced-motion` shows every page in its finished state: no writing, no drawing, no cover, no sheet-lift, no ambient motion. Sections switch instantly. The lamp and sound still work, because the visitor initiates them.

## Franklin

- **Source:** the reference photo (`reference/franklin-photo.jpg`, local only and gitignored — never commit it) — mostly white coat, black ears and head markings, a dark patch on her side, mid-run toward the viewer with her tongue out.
- **The drawing:** pen and ink with ink wash, in the same blue-black as the handwriting. A loose, confident outline — a few broken lines where fur breaks the edge — with her black markings (ears, eye patches, the patch on her side) laid in as diluted-ink washes with soft, feathered edges that bleed into the vellum. White fur is the paper itself. It sits below the contents at about a third of the page width.
- **How it's made:** traced by hand from the reference photo — shapes taken from the photo's outlines, then cleaned up so it reads as drawn, not auto-traced. Only the finished SVG is committed.
- **Drawing in:** the pen draws the outline first (about 0.8s), lifting where the line breaks; then the washes bleed outward, lightest first, darkest last (about 1.2s). A few quick fur strokes land at the end.
- Franklin is the only image on the page. No second illustration gets this treatment.

## Sound

- Always off until the visitor turns it on with the radio. Nothing ever autoplays.
- **Rain:** generated in code (filtered noise and scattered droplets), at a gentle default volume.
- **Pen scratch:** a faint nib-on-paper sound that follows the pen's speed, heard only while the pen writes and only when sound is on.
- The radio shows its state clearly (on or off), is a real toggle button for keyboard and screen readers, and remembers the choice.
- Audio only loads once the visitor turns sound on.

## Voice

Microcopy can sound like a notebook, but never at the cost of clarity. One flourish per surface at most; entry names, link labels, and instructions are always literal ("Projects," "Back to contents," "Lamp brightness"), never coy.

## Quality bar (check before shipping any change)

- **Squint test:** with eyes half-closed, the frame reads as one warm pool of light on a dark desk, with the page brightest.
- **Screenshot test:** any random frame looks like a photo of a real desk, not a UI.
- **Recruiter test:** a cold first-time visitor reaches all four sections in under 30 seconds.
- **Lamp test:** every page is comfortably readable at the dimmest lamp setting.
- **Listen test:** a screen reader announces the name, the contents, and each section in a sensible order, and never reads out decorative ink.
- **The Chanel rule:** after finishing anything, remove one element.
