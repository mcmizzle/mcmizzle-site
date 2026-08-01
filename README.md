# mcmizzle-site

The McMizzle marketing/support site — plain static HTML/CSS, no build step,
deployed via GitHub Pages straight from `main`.

Built to unblock [AmbientCast#57](https://github.com/mcmizzle/AmbientCast/issues/57)
and [AmbientCast#59](https://github.com/mcmizzle/AmbientCast/issues/59): App
Store Connect needs real Support URL and Privacy Policy URL fields, and this
is where they live once the domain/hosting below are set up.

## Structure

- `index.html` — McMizzle landing page, lists all apps
- `privacy/` — one privacy policy shared across every McMizzle app (accurate
  as of writing: no analytics/tracking anywhere, nothing sent to any server
  McMizzle operates, since there isn't one)
- `support/` — support contact info, per app
- `ambientcast/` — AmbientCast's app page

Add a new folder per app (e.g. `calorieburndown/`) as each one launches.

## Status (see AmbientCast#59)

Live as of August 2026: `mcmizzle.com` purchased on Porkbun, DNS pointed at
GitHub Pages (A/AAAA records + `www` CNAME, verified across all 4
authoritative nameservers), HTTPS cert authorized, `CNAME` file in this repo
set to `mcmizzle.com`. `support@mcmizzle.com` forwards to Kevin's inbox via
Porkbun email forwarding. AmbientCast's `docs/APP_STORE_LISTING.md` points
at the real `mcmizzle.com/support/` / `mcmizzle.com/privacy/` URLs.

`mcmizzle.net` is also purchased, set up as a redirect to `.com` via
Porkbun's URL forwarding (not hosted separately here).

## Local preview

No build step — just open `index.html` in a browser, or serve the directory
with anything static (e.g. `python3 -m http.server`).
