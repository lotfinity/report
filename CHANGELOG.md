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
