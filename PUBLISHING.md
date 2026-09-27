# Publish the course site

After pushing the `main` branch to GitHub, enable GitHub Pages once:

1. Open the repository's **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select branch `main` and folder `/docs`, then save.
4. GitHub will publish the course site at `https://drfarrukh.github.io/teaching/`.

The Reveal.js slide deck is already built into `docs/`. When its source slides or local images change, rebuild it from the lecture's `revealjs/` folder with `npm run build`, then copy the contents of `dist/` into the matching `docs/.../slides/` folder before committing.
