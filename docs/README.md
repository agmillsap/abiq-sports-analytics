# Abigail Millsap · Interactive Product Portfolio

This `docs/` folder contains a public product-management portfolio that can be hosted on GitHub Pages without Streamlit or a Python server.

## What is included
- **Field Sales Portfolio Optimization:** interactive illustrative business demo and case study.
- **Market Opportunity Navigator:** interactive illustrative business demo and case study.
- **ABIQ Sports Decision Intelligence:** browser-based, static HTML/CSS/JavaScript version of the public ABIQ Showcase, including a frozen NFL forecast board, verified historical model-performance presentation, and an interactive **SEC / Big Ten CFB Survivor** scenario engine.

The original user-supplied portfolio HTML is preserved as 14 binary chunks under `parts/`. `index.html` reconstructs it in the browser and replaces the old Streamlit link with the local `./abiq/` destination. Clicking the ABIQ card opens a full-screen, responsive portfolio overlay (or visitors can choose to open the standalone ABIQ page). The other two interactive enterprise demonstrations remain unchanged.

The ABIQ copy is served from `abiq/index.html`, `abiq/app.css`, and `abiq/app.js`. It is derived from the **public sanitized ABIQ Showcase** in this repository, not the private production ABIQ system. The NFL Week 1 sample and model-performance evidence are frozen; CFB fixtures and example probabilities are synthetic. It neither displays live odds nor makes live betting recommendations. Public brand image files are referenced from this repository's raw GitHub URLs, while team logos may be requested from ESPN's public CDN.

## Publish with GitHub Pages

In the GitHub repository, open **Settings → Pages**:
1. Source: **Deploy from a branch**.
2. Branch: `main`; folder: `/docs`.
3. Save and follow the URL GitHub displays after successful deployment.

The usual project-site URL for the current repository name is `https://agmillsap.github.io/abiq-sports-analytics/`, and the standalone static ABIQ showcase is under `/abiq/` on that site. These URLs are expected until GitHub Pages deployment is confirmed. This tool connection cannot change GitHub's repository name or Pages settings. A future dedicated `abigail-millsap-product-portfolio` repository can provide a more professional URL without renaming the ABIQ application's existing repository.

## Public/private boundary

Business dashboards use sample data. The static ABIQ replica contains no authentication, private production data, paid provider tokens, API secrets, or user pick storage. The scenario engine runs inside the visitor's browser and does not persist choices across sessions. Review any employer trademarks and brand materials before sharing externally.
