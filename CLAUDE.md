# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static landing page for Sociail Assistant, an AI hardware companion device. A lightweight Node server is included for email capture via Resend.

## Development Commands

```bash
# Open directly (macOS)
open index.html

# Serve locally (recommended for testing navigation and asset paths)
python3 -m http.server 8000
# Then visit http://localhost:8000

# Serve locally with backend (email capture)
npm install
npm start
# Then visit http://localhost:3000
```

## Architecture

**Entry point:** `index.html` - single-page landing with sections for hero, features, spaces, and CTA

**Backend:** `server.js` handles `/api/subscribe` and sends emails via Resend.

**CSS modules** (`styles/`):
- `variables.css` - design tokens (colors, theming via CSS custom properties)
- `base.css` - foundation styles
- `navigation.css` - nav bar
- `hero.css` - hero section and ticker animations
- `device.css` - 3D device preview with tooltips and ecosystem silhouettes
- `sections.css` - features, spaces, CTA sections
- `responsive.css` - breakpoints

**JavaScript:** `scripts/main.js` handles smooth scrolling, theme toggle (persisted to localStorage), and form submission

**Theming:** Uses `data-theme` attribute on `<html>` with CSS custom properties. Respects `prefers-color-scheme` by default, with manual override via theme toggle button.

**Environment:** set `RESEND_API_KEY` and optionally `RESEND_FROM`/`RESEND_NOTIFY_TO` (see `.env.example`).

## Code Style

- 4-space indentation in HTML, CSS, and JS
- Semicolons in JS
- kebab-case for CSS classes (e.g., `device-hotspot`)
- camelCase for JS functions (e.g., `toggleTheme`)
- Add new design tokens to `styles/variables.css` rather than hardcoding colors
- Keep section styles in their existing CSS module files

## Manual Testing Checklist

- Navigation anchors scroll smoothly to `#features`, `#spaces`, `#notify`
- Theme toggle updates icon and persists across page reloads
- Tooltips appear on hover for device ecosystem elements in hero
- Email form posts to `/api/subscribe`, shows a status message, and resets on success

## Commit Style

Use Conventional Commits: `feat:`, `fix:`, etc. For UI changes, include before/after screenshots in PRs.
