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
