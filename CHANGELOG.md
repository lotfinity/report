# Changelog

Every agent must append a dated entry before finishing work.

Use this format:

```text
## YYYY-MM-DD - Agent/Task
Done:
- ...

Not done:
- ...

Verification:
- ...

Next:
- ...
```

## 2026-06-02 - Standalone Image Embedding

Done:
- Embedded the four visible report images directly into `standalones/future-park-pdf-friendly-report.html` as data URIs.
- Embedded the FireShot screenshot link target directly into the HTML as a data URI, so the `1+0 Future Park à 1.45M TL` card is self-contained.
- Regenerated `standalones/future-park-simple-report.pdf` from the embedded-image HTML.

Not done:
- Did not change the external Airbnb destinations; only the image assets were embedded.
- Did not touch the active Webflow report page.

Verification:
- Verified through CDP at `100.115.42.17:9223` that the standalone HTML has `4` images, all `complete`, with `0` scripts and `0` asset references to `../assets-rebuilt`.
- Regenerated the PDF with headless Chrome and checked `pdfinfo`: 9 pages, JavaScript none.
- Confirmed the PDF file grew to reflect the inlined assets and still renders from the standalone HTML.

Next:
- If you want the last remaining external dependencies removed, the next pass would be to inline or snapshot the linked Airbnb targets themselves, but that is a separate decision from embedding the visible images.

## 2026-06-02 - PDF Second Airbnb Link

Done:
- Linked the `Appartement meublé de 52 m2` evidence card in `standalones/future-park-pdf-friendly-report.html` directly to the provided Airbnb room URL.
- Added a visible `Ouvrir Airbnb` affordance on that second Airbnb card.
- Regenerated `standalones/future-park-simple-report.pdf` so the updated second Airbnb link/text is included.

Not done:
- Did not change the active Webflow report page.
- Did not wire the remaining non-Airbnb evidence cards.

Verification:
- Verified through CDP at `100.115.42.17:9223` that both Airbnb evidence cards resolve to their intended Airbnb URLs.
- CDP confirmed the simplified report still has `0` scripts and `0` broken images.
- Regenerated the PDF with headless Chrome and checked `pdfinfo`: 9 pages, JavaScript none.
- Checked `pdftotext` output includes `Appartement meublé de 52 m2` and `Ouvrir Airbnb`.

Next:
- Continue linking the remaining evidence cards to their chosen screenshots or external pages.

## 2026-06-02 - PDF Airbnb Direct Link

Done:
- Linked the `Comparable meublé à Esenyurt` Airbnb evidence card in `standalones/future-park-pdf-friendly-report.html` directly to the provided Airbnb room URL.
- Added a visible `Ouvrir Airbnb` affordance on that card.
- Regenerated `standalones/future-park-simple-report.pdf` so the updated Airbnb link/text is included.

Not done:
- Did not change the active Webflow report page.
- Did not wire the remaining evidence cards beyond the Airbnb and 1+0 Future Park test cards.

Verification:
- Verified through CDP at `100.115.42.17:9223` that the Airbnb card resolves to the exact provided Airbnb URL.
- CDP confirmed the simplified report still has `0` scripts and `0` broken images.
- Regenerated the PDF with headless Chrome and checked `pdfinfo`: 9 pages, JavaScript none.
- Checked `pdftotext` output includes `Ouvrir Airbnb`.

Next:
- Continue linking the remaining evidence cards to their chosen screenshots or external pages.

## 2026-06-02 - PDF Evidence Screenshot Link

Done:
- Linked the `1+0 Future Park à 1.45M TL` evidence card in `standalones/future-park-pdf-friendly-report.html` to the added FireShot Sahibinden screenshot.
- Added a visible `Ouvrir la capture Sahibinden` affordance on that card.
- Regenerated `standalones/future-park-simple-report.pdf` so the updated evidence link/text is included.

Not done:
- Did not wire the other evidence cards yet; this pass only tests the 1+0 Future Park card.
- Did not move or rename the added FireShot screenshot.

Verification:
- Verified through CDP at `100.115.42.17:9223` that the card resolves to the PNG target served from `standalones/`.
- CDP confirmed the target loads as `image/png` with dimensions `1380x3181`.
- CDP confirmed the simplified report still has `0` scripts and `0` broken images.
- Regenerated the PDF with headless Chrome and checked `pdfinfo`: 9 pages, JavaScript none.
- Checked `pdftotext` output includes `Ouvrir la capture Sahibinden`.

