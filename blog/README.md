# Blog authoring guide

This is the contract for anything published under `/blog/`. It is written for
the weekly review agent (see "The weekly agent" below), but it applies to
hand-written posts too.

Posts are plain static HTML, like the rest of this site. There is no build
step, no generator, and no front matter. Adding a post means writing three
things by hand: the post file, an entry in `blog/index.html`, and an item in
`blog/feed.xml`.

## Disclosure rules — read these first

Seven of the eight McMizzle repos are **private**. A post is public and
permanent. These rules are not negotiable, and a post that breaks one should
be thrown away rather than patched.

**Never publish, from any private repo:**

- Secrets or credentials of any kind, or anything shaped like one — API keys,
  tokens, stream keys, certificates, provisioning profiles, device IDs,
  account identifiers, endpoint URLs that embed a key. This has already been
  a real problem in these repos, not a hypothetical one.
- Verbatim source files, or long verbatim excerpts. Short illustrative
  snippets are fine, but write them for the post — reduced to the minimum
  that shows the idea, with project-specific names generalized.
- Anything about unreleased features, unannounced apps, or ship dates.
- Third-party API details obtained by reverse engineering where publishing
  them would breach that party's terms — describe the *method* and the
  general shape of the problem, not a working recipe against their service.
- Anyone else's personal data. Real names, emails, or team/player names that
  appear in test fixtures or logs, whether or not they belong to the user.

**Safe to publish:** the technique, the misleading symptom, the reasoning
that got from one to the other, the platform behavior that turned out to be
the real cause, and code you wrote fresh for the post to illustrate it.

When in doubt, leave it out and say so in the PR description. It is always
cheaper to ask than to un-publish.

## What earns a post

The bar is: **another engineer hits this problem, finds the post, and saves
an afternoon.** That is the only test that matters. It is not "what did I do
this week."

Good candidates look like:

- Undocumented or actively misleading platform behavior, where the symptom
  pointed somewhere other than the cause.
- A problem with no good existing write-up — search first; if the top results
  already answer it well, there is no traffic to win and no reader to help.
- Hardware, protocol, or third-party integration work where the spec was
  wrong, absent, or only available as a UI.
- A debugging story with a concrete, transferable takeaway.

Not worth a post: routine feature work, refactors, dependency bumps, anything
whose honest summary is "I did the normal thing and it worked," and anything
already covered well by first-party docs.

**"Nothing this week" is a correct and expected answer.** Filler posts cost
more credibility than they earn in traffic. Say what was reviewed and why
none of it cleared the bar.

## House style

- Write as Kevin, first person, past tense. Plain and direct.
- Lead with the symptom, not the architecture. The reader arrived from a
  search for their bug — the first paragraph should confirm they are in the
  right place.
- Be specific about versions, platforms, and hardware. "tvOS 18" is useful;
  "recent tvOS" is not.
- Include the wrong turns. The failed hypothesis is often the most useful
  part, because it is what the reader is currently believing.
- End with the transferable takeaway, not a summary.
- No filler openers ("In today's fast-paced world"), no invented metrics,
  no claims you cannot support from the actual work.
- 800–1500 words. Longer only if the material genuinely needs it.
- Never invent a detail to make the story flow. If the git history does not
  establish something, either leave it out or say it is uncertain.

## Adding a post — the three steps

### 1. The post file

`blog/<slug>/index.html`, where `<slug>` is short, hyphenated, and keyword
bearing (`tvos-top-shelf-image-cache`, not `a-frustrating-evening`).

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>POST TITLE — McMizzle</title>
<meta name="description" content="ONE SENTENCE, UNDER 160 CHARS, WRITTEN FOR SEARCH RESULTS.">
<link rel="canonical" href="https://mcmizzle.com/blog/SLUG/">
<link rel="alternate" type="application/rss+xml" title="McMizzle Blog" href="https://mcmizzle.com/blog/feed.xml">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#fdf6ec">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#201a13">
<meta property="og:type" content="article">
<meta property="og:url" content="https://mcmizzle.com/blog/SLUG/">
<meta property="og:title" content="POST TITLE — McMizzle">
<meta property="og:description" content="SAME SENTENCE AS THE DESCRIPTION ABOVE.">
<meta property="og:image" content="https://mcmizzle.com/assets/og-image.png">
<meta property="article:published_time" content="YYYY-MM-DD">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site-header"><a class="home-link" href="/">McMizzle</a></header>
<main>
<article class="post">
  <h1>POST TITLE</h1>
  <p class="post-meta">Kevin McMahon · MONTH D, YYYY</p>

  <p>Opening paragraph: the symptom, as the reader would have searched for it.</p>

  <h2>Section heading</h2>
  <p>Body copy.</p>

  <pre><code>// short, illustrative, written for the post
</code></pre>

  <h2>What I'd tell you to check first</h2>
  <p>The transferable takeaway.</p>
</article>
<nav class="post-nav"><a href="/blog/">← All posts</a></nav>
</main>
<footer>
  &copy; 2026 Kevin McMahon (McMizzle)
</footer>
</body>
</html>
```

Escape `<`, `>`, and `&` inside `<pre><code>` blocks as `&lt;`, `&gt;`, `&amp;`.
Swift generics and HTML tags in sample code will otherwise silently eat the
rest of the page.

### 2. The index entry

Add as the **first** `<li>` inside the `<ul class="post-list">` in
`blog/index.html`, immediately after the `<!-- POST LIST -->` comment. If the
"Nothing published yet" placeholder `<li>` is still there, delete it.

```html
    <li>
      <p class="post-meta">MONTH D, YYYY</p>
      <span class="post-title"><a href="/blog/SLUG/">POST TITLE</a></span>
      <p class="post-summary">One or two sentences. Can differ from the meta description.</p>
    </li>
```

### 3. The feed item

Add as the **first** `<item>` in `blog/feed.xml`, immediately after the
`<!-- ITEMS ... -->` comment.

```xml
    <item>
      <title>POST TITLE</title>
      <link>https://mcmizzle.com/blog/SLUG/</link>
      <guid isPermaLink="true">https://mcmizzle.com/blog/SLUG/</guid>
      <pubDate>Day, DD Mon YYYY 12:00:00 +0000</pubDate>
      <description>SAME SUMMARY AS THE INDEX ENTRY.</description>
    </item>
```

`pubDate` must be RFC-822 (`Fri, 07 Aug 2026 12:00:00 +0000`), not ISO-8601.
Feed readers drop items with an unparseable date without reporting an error.

## Before opening the PR

- [ ] Every disclosure rule above holds. Re-read the diff specifically
      looking for secrets, verbatim private source, and other people's names.
- [ ] All three files changed — post, index, feed.
- [ ] Slug, canonical URL, and `og:url` agree with the actual directory.
- [ ] The topic is not already covered by an existing post under `blog/`.
- [ ] Every technical claim traces to something real in the repo history.
      No invented versions, numbers, or error messages.
- [ ] Serve the site locally and load the post, the index, and the feed —
      `python3 -m http.server`, then `http://localhost:8000/blog/`. Opening
      the file over `file://` loads it unstyled (see the root README).

## The weekly agent

A scheduled cloud agent reviews all active repos weekly and either opens a
PR here or reports that nothing cleared the bar. It drafts; it does not
publish. Every post is merged by a human.

Its prompt points at this file, so **editing the rules above changes the
agent's behavior** — no need to touch the routine itself.
