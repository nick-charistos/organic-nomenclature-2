# Changelog

All notable changes to the Οργανική Ονοματολογία MuLERMoC.

---

## [v33] — 2026-04-13 · `6140142`

**Major upgrade**

- 3D structure analysis: atom/bond highlighting in JSmol (`fHighlightFG3D()`)
- Minimal external data file (`jsme-nick-nomeclature-moc2-data_6.js`) — most properties now algorithmically generated
- All compound properties (FG detection, locants, substituents, unsaturation) algorithmic — only main chain remains data-driven (TBD)
- Fix: wrong halogen atom highlighted in 2D/3D for molecules with two different halogens (e.g. 2-βρωμο-3-χλωροβουτάνιο) — sort in `fHighlightFG`/`fHighlightFG3D` now uses canonical `nameMainCompObj3.halogen.substitute` key order as tiebreak

---

## [v32] — 2026 · `180e26f`

- TTS rule narration: `fNarrateRule()` reads selected rule aloud in Greek
- Greek TTS helper `fSpeakGreek(text)` — prefers female voice (Eleni/Nefeli/Maria/Sofia)
- Name analysis narration: toggle + play button (`#narrateAnalysisToggle`, `#readNameBtn`)
- SVG icon constants: `svgSpeaker`, `svgMute`, `svgStop`, `svgPlay` — no emoji dependency
- Audio button on by default at page load
- Chevron accordion symbol with animated rotation
- CSS-styled tooltips with delay (no native browser tooltip)
- Drop-down menu: SVG arrow (Android-safe), larger triangle, event delegation fix, close-on-select fix
- Fix: strip dashes from TTS narration (prevent reading as "minus")
- Fix: strip standalone "C" from carbon count narration
- Fix: typo καβροξυ → καρβοξυ in carboxylicAcid substitute

---

## [v31] — earlier · `d0666ce`

- 2D/3D PNG export with assembled name boxes (`fSave2DPng`, `fSaveJmolPng`)
- Increased PNG export size to 1200px
- Fix: guard against undefined `jsmeNomeclatureApplet` in `fDeselectMol`, `fUpdateSVG`, `fClearHighlights`
- Fix: JSME NH2 highlight SVG bug (stroke-width attribute swallowing tspan content)
- Fix: page jump when selecting name component
- Radio scoping, save button alignment, checkbox/radio styles, credits links
- Auto-select first molecule on page load
- Google Analytics tracking added

---

## [Initial] — earlier · `cb66337`

- Initial upload: organic nomenclature 2 page with assets