Next:
- Apply the same link pattern to the remaining evidence cards once the preferred screenshots are selected.

## 2026-06-02 - PDF-Friendly Report

Done:
- Created `standalones/future-park-pdf-friendly-report.html` as a simplified, single-column investor memo sourced from `index-standalone-rebuilt.html`.
- Exported `standalones/future-park-simple-report.pdf` with mobile-width pages, large text, no scripts, no forms, and only necessary evidence images/tables.
- Kept the active Webflow rebuild page unchanged.

Not done:
- Did not rewrite or simplify `index-standalone-rebuilt.html`.
- Did not add new source data beyond the existing report content.

Verification:
- Connected to CDP at `100.115.42.17:9223` with suppressed origin and inspected the active report through `http://100.74.113.44:8090/index-standalone-rebuilt.html`.
- Verified the simplified report through CDP at desktop 1100x900 and mobile 390x844: 10 sections, 0 scripts, 0 broken images, vertical scroll only.
- Saved verification screenshots at `/tmp/future-park-pdf-friendly-desktop.png` and `/tmp/future-park-pdf-friendly-mobile.png`.
- Generated the PDF with headless Chrome and checked `pdfinfo`: 9 pages, tagged PDF, JavaScript none, page size `323.04 x 660 pts`.
- Checked text extraction with `pdftotext` to confirm the document is readable and navigable.

Next:
- Use `standalones/future-park-pdf-friendly-report.html` as the source if the simplified PDF needs future copy or number updates.

## 2026-06-02 - Sahibinden Sale Search Local Modal

Done:
- Copied the provided saved Sahibinden sale-search page into `assets-rebuilt/evidence/sahibinden-future-park-sale-search-local.html`.
- Converted the `Deux achats laissent une marge` card from an external link to a modal-opening button.
- Pointed the card at the saved local sale-search snapshot with `data-modal-src`.
- Updated the second-row blueprint and restructure plan to document the modal behavior.

Not done:
- Did not remove the external Sahibinden sale-search URL from the blueprint; it remains as `external_href` for reference.
- Did not clean unrelated Pinegrow backup churn.

Verification:
- Confirmed the copied local HTML serves HTTP 200 on port 8090.
- Verified through CDP at `100.115.42.17:9223` that clicking the card opens the modal.
- CDP confirmed iframe `src` and loaded path are `assets-rebuilt/evidence/sahibinden-future-park-sale-search-local.html`.
- CDP confirmed the iframe title is `Prix des maisons en Vente sur sahibinden.com`.
- Saved screenshot at `/tmp/report-sahibinden-sale-search-local-modal.png`.

Next:
- Continue using the shared `data-modal-src` modal pattern for locally saved evidence pages.

## 2026-06-02 - Sahibinden Detail Local Modal

Done:
- Copied the provided saved Sahibinden detail page into `assets-rebuilt/evidence/sahibinden-future-park-1plus0-detail-local.html`.
- Generalized the existing modal script so each trigger can pass a `data-modal-src` iframe target.
- Converted the `1+0 Future Park à 1.45M TL` evidence card from an external link to a modal-opening button.
- Updated the second-row blueprint and restructure plan to record the local snapshot behavior.

Not done:
- Did not remove the external Sahibinden URL from the blueprint; it remains as `external_href` for reference.
- Did not clean unrelated Pinegrow backup churn.

Verification:
- Confirmed the copied local HTML serves HTTP 200 on port 8090.
- Verified through CDP at `100.115.42.17:9223` that clicking the 1+0 card opens the modal.
- CDP confirmed iframe `src` and loaded path are `assets-rebuilt/evidence/sahibinden-future-park-1plus0-detail-local.html`.
- CDP confirmed the iframe title is the expected Sahibinden listing title.
- Saved screenshot at `/tmp/report-sahibinden-local-modal.png`.

Next:
- Apply the same `data-modal-src` pattern to any future locally saved evidence pages that should open inside the report.

## 2026-06-02 - Row Finish Pass

Done:
- Replaced duplicated first-row visual assets with distinct local report/evidence assets while preserving the Webflow row structure and links.
- Updated the first-row manifests to show 12 conceptual cards and 28 unique first-row image sources.
- Rebalanced the second-row narrative: Airbnb proof, revenue math, local listing, capital plan, due-diligence listing, and fallback rent floor.
- Replaced the third-row/shop euro furniture catalog with estimative Turkish lira package pricing and updated the text hierarchy manifest.
- Updated `ROADMAP.md`, `docs/second-row-restructure-plan.md`, and row blueprints to match the active HTML.

