# Οργανική Ονοματολογία — MuLERMoC

Greek IUPAC organic chemistry SPA (Single-Page Application) — educational module for naming organic compounds.

**Live:** [https://nick-charistos.github.io/organic-nomenclature-2/](https://nick-charistos.github.io/organic-nomenclature-2/)  
**Repo:** [https://github.com/nick-charistos/organic-nomenclature-2](https://github.com/nick-charistos/organic-nomenclature-2)

---

## Stack

- **jQuery** 3.7.1
- **JSME** — 2D molecule editor/viewer
- **JSmol** — 3D molecule viewer
- **Snap.svg** — SVG manipulation
- **Web Speech API** — Greek TTS narration

---

## Current Version: 33

| File | Description |
|------|-------------|
| `nomenclature_moc2_1_RC-33.html` | Main entry point |
| `css/jsme-nick-33.css` | All styles |
| `js/jsme-nick-nomeclature-moc2-33.js` | All app logic (~3000 lines) |
| `js/jsme-nick-nomeclature-moc2-data_6.js` | Minimal molecule data file |

`index.html` redirects to the current version automatically.

---

## Features

- Draw or select organic molecules via JSME 2D editor
- 3D structure display via JSmol with ball-and-stick / spacefill / sticks modes
- Algorithmic IUPAC name generation (Greek):
  - Functional groups: carboxylic acids, aldehydes, ketones, alcohols, amines, nitriles, nitro, halogens
  - Unsaturated bonds (alkene, alkyne, diene)
  - Multiple substituents with correct locant assignment
- Name analysis panel: colour-coded breakdown of each name component
- Atom/bond highlighting: clicking a name component highlights the corresponding atoms in 2D and 3D
- Rule theory panel: IUPAC rules displayed per detected compound class
- TTS narration: rules and name analysis read aloud in Greek (prefers female voice)
- PNG export: 2D and 3D images with assembled name
- Responsive drop-down menu for 3D visualisation mode
- Google Analytics tracking

### In Progress
- Algorithmic main chain detection (currently data-driven)

---

## Previous Versions

| Version | HTML | JS | CSS |
|---------|------|----|-----|
| 32 | `nomenclature_moc2_1_RC-32.html` | `jsme-nick-nomeclature-moc2-32.js` | `jsme-nick-32.css` |
| 31 | `nomenclature_moc2_1_RC-31.html` | `jsme-nick-nomeclature-moc2-31.js` | `jsme-nick-31.css` |

---

## Key Function Reference (v33)

| Function | Approx. Line | Purpose |
|----------|-------------|---------|
| `fInitData()` | ~50 | Initialise molecule data and `nameMainCompObj3` |
| `fDetectMolType()` | ~200 | Detect functional groups from SMILES |
| `fGuessName()` | ~640 | Build IUPAC name components |
| `fShowNameAnalysis()` | ~1416 | Render name analysis panel |
| `fShowRuleTheory()` | ~1330 | Display rule theory |
| `fNarrateRule()` | ~1340 | TTS narration of rule |
| `fSpeakGreek(text)` | ~1372 | Web Speech API wrapper |
| `fHighlightFG()` | ~2020 | Highlight functional group atoms in 2D |
| `fHighlightFG3D()` | ~2175 | Highlight functional group atoms in 3D |
| `fSave2DPng()` | — | Export 2D PNG with name |
| `fSaveJmolPng()` | — | Export 3D PNG with name |

