# Repository Guidelines

## Project Structure & Module Organization
This is a static landing page with a lightweight Node backend for email capture. The entry point is `index.html`, and the backend lives in `server.js`. Styling is split into modular CSS files in `styles/` (tokens in `styles/variables.css`, layout and section styles in `styles/base.css`, `styles/navigation.css`, `styles/hero.css`, `styles/device.css`, `styles/sections.css`, and `styles/responsive.css`). Interactivity lives in `scripts/main.js`. Static assets live in `images/`. Product docs and prototype assets live in `docs/`, including `docs/7-Sociail-Assistant/` and `docs/prototype/` ZIPs.

## Build, Test, and Development Commands
There is no build step. Use one of the following:
```
# Open directly (macOS)
open index.html

# Serve locally for consistent asset loading
python3 -m http.server 8000

# Serve locally with backend (email capture)
npm install
npm start

# Run tests (Node test runner)
npm test
```
The HTTP server lets you test hash navigation, theme toggling, and asset paths in a browser at `http://localhost:8000`. The Node server runs at `http://localhost:3000` and requires `RESEND_API_KEY` in `.env` (see `.env.example`).

## Coding Style & Naming Conventions
Use 4-space indentation in HTML, CSS, and JS, and keep semicolons in JS. Prefer kebab-case for CSS class names (for example, `device-hotspot`) and camelCase for JS functions (for example, `toggleTheme`). Add new design tokens to `styles/variables.css` rather than hard-coding colors. Keep section-level styles in their existing module file instead of creating new one-off files.

## Testing Guidelines
There are no automated tests. Perform a quick manual smoke check:
- Navigation anchors smoothly scroll to `#features`, `#spaces`, `#notify`.
- Theme toggle updates the icon and persists across reloads.
- Tooltips and hover interactions render correctly in the hero device section.
- The notify form submits to `/api/subscribe` and shows a success or error message.

## Commit & Pull Request Guidelines
Recent history uses Conventional Commit style prefixes like `feat:` and `fix:`. Keep messages short and scoped. For PRs, include a clear summary, note any manual testing performed, link related issues when applicable, and attach before/after screenshots for UI or layout changes.

## Documentation & Assets
Keep product and prototype docs in `docs/`. Large prototype ZIPs should not be unpacked into the repo. Update related HTML in `docs/7-Sociail-Assistant/` only when you are changing the corresponding static pages.
