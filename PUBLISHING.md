# Publish the course site

After the `main` branch is pushed to GitHub, enable GitHub Pages:

1. Open the repository's **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch `main` and folder `/docs`, then save.
4. GitHub will publish the site at `https://drfarrukh.github.io/teaching/`.

The Reveal.js pages in `docs/` load the Markdown slide decks and figure assets from their adjacent `public/` folders. They reuse the local Reveal.js and MathJax files already included with the Data Analysis and Visualization lecture.
