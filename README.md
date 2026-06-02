# Future Park Report Workspace

Active page: `index-standalone-rebuilt.html`

Active assets: `assets-rebuilt/`

This repo is now arranged so the root contains the active rebuilt report and project docs. Legacy exports, backups, and manifests are kept in subdirectories.

## Required Debug Workflow

Do not make layout, animation, or responsive asset changes without checking the page through a Chrome DevTools Protocol browser. Use one of these remote browsers:

- `100.68.242.20:9223`
- `100.122.77.105:9223`
- `100.115.42.17:9223`

Before committing visual work, verify the relevant section with the DOM, console/network status, and screenshots at desktop and mobile widths.

## Pinegrow

Run the lightweight Pinegrow session from the repo root:

```bash
python3 tools/pinegrow_session.py --file index-standalone-rebuilt.html --port 8090
```

The server binds to `0.0.0.0` by default, so it can be reached from Tailscale/CDP browsers. The live preview restores disabled scripts and media in memory while Pinegrow edits a lighter HTML file.

Useful flags:

- `--enable-scripts`
- `--enable-media`
- `--enable-responsive-images`
- `--no-edit-css`
- `--no-runtime-guard`

The preloader is always hidden in Pinegrow edit mode, regardless of these flags.

## Project Structure

- `index-standalone-rebuilt.html`: only active page.
- `assets-rebuilt/`: only active asset directory.
- `tools/pinegrow_session.py`: Pinegrow edit/preview helper.
- `docs/manifests/`: blueprints, manifests, and rebuild notes.
- `docs/legacy/`: archived source exports.
- `backups/`: historical HTML and Pinegrow backups.
- `AGENTS.md`: detailed implementation notes for future agents.
- `ROADMAP.md`: next planned content/design tasks.
- `CHANGELOG.md`: every agent must append what changed, what did not, and how it was verified.