Not done:
- Did not generate bespoke final first-row image assets under `assets-rebuilt/first-row/`; this pass reused existing local assets.
- Did not source every furniture price from live Turkish vendors; values are explicit estimates/ranges.
- Did not clean unrelated Pinegrow `_pgbackup/` churn or `pinegrow.json` state.

Verification:
- Connected to CDP at `100.115.42.17:9223` using WebSocket `suppress_origin`.
- Served `index-standalone-rebuilt.html` on port 8090 and verified desktop 1440x900 plus mobile 390x844.
- CDP confirmed first row has 28 images and 28 unique image sources.
- CDP confirmed row 2 includes `Deux achats laissent une marge` and `Le plan B reste louable`.
- CDP confirmed TL furniture content including `Canapé-lit compact`, `280k-360k TL`, and `35k TL`.
- CDP final check confirmed no `€` symbol in rendered main-document text.
- Saved screenshots at `/tmp/report-finish-desktop.png` and `/tmp/report-finish-mobile.png`.
- Ran JSON validation with `python3 -m json.tool` for updated manifests.

Next:
- If a more polished visual pass is needed, generate bespoke first-row images into `assets-rebuilt/first-row/` and swap them in with another CDP screenshot pass.
- Replace estimative furniture prices with sourced Turkish vendor links when exact procurement choices are available.

## 2026-06-02 - Project Progress Check

Done:
- Reviewed `CHANGELOG.md`, `ROADMAP.md`, `git status`, and current diffs to summarize project progress.
- Confirmed `index-standalone-rebuilt.html` is currently restored to full-preview media/iframe markup rather than Pinegrow edit-mode placeholders.
- Started a temporary static server on port 8090 and confirmed the active page returns HTTP 200.

Not done:
- Did not change active page content, layout, assets, or roadmap status.
- Could not complete deep CDP console/network/screenshot inspection because the reachable browser rejected WebSocket attachment due to Chrome remote-origin restrictions.

Verification:
- `git status --short --branch`
- `git diff --stat`
- `curl -I http://127.0.0.1:8090/index-standalone-rebuilt.html`
- CDP endpoint check: `100.115.42.17:9223` reachable; `100.68.242.20:9223` unavailable; `100.122.77.105:9223` timed out.

Next:
- Continue with first-row image asset generation/replacement, then CDP-verified screenshots once CDP WebSocket attachment is available.

## 2026-06-02 - Pinegrow Save-Preservation Fix

Done:
- Changed `tools/pinegrow_session.py` so Ctrl+C cleans Pinegrow edit-mode patches from the current saved HTML instead of copying the old session backup over it.
- Added reversible responsive-image backup helpers for future `srcset`, `sizes`, and eager-loading lightening.
- Wired cleanup into the full-preview path so preview HTML also restores Pinegrow-disabled scripts, media, and responsive image attributes in memory.

Not done:
- Did not delete the stale `backups/pinegrow-session/index-standalone-rebuilt.html.pinegrow-full.bak` file.
- Did not change the active page content.

Verification:
- Ran `python3 -m py_compile tools/pinegrow_session.py`.
- Started `python3 tools/pinegrow_session.py --file index-standalone-rebuilt.html --port 8090`, added a temporary marker to simulate a Pinegrow save, stopped with Ctrl+C, and confirmed the marker survived while edit-mode scaffolding was cleaned.
- Restored `index-standalone-rebuilt.html` after the test so the working tree only keeps the helper and changelog changes.

Next:
- Use the normal Pinegrow command without `--no-restore-on-exit`; saved edits should now survive stop because the stale backup is no longer copied over the page.

## 2026-06-02 - Pinegrow Backup Restore Diagnostic

Done:
- Inspected `tools/pinegrow_session.py` backup and restore logic.
- Confirmed the helper restores `index-standalone-rebuilt.html` from `backups/pinegrow-session/index-standalone-rebuilt.html.pinegrow-full.bak`.
- Ran `python3 tools/pinegrow_session.py --file index-standalone-rebuilt.html --port 8090` once and stopped it with Ctrl+C.
- Confirmed the stop path overwrote the active HTML with the existing backup, shrinking it from `462186` bytes to `405002` bytes.
- Restored `index-standalone-rebuilt.html` back to the pre-test git state.

