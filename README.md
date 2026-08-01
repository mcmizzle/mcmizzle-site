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

## What's still needed before this is live (see AmbientCast#59)

- [ ] Buy `mcmizzle.com`
- [ ] Point its DNS at GitHub Pages (an `A`/`ALIAS` record for the apex
      domain to GitHub Pages' IPs, or a `CNAME` record if using `www`) —
      see [GitHub's custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
      when ready. **Then** add a `CNAME` file back to this repo's root
      containing just `mcmizzle.com` (deliberately left out for now — with
      no domain yet, a `CNAME` file makes GitHub Pages redirect the default
      `mcmizzle.github.io/mcmizzle-site/` preview URL to a domain that
      doesn't resolve, breaking the only way to preview this before the
      domain exists).
- [ ] Set up `support@mcmizzle.com` (currently a placeholder on the support
      page)
- [ ] Once live, update AmbientCast's `docs/APP_STORE_LISTING.md` Support/
      Privacy URLs from the interim GitHub placeholders to
      `https://mcmizzle.com/ambientcast/` / `https://mcmizzle.com/privacy/`

## Local preview

No build step — just open `index.html` in a browser, or serve the directory
with anything static (e.g. `python3 -m http.server`).
