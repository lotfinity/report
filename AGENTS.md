# Agent Handoff Notes

This workspace is a Pinegrow/Webflow static report rebuild. Treat `index-standalone-rebuilt.html` as the single active page and `assets-rebuilt/` as the single active asset directory.

## Non-Negotiable Workflow

Connect to a CDP browser before changing visual layout, responsive behavior, animations, images, or asset paths. Available CDP endpoints:

- `100.68.242.20:9223`
- `100.122.77.105:9223`
- `100.115.42.17:9223`

Use CDP to inspect the relevant DOM, console/network failures, and screenshots. Do not rely on static HTML diffs alone for layout work.

Every agent must update `CHANGELOG.md` before finishing. Include Done, Not done, Verification, and Next.

## Session Transcript

Important historical context for this project is available in the local Codex transcript:

`/home/lofa/.codex/sessions/2026/06/01/rollout-2026-06-01T11-38-21-019e8255-7d3d-71e3-a02d-657527c8a67b.jsonl`

Search it with `rg` only when the committed docs do not answer a question. The committed source of truth remains this repo.

## Active Files

- Page: `index-standalone-rebuilt.html`
- Assets: `assets-rebuilt/`
- Pinegrow helper: `tools/pinegrow_session.py`
- First-row blueprint: `docs/manifests/future-park-slide-1-grid-blueprint.json`
- Source report inputs: `docs/source/original-report.html` and `docs/source/fp.jpg`
- Project-provided skills: `skills/`
- Legacy exports: `docs/legacy/`
- Backups: `backups/`

The old `assets/` directory was removed intentionally. Do not reintroduce it unless the active HTML is explicitly being migrated again.

The `skills/` directory was added intentionally as agent-facing project guidance. Read relevant skill notes before major visual, copywriting, animation, color, or data-report work.

## Pinegrow Edit Mode

Use:

```bash
python3 tools/pinegrow_session.py --file index-standalone-rebuilt.html --port 8090
```

Defaults:

- Host: `0.0.0.0`
- Scripts disabled in Pinegrow edit mode.
- Video/iframe media disabled in Pinegrow edit mode.
- Responsive image `srcset`/`sizes` lightened in Pinegrow edit mode.
- Preloader always hidden, even when other features are enabled.
- Full preview re-enables disabled scripts/media in memory.
- Backups go to `backups/pinegrow-session/`.

Granular flags:

- `--enable-scripts`
- `--enable-media`
- `--enable-responsive-images`
- `--no-edit-css`
- `--no-runtime-guard`

## Horizontal Scroll Sections

The report uses Webflow IX/GSAP-style horizontal scroll sections. The two main rows are not plain CSS overflow rows; scroll distance is controlled by both container height and Webflow interaction transforms.

First row:

- Section meaning: `Pourquoi Future Park ?`
- Container: `.design-container._1`
- Wrapper: `.design-wrap._1`
- Structure: two `.slide-content` groups, each containing one `.slide-1-grid`.
- Current content: 12 cards total, 6 cards in each group.
- Desktop height tuning lives in the inline style block `#extra-grid-scroll-tuning` inside `index-standalone-rebuilt.html`.
- Current desktop height: `.design-container._1 { height: 760vh; }`
- Desktop Webflow action: `a-26` in `assets-rebuilt/beeaf25ddb_webflow.schunk.452e1cd124749014.js`.
- Current desktop transform distance: `xValue: -282`.

Second row:

- Container: `.design-container._2`
- Wrapper: `.design-wrap._2`
- Current purpose: evidence/listings/furnishing bridge. This needs restructuring.
- Current desktop height: `.design-container._2 { height: 900vh; }`
- Desktop Webflow action: `a-27` in `assets-rebuilt/beeaf25ddb_webflow.schunk.452e1cd124749014.js`.
- Current desktop transform distance: `xValue: -342`.

Mobile/tablet action IDs also exist in the Webflow chunk. Do not change only desktop and assume responsive behavior survived; verify through CDP.

## Text Injection Rules

For first-row text edits, use `docs/manifests/future-park-slide-1-grid-blueprint.json` as the safe conceptual map. After changing first-row content, update that blueprint so future agents can inject text without guessing.

Keep the row structure stable unless the task explicitly requires changing card count:

- Group 1: `group_1_slide_1` through `group_1_slide_6`.
- Group 2: `group_2_slide_1` through `group_2_slide_6`.

Text edits should preserve the existing class structure. Avoid bulk rewrites of the section unless CDP verification shows the resulting scroll behavior is correct.

## Asset Rules

New images should go in `assets-rebuilt/`. The current first row still needs an image-content relevance pass. Video placeholders currently link to local video wrapper pages in `assets-rebuilt/`.

Responsive images are a known source of broken visual matches. When replacing an image, check `src`, `srcset`, `sizes`, and the actual file dimensions served at the tested viewport.

## Git Auth

This local checkout should use the repo-specific SSH key `~/.ssh/github_lotfinity_report_ed25519` through `core.sshCommand`, so pushes authenticate as `lotfinity` instead of the global `dewise080` key. If GitHub auth starts reporting `dewise080`, restore the repo-local config:

```bash
git config core.sshCommand "ssh -i ~/.ssh/github_lotfinity_report_ed25519 -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
```
