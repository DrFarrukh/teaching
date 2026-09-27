# Lecture 1 Reveal.js deck

This directory presents the sibling `../slides.md` as a Reveal.js deck. Edit `../slides.md`; the sync script removes its Marp front matter and copies the generated figures.

Reveal.js and MathJax browser assets are stored in `vendor/`, so the deck runs without an npm install or internet connection.

## Present locally

From this directory, run `npm run dev` and open <http://127.0.0.1:8000>. Press `F` for fullscreen, `S` for speaker view, `O` or `Esc` for the slide overview, and `B` to blank the screen.

## Build static files

Run `npm run build`. The deployable site is written to `dist/` and contains the slides, figures, Reveal.js code, and local math assets.
