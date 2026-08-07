# mcmizzle-site

The McMizzle marketing/support site — plain static HTML/CSS, no build step,
deployed via GitHub Pages straight from `main`. Warm cream/terracotta visual
identity (see `assets/style.css`), with light/dark variants throughout.

Built to unblock [AmbientCast#57](https://github.com/mcmizzle/AmbientCast/issues/57)
and [AmbientCast#59](https://github.com/mcmizzle/AmbientCast/issues/59): App
Store Connect needs real Support URL and Privacy Policy URL fields, and this
is where they live once the domain/hosting below are set up.

## Structure

- `index.html` — McMizzle landing page, lists all apps
- `blog/` — engineering write-ups. `blog/README.md` is the authoring
  contract: disclosure rules for the private repos, what earns a post, house
  style, and the exact three files every post has to touch (post, index,
  feed). Read it before adding a post by hand or changing what the weekly
  agent does — the agent's prompt points at that file rather than restating
  the rules, so editing it is how you steer the agent
- `privacy/` — one privacy policy shared across every McMizzle app (accurate
  as of writing: no analytics/tracking anywhere, nothing sent to any server
  McMizzle operates, since there isn't one)
- `support/` — support contact info, per app
- `ambientcast/` — AmbientCast's app page
- `calorieburndown/` — Calorie Burndown's app page
- `404.html` — branded 404, picked up automatically by GitHub Pages for any
  unmatched URL
- `robots.txt` — allows all crawlers; no sitemap, since the site is only a
  handful of pages
- `assets/style.css` — the one shared stylesheet for every page
- `assets/favicon.png`, `favicon-16.png`, `apple-touch-icon.png` — site
  favicon/home-screen icon, a cream "M" monogram on the terracotta accent
  color, generated with Pillow (see git history for the generation script)
- `assets/og-image.png` — 1200×630 Open Graph/Twitter card preview image,
  same monogram, referenced by every real page's `og:image` meta tag

Every real page (not `404.html`) also carries `rel=canonical`,
`theme-color` (light/dark), and Open Graph/Twitter card meta tags.

Add a new folder per app as each one launches.

## Status (see AmbientCast#59)

Live as of August 2026: `mcmizzle.com` purchased on Porkbun, DNS pointed at
GitHub Pages (A/AAAA records + `www` CNAME, verified across all 4
authoritative nameservers), HTTPS cert authorized, `CNAME` file in this repo
set to `mcmizzle.com`. `support@mcmizzle.com` forwards to Kevin's inbox via
Porkbun email forwarding. AmbientCast's `docs/APP_STORE_LISTING.md` points
at the real `mcmizzle.com/support/` / `mcmizzle.com/privacy/` URLs.

Both AmbientCast and Calorie Burndown were submitted to Apple App Review on
2026-08-02; the homepage no longer shows a "Coming soon" badge for Calorie
Burndown, and it has its own `calorieburndown/` page mirroring
`ambientcast/`'s.

`mcmizzle.net` is also purchased, set up as a redirect to `.com` via
Porkbun's URL forwarding (not hosted separately here).

## Local preview

No build step, but **serve the directory over HTTP rather than opening
`index.html` directly as a `file://` URL** — every page links
`/assets/style.css` with a root-relative path, which only resolves under
`file://` if `/assets/style.css` happens to exist at your filesystem root.
Opening the file directly loads the page with no styling at all and no
console error explaining why. Serve it with anything static instead, e.g.
`python3 -m http.server`, then open `http://localhost:8000/`. This only
affects local preview — GitHub Pages serves everything from the domain
root, so the same paths resolve correctly once deployed.
