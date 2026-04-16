# Changelog

All notable changes to the Οργανική Ονοματολογία MuLERMoC.

---

## [v37] — 2026-04-16

**Major refactor:Algorithmic main chain (+ UI improvements)**

### Core logic
- **Tier 2b tie-breaker**: double bonds beat triple bonds in `fCalcMainChain` and `fCalcMainChain3D` (IUPAC rule 2b compliance)
- **Algorithmic main chain mode** (`mainChainMode = 'algorithmic'`): main chain now computed entirely by the algorithm by default; user can switch to `'data'` mode via the settings panel

### UI — settings panel
- Gear button (`#viewerSettingsBtn`) added to middle column `.panelTitle`; toggles animated dropdown (`#viewerSettingsPanel`) via `fToggleViewerSettings()`
- Outside-click listener closes the panel automatically
- Chain mode radio (Από δεδομένα / Αλγοριθμικά) moved inside settings panel, wrapped in `.radioGroupContainer` for correct deselection logic
- Tooltip on gear button: left-pointing (avoids clipping by right column), `z-index: 400`

### UI — teaching layer
- Mode-switch (2D ↔ chain view) now calls `fShowNameAnalysis()` — name component boxes refresh on every mode change
- `.selected` name component box preserved across rebuilds via `_modeToCompId` reverse lookup in `fShowNameAnalysis`

### UI — CSS (`jsme-nick-37.css`)
- Tap-target sizing: `.settingsBtn` padding `6px 8px`, `.settingRow` min-height `36px`, `.dropLi` min-height `36px` with flex align-center
- Unified UI text size: `.radioCheckContainer`, `.checkBoxContainer`, `#dropLabel`, `.dropLi` all set to `0.85rem`
- `#viewerCol` changed from `overflow: hidden` → `overflow: visible` — fixes dropdown and tooltip clipping

---

## [v36] — 2026-04-16

- Responsive viewer resizing: `fResizeViewers()` in `mulermoc-nom-molview-36.js`
  - Listens to `window resize` (debounced 150ms)
  - On small landscape screens (viewport height < 430px): caps each viewer at 30% of viewport height
  - Resizes JSmol applet and JSME SVG div together to keep aspect ratios
  - Triggers once on JSmol ready (`jmol_isReady` hook + 300ms delay)

---

## [v35] — 2026-04-16

**Major refactor: monolithic JS split into 4 files**

- `mulermoc-nom-core-35.js` (943 lines) — pure analysis engine, no DOM or jQuery
  - All analysis globals declared at top level
  - `fAnalyseStructure`, `fDetectMolType`, `fGuessName` (2D)
  - `fAnalyseStructure3D`, `fDetectMolType3D`, `fGuessName3D`, `fFetchAndParse3D` (3D, async SDF)
  - `fInitNamingProps`, `fInitProps`
- `mulermoc-nom-molview-35.js` (1325 lines) — viewer layer (JSME, JSmol, Snap.svg, jQuery)
  - `jsmeOnLoad`, `fInitData`, `fSelectMol`, `fLoadMol2D/3D`, `fUpdateSVG`
  - `fHighlightFG`, `fHighlightFG3D`, `fShowNumbering`, `fClearHighlights`
  - `fSave2DPng`, `fSaveJmolPng`, `fUpdateDiagr2DButton`
  - SVG icon constants: `svgSpeaker`, `svgMute`, `svgStop`, `svgPlay`
- `mulermoc-nom-teaching-35.js` (547 lines) — teaching layer
  - `fInitTheory`, rule text/tables, `$(document).ready` jQuery event handlers
  - `fSpeakGreek`, `fNarrateRule`, `fShowRuleTheory`, `fShowNameAnalysis`, `fExplainNameComp`
- `jsme-nick-nomeclature-moc2-data_35.js` (3846 lines) — all molecule data
  - `nameExamples` object: 59 molecules with `formula`, `mainChain`, `mainChain_E`, `mainChain3D`, `moveto`
  - 2D SMILES-like strings (`*_2D`, `*_2D_E`, `*_diagr2D`) and 3D SDF file paths

---

## [v34] — 2026-04-13

- (Version created; details carried from v33 refactor work — see v33 entry)

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

