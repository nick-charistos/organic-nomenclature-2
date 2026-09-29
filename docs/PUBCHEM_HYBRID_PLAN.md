# PUBCHEM_HYBRID_PLAN.md

## Hybrid PubChem/Wikipedia Integration Plan

### Data Structure (jsme-nick-nomeclature-moc2-data_40.js)

Add to each molecule in `nameExamples`:
```javascript
methane: {
  formula: "CH4",
  mainChain: [1],
  mainChain_E: [1],
  mainChain3D: [1],
  moveto: "...",
  // NEW FIELDS:
  pubchemCID: 297,           // number | null | undefined
  wikipediaSlug: "Methane",  // string | null | undefined
}
```

| Value | Meaning |
|-------|---------|
| `undefined` (absent) | Not yet checked → triggers dynamic fallback |
| `null` | Explicitly verified: **not in PubChem/Wikipedia** |
| `number` / `string` | Verified CID / slug — use directly |

---

## Core Module: `js/pubchem-lookup.js` (NEW FILE)

### Features
- In-memory cache (Map) with 30min TTL
- Request deduplication via `pendingRequests` Map
- Rate limiting: 250ms between requests (4/sec, under PubChem's ~5/sec)
- Serial request queue (FIFO)
- Stale-mol guard pattern (like `fFetchAndParse3D`)
- Error caching (short TTL)

### Exported API
```javascript
PubChemLookup.getPubChemData(molKey, molData)  // Returns LookupResult
PubChemLookup.getWikipediaData(molKey, molData, pubchemResult)
PubChemLookup.clearCache()
PubChemLookup.getCacheStats()
```

### LookupResult Type
```javascript
{
  cid: number|null,
  iupacName: string|null,
  wikipediaSlug: string|null,
  source: "stored"|"dynamic"|"not-found"|"error",
  error: string|null
}
```

---

## Hybrid Lookup Logic

```
getPubChemData(molKey, molData):
  1. If molData.pubchemCID !== undefined:
       - If null → return {source: "stored", error: "Not in PubChem (verified)"}
       - If number → fetch IUPAC + Wikipedia slug from CID, return {source: "stored"}
  2. Else (undefined):
       - Get SMILES from JSME (jsmeNomeclatureApplet.smiles())
       - fetchCIDFromSMILES(smiles, molKey) → dynamic lookup
       - Returns {source: "dynamic" | "not-found" | "error"}

getWikipediaData(molKey, molData, pubchemResult):
  1. If molData.wikipediaSlug !== undefined → return stored (or not-found if null)
  2. Else if pubchemResult.cid → fetchWikipediaSlugFromCID(cid)
  3. Else → not-found
```

---

## Integration in mulermoc-nom-molview-40.js

### Load Order (HTML)
```html
<script src="js/pubchem-lookup.js"></script>
<script src="js/jsme-nick-nomeclature-moc2-data_40.js"></script>
<script src="js/mulermoc-nom-molview-40.js"></script>
<script src="js/mulermoc-nom-teaching-40.js"></script>
```

### In fSelectMol()
```javascript
function fSelectMol() {
  // ... existing code ...
  fLoadMol2D();
  fLoadMol3D();
  fFetchAndParse3D();
  // ... existing code ...
  fFetchExternalLinks();  // NEW
}
```

### New Functions
```javascript
let currentPubChemRequestId = 0;

async function fFetchExternalLinks() {
  const molKey = selectedMol;
  const molData = nameExamples[molKey];
  if (!molData) return;

  const requestId = ++currentPubChemRequestId;
  fUpdateExternalLinksUI({ state: "loading" });

  try {
    const pubchemResult = await PubChemLookup.getPubChemData(molKey, molData);
    if (requestId !== currentPubChemRequestId || selectedMol !== molKey) return;

    const wikiResult = await PubChemLookup.getWikipediaData(molKey, molData, pubchemResult);
    if (requestId !== currentPubChemRequestId || selectedMol !== molKey) return;

    fUpdateExternalLinksUI({ state: "done", pubchem: pubchemResult, wikipedia: wikiResult });

    // Optional: cache dynamic results back to in-memory data
    if (pubchemResult.source === "dynamic" && pubchemResult.cid && molData.pubchemCID === undefined) {
      molData.pubchemCID = pubchemResult.cid;
    }
    if (wikiResult.source === "dynamic" && wikiResult.slug && molData.wikipediaSlug === undefined) {
      molData.wikipediaSlug = wikiResult.slug;
    }
  } catch (e) {
    if (requestId !== currentPubChemRequestId) return;
    fUpdateExternalLinksUI({ state: "error", error: e.message });
  }
}

function fUpdateExternalLinksUI(data) {
  const $pubchemLink = $("#pubchemLink");
  const $wikiLink = $("#wikipediaLink");
  const $status = $("#externalLinksStatus");

  // ... update links, badges, status text based on data.state ...
  // Shows: "Αποθηκευμένο" (green) or "Δυναμικό" (blue) badges
  // Greek messages: "Φόρτωση συνδέσμων...", "PubChem: αποθηκευμένο | Wiki: δυναμικό", etc.
}
```

---

## UI (HTML + CSS)

### HTML (in molecule info panel)
```html
<div id="externalLinksPanel" class="external-links-panel">
  <div id="externalLinksStatus" class="ext-links-status"></div>
  <div class="ext-links-row">
    <a id="pubchemLink" class="ext-link pubchem-link" target="_blank" rel="noopener">
      <svg class="ext-icon" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
      <span>PubChem</span>
      <span class="source-badge"></span>
    </a>
    <a id="wikipediaLink" class="ext-link wiki-link" target="_blank" rel="noopener">
      <svg class="ext-icon" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
      <span>Wikipedia</span>
      <span class="source-badge"></span>
    </a>
  </div>
</div>
```

### CSS
```css
.external-links-panel {
  margin-top: 12px; padding: 8px 12px;
  background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;
  font-size: 13px;
}
.ext-links-status { min-height: 18px; margin-bottom: 6px; color: #6c757d; font-style: italic; }
.ext-links-status.loading { color: #0d6efd; }
.ext-links-status.done { color: #198754; font-style: normal; }
.ext-links-status.error { color: #dc3545; font-style: normal; }
.ext-links-row { display: flex; gap: 12px; flex-wrap: wrap; }
.ext-link {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px; background: #fff; border: 1px solid #dee2e6;
  border-radius: 4px; color: #212529; text-decoration: none;
  transition: all 0.15s ease; position: relative;
}
.ext-link:hover { background: #e7f1ff; border-color: #0d6efd; color: #0d6efd; }
.ext-link.hide { display: none; }
.ext-icon { width: 16px; height: 16px; fill: currentColor; flex-shrink: 0; }
.source-badge {
  display: inline-block; font-size: 10px; padding: 1px 5px;
  border-radius: 3px; font-weight: 600; text-transform: uppercase;
}
.ext-link.source-stored .source-badge { background: #d1e7dd; color: #0f5132; }
.ext-link.source-stored .source-badge::after { content: "Αποθηκευμένο"; }
.ext-link.source-dynamic .source-badge { background: #cfe2ff; color: #084298; }
.ext-link.source-dynamic .source-badge::after { content: "Δυναμικό"; }
```

---

## Future Migration Path (SMILES-Only Import)

1. **Phase 1 (Now)**: Deploy hybrid. Undergrads add `pubchemCID` for common molecules.
2. **Phase 2**: Cache warms via student usage.
3. **Phase 3**: Run batch script to pre-populate cache for all molecules:
   ```javascript
   for (const [key, mol] of Object.entries(nameExamples)) {
     const smiles = jsmeNomeclatureApplet.smiles(); // after loading each
     await PubChemLookup.fetchCIDFromSMILES(smiles, key);
   }
   // Export cache to localStorage / static JSON
   ```
4. **Phase 4**: Load cache at startup → zero dynamic calls for known molecules.
5. **Phase 5**: Remove `pubchemCID` from data schema; dynamic becomes primary.

---

## Key Technical Safeguards

| Safeguard | Implementation |
|-----------|----------------|
| Rate limiting | 250ms min interval, serial queue |
| Deduplication | `pendingRequests` Map returns same Promise for concurrent same-SMILES calls |
| Stale-mol guard | `currentPubChemRequestId` increments each call; checked after every `await` |
| Explicit nulls | `pubchemCID: null` = verified absent, no network call |
| Error states | Distinct: "Network error" / "Not in PubChem" / "Verified absent" |
| Caching | 30min TTL in-memory; optional localStorage persistence |

---

## Files to Modify

| File | Changes |
|------|---------|
| `js/pubchem-lookup.js` | **NEW** — Core module |
| `jsme-nick-nomeclature-moc2-data_40.js` | Add `pubchemCID`, `wikipediaSlug` to each molecule |
| `mulermoc-nom-molview-40.js` | Add `fFetchExternalLinks()`, `fUpdateExternalLinksUI()`, call from `fSelectMol()` |
| `mulermoc-nom-teaching-40.js` / HTML | Add link panel HTML + CSS |

---

## Testing Checklist

- [ ] Molecule with stored CID → instant link, "Αποθηκευμένο" badge
- [ ] Molecule without CID → loading → dynamic link, "Δυναμικό" badge
- [ ] Molecule with `pubchemCID: null` → no link, "δεν βρέθηκε (επιβεβαιωμένο)"
- [ ] Rapid switching → no UI flicker / wrong links (stale-mol guard)
- [ ] Network offline → graceful error state
- [ ] Cache persists across reloads (if localStorage enabled)

---

## PubChem API Endpoints Used

| Purpose | URL |
|---------|-----|
| CID from SMILES | `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{encodedSMILES}/cids/JSON` |
| IUPAC from CID | `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/IUPACName/JSON` |
| Synonyms from CID | `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON` |
| Compound page | `https://pubchem.ncbi.nlm.nih.gov/compound/{CID}` |
| Wikipedia search | `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json` |

**Critical**: SMILES must be `encodeURIComponent()`'d (handles `=`, `#`, `@`, `/`, `\`, brackets, etc.)