Not done:
- Did not patch `tools/pinegrow_session.py`.
- Did not replace or delete the stale Pinegrow session backup.

Verification:
- Before test: `index-standalone-rebuilt.html` checksum was `335e7b9939be63871b0843f3393f34a4a3809d7a3a5147f5ac7945861a9faa29`.
- After session stop: active HTML matched the backup checksum `f99fb4816af3a386fe5f31e7555b00566e096ae9b73ce2b65604dd5d0fb63ed3`.
- After cleanup: active HTML returned to checksum `335e7b9939be63871b0843f3393f34a4a3809d7a3a5147f5ac7945861a9faa29`.

Next:
- Update the helper so session backups are refreshed per run or restore only the edit-mode transforms instead of blindly copying the first saved backup.

## 2026-06-01 - Pinegrow State Cleanup And Session Pointer

Done:
- Removed `pinegrow.json` from the project root.
- Removed `_pgbackup/` from the project root.
- Added `docs/codex-session-pointer.md` with the local Codex transcript path for future agents.
- Added the same transcript pointer to `AGENTS.md`.
- Added `/home/lofa/.codex/report-session-pointer.md` so agents can find the report transcript from the Codex directory.
- Confirmed the lingering `tools/pinegrow_session.py` process was already stopped before cleanup.

Not done:
- Did not modify the active Airbnb second-row content.

Verification:
- Confirmed no `pinegrow_session.py` process remains running.
- Confirmed `index-standalone-rebuilt.html` still contains the Airbnb second-row cards after the restore.

Next:
- Keep Pinegrow-generated local state out of the repo root to avoid confusing active source files.

## 2026-06-02 - Airbnb Revenue Benchmark Injection

Done:
- Removed the `PHOTO_TOUR_SCROLLABLE` modal parameter from the active Airbnb evidence links.
- Updated the second-row Airbnb comparable card with the CDP-verified stay total: `₺16,613 / 5 nights`.
- Updated the second-row revenue model card to show the projected four-cycle gross benchmark: `₺66,452` before fees, cleaning, vacancy, utilities, furnishing amortization, and management.
- Updated `docs/manifests/second-row-restructure-blueprint.json`, `docs/second-row-restructure-plan.md`, and `ROADMAP.md` to match the verified benchmark.

Not done:
- Did not add additional Airbnb comparable listings yet.
- Did not revise the later furnishing/cost row.

Verification:
- Confirmed by static search that active Airbnb links no longer include `PHOTO_TOUR_SCROLLABLE`.
- Verified through CDP on `100.122.77.105:9223` against `http://100.74.113.44:8090/index-standalone-rebuilt.html` that row 2 renders the updated Airbnb and revenue cards.
- Saved a CDP screenshot at `/tmp/report-airbnb-revenue-card-current.png`.

Next:
- Add more Airbnb comparables when the user provides links/screenshots, then rebalance the second row around revenue proof, acquisition proof, and furnishing cost.

## 2026-06-01 - Airbnb Evidence Row Experiment

Done:
- Reworked the first second-row group into three Airbnb/revenue cards followed by three Sahibinden proof cards.
- Added extracted Airbnb listing images under `assets-rebuilt/evidence/`.
- Added an Airbnb-themed card linking to the provided Airbnb URL in a new tab.
- Added a local popup iframe experiment that opens `Future-park.html`.
- Added a revenue-model card using the visible five-night test stay as the calculation frame.
- Updated the second-row plan and manifest to match the active experiment.

Not done:
- Did not invent a nightly or five-night Airbnb price. The saved local HTML and JS-free Airbnb response do not expose the final price.
- Did not commit or clean unrelated Pinegrow state files.

Verification:
- Parsed the active second row and confirmed the six-card order.
- Verified the extracted Airbnb images exist as WebP files.
- Confirmed the local modal markup and script are present in `index-standalone-rebuilt.html`.

Next:
- Use a live browser/CDP session to confirm the popup iframe behavior and responsive card crop.
- Extract the real Airbnb price from a browser session if the Airbnb page exposes it after JS/session load.

## 2026-06-01 - Second-Row Restructure Blueprint

Done:
- Audited the active `.design-container._2` second row and confirmed the current first group is six Sahibinden-first evidence cards.
- Created `docs/second-row-restructure-plan.md` with the intended narrative order: revenue reality, monthly floor, acquisition supply, captured detail, capital reserve, final product thesis.
- Created `docs/manifests/second-row-restructure-blueprint.json` with slot-by-slot copy, links, assets, readiness, and missing Airbnb comparable inputs.
- Marked the roadmap's second-row review task complete and left the active HTML rewrite pending.

