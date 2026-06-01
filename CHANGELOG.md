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
