# Roadmap

## Current Priority

- [x] Assess whether the current first-row images match the new French text content.
- [ ] Generate or source new first-row images where the current visuals do not support the message.
  - [x] Create first-row image generation prompts and target-file manifest.
  - [ ] Add generated first-row assets under `assets-rebuilt/first-row/`.
- [ ] Verify the first-row image replacements through CDP screenshots at desktop and mobile widths.

## Second Row Restructure

- [x] Revisit the second row instead of leaving the Sahibinden items one after another.
  - [x] Create the second-row target story and replacement blueprint.
  - [x] Apply the first active HTML rewrite for the Airbnb/Sahibinden evidence order.
- [x] Introduce Airbnb-style comparable apartment examples after links are provided.
- [ ] Use those Airbnb examples to show that the revenue model is real and currently market-supported.
  - [ ] Extract the real Airbnb stay price; current page exposes the stay dates but not the final price without JS/session state.
- [x] Then present Sahibinden listings as purchasable supply, with links opening in a new tab.
- [ ] Keep the final narrative flow clear: revenue evidence first, acquisition listings second.

## Furnishing And Cost Flow

- [ ] Shift the later second-row content toward furnishing scope and costs.
- [ ] Rework the third row as the interactive furniture selector and cost explainer.
- [ ] Replace current euro pricing with real Turkish lira pricing.
- [ ] Check that each furniture/cost element has a believable source or clear assumption.

## Agent Process

- [ ] Every agent appends a dated entry to `CHANGELOG.md`.
- [ ] Every visual/layout change is checked in a CDP browser before commit.
- [ ] Every first-row text/content change updates `docs/manifests/future-park-slide-1-grid-blueprint.json`.
- [ ] Keep root clean: active page, docs, tools, assets, manifests, and backups only.

## Later Discussion

- [ ] Review the complete story once first-row images, second-row revenue/listings, and third-row furnishing costs are coherent.
- [ ] Decide whether additional sections are needed or whether the current three-row structure is enough.
