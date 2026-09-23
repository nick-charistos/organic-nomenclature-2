# MuLERMoCs — Organic Nomenclature Learning Platform

A Greek-first interactive learning platform for organic nomenclature, built around molecular structure, naming logic, and multiple representations.

**Current working baseline:** v39  
**Main entry point:** [mulermoc-nom-39.html](mulermoc-nom-39.html)  
**Core engine:** [js/mulermoc-nom-core-39.js](js/mulermoc-nom-core-39.js)  
**Viewer layer:** [js/mulermoc-nom-molview-39.js](js/mulermoc-nom-molview-39.js)  
**Teaching layer:** [js/mulermoc-nom-teaching-39.js](js/mulermoc-nom-teaching-39.js)  
**Data set:** [js/jsme-nick-nomeclature-moc2-data_39.js](js/jsme-nick-nomeclature-moc2-data_39.js)

---

## Project status

This project is currently a no-build web application built with JSME, JSmol, Snap.svg, and vanilla JavaScript. It already contains a working nomenclature engine and multiple representation modes, but it is still a legacy HTML-based implementation rather than a fully refactored product structure.

The next product iteration is being re-scoped around a clearer educational model:

- Greek-first interface
- homologous series as the primary navigation model
- rules as a secondary explanatory layer
- chemistry expansion in this order: branched molecules → ethers → esters

---

## Current stack

- **jQuery** 3.7.1
- **JSME** — 2D molecule editor/viewer
- **JSmol** — 3D molecule viewer
- **Snap.svg** — SVG manipulation
- **Web Speech API** — Greek TTS narration

---

## What exists now

### Supported baseline
- 2D molecular rendering via JSME
- 3D molecular rendering via JSmol
- Molecule menu grouped by homologous series by default
- Alternate rule-based molecule grouping
- Homologous-series groups ordered by increasing total carbon count
- Group switching preserves the selected molecule and opens its new group
- No molecule is selected when switching groups with no prior selection
- Methane is selected by default on page load
- Multiple representation modes:
  - condensed
  - expanded
  - skeletal
  - annotated skeletal
- Greek IUPAC name generation
- Name analysis and explanation panels
- Rule theory panel
- TTS narration in Greek
- PNG export for 2D and 3D views
- Responsive menu and settings controls
- Current molecule data set for the teaching application

### v39 molecule grouping

The v39 menu classifies molecules through the existing structure-analysis
pipeline (`fAnalyseStructure()` and `fDetectMolType()`). Each molecule receives
a classification snapshot containing its functional groups, homologous-series
key, bond-series type, and total carbon count.

The default menu groups molecules by homologous series. Rule grouping remains
available as an alternate mode. Special series currently include amino acids,
hydroxy acids, keto acids, hydroxy nitriles, and oxo carboxylic acids.

Within each homologous-series group, molecules are ordered by increasing total
number of carbon atoms. The optional `mainChain` data is not required for this
menu ordering.

### Current implementation architecture
The project uses a split-layer architecture:

- **Core logic**: analysis + naming
- **Viewer layer**: JSME / JSmol / Snap.svg integration
- **Teaching layer**: rule explanations, narration, UI wiring
- **Data layer**: molecule definitions and structural data

This makes the codebase a workable foundation for the restart and expansion.

---

## Restart and expansion plan

### Product principle
The next version should not be organized primarily around rule-by-rule teaching. Instead, the platform should be organized around:

- homologous series
- molecule browsing by family
- molecule detail view
- naming analysis
- optional rule explanations

### Immediate chemistry roadmap
1. **Branched molecules**
   - alkyl substituent recognition
   - multi-branch chain selection
   - corrected locant logic
   - validation examples

2. **Ethers**
   - detection and classification
   - naming logic
   - examples and edge cases

3. **Esters**
   - acid-derived and alcohol-derived grouping
   - full IUPAC naming logic
   - validation dataset

### After the chemistry expansion
- add a first learning interaction layer
- add atom/bond click targets
- add one exploration mode
- then consider quiz features and research instrumentation

---

## Deferred scope

These remain explicitly out of the first restart milestone:

- full research-mode architecture
- participant/session logging
- quiz SPA
- condition locking
- CSV export
- transfer-test data set
- server-side classroom management
- rings and aromatics
- full reaction module

These belong to a later product phase.

---

## Key project documents

- [DEVELOPMENT-PLAN.md](DEVELOPMENT-PLAN.md)
- [RESEARCH-PLAN.md](RESEARCH-PLAN.md)
- [PROJECT-PLAN.md](PROJECT-PLAN.md)
- [PROJECT-PLAN-GR.md](PROJECT-PLAN-GR.md)
- [CHANGELOG.md](CHANGELOG.md)

These plans describe the research and product ambitions, but the current implementation should be treated as the working v39 baseline rather than as a fully finished research platform.

---

## Technical notes

### Important observations
- The workspace contains multiple historical versions, including v35-v39 snapshots.
- The project plans still describe older intended milestones and should be reconciled with the real v39 baseline.
- The chemistry engine should be validated before expanding into more complex categories.
- Known engine issues still need explicit testing, especially around ester and tertiary-amine detection paths.

---

## Future goal

The target product is not only a naming tool, but a series-based chemistry learning environment that helps students explore:

- molecular family
- naming patterns
- structural logic
- representation transitions
- explanation by structure, not only by rules

This makes the platform more pedagogically coherent and more scalable than a strict rule-first interface.

---

## Repository status summary

- Working baseline: **v39**
- Main focus: **stable learning app + chemistry expansion**
- Near-term goal: **branch logic, ethers, esters**
- Product model: **homologous series first**
- Rules: **secondary explanatory layer**
- Research layer: **deferred**