Not done:
- Did not edit `index-standalone-rebuilt.html` because the Airbnb-style comparable links/screenshots are still missing.
- Did not change row images or links.

Verification:
- Parsed `.design-container._2` from `index-standalone-rebuilt.html`.
- Cross-checked report numbers against `docs/source/original-report.html`.
- Confirmed available second-row evidence assets under `assets-rebuilt/evidence/`.

Next:
- When Airbnb-style comparable links/screenshots arrive, add them to `assets-rebuilt/evidence/` and replace the second row one card at a time, with CDP verification.

## 2026-06-01 - First-Row Visual Prompt Pack

Done:
- Added `FIRST_ROW_VISUAL_PROMPTS.md` at the project root with generation prompts for all twelve first-row visuals.
- Added `docs/manifests/first-row-visual-replacement-plan.json` to map each slide to its current assets, target filename, priority, and expected fit.
- Added `assets-rebuilt/first-row/README.md` as the drop location for generated first-row visuals.
- Updated the roadmap with the completed prompt/manifest subtask.

Not done:
- Did not replace active HTML images yet.
- Did not generate or add final image files yet.

Verification:
- Cross-checked the prompt targets against the first-row image audit.
- Kept this pass documentation-only; no CDP screenshot required because rendered visuals were not changed.

Next:
- Add generated assets under `assets-rebuilt/first-row/`, then replace the weakest first-row placeholders in a controlled browser-verified pass.

## 2026-06-01 - First-Row Image Relevance Audit

Done:
- Audited the twelve first-row `Pourquoi Future Park ?` cards against their current French text.
- Documented the current repeated visual assets and which slides should keep, rework, or replace them.
- Added `docs/first-row-image-assessment.md` as the handoff document for image generation/replacement.
- Marked the first roadmap task complete.

Not done:
- Did not replace or generate any images in this pass.
- Did not edit `index-standalone-rebuilt.html`.

Verification:
- Parsed `.design-container._1` from `index-standalone-rebuilt.html` and confirmed it contains two `.slide-1-grid` groups with six cards each.
- Inspected representative current assets from `assets-rebuilt/`.

Next:
- Generate or source replacement images for the weak first-row matches, starting with slides 2, 5, 8, and 11.
- Verify replacements through CDP screenshots before committing visual changes.

## 2026-06-02 - Workspace Cleanup And First-Row Handoff

Done:
- Kept `index-standalone-rebuilt.html` as the active root page.
- Moved legacy exports to `docs/legacy/`.
- Moved manifests and blueprints to `docs/manifests/`.
- Moved HTML/Pinegrow backups to `backups/`.
- Removed the old `assets/` tree from the active workspace and kept `assets-rebuilt/`.
- Updated `tools/pinegrow_session.py` for granular Pinegrow toggles, always-hidden preloader, central backups, and default `0.0.0.0` serving.
- Documented the horizontal scroll structure, CDP workflow, and next roadmap.

Not done:
- Did not replace first-row images yet.
- Did not restructure the second row yet.
- Did not revise third-row furniture prices to Turkish lira yet.

Verification:
- `python3 -m py_compile tools/pinegrow_session.py`
- Pinegrow live-preview smoke test returned HTTP 200 for `index-standalone-rebuilt.html` on port 8096.
- Restored `index-standalone-rebuilt.html` back to full mode after the smoke test.
- Confirmed the root now contains the active page plus docs, tools, assets, and backups directories.

Next:
- Start with first-row image relevance against the injected French content.

## 2026-06-01 - Source Inputs And Local Auth

Done:
- Added the new project skill notes under `skills/`.
- Moved the standalone source report and `fp.jpg` into `docs/source/`.
- Archived new Pinegrow backup files under `backups/pinegrow/`.
- Removed generated local cache/cookie files from the working tree.
- Configured this local repo to use the `lotfinity` GitHub SSH key instead of the global `dewise080` key.

Not done:
- Did not inject new source-report content into the active presentation yet.
- Did not redesign rows or replace images in this pass.

Verification:
- Confirmed the active HTML is not left in Pinegrow edit mode.
- Confirmed `git ls-remote origin main` works locally with the repo-specific SSH key.

Next:
- Use `docs/source/original-report.html` as the source input when restructuring the second and third rows.
