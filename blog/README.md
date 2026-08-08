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

**Never assume a repo is public. Check.** `gh repo view <repo> --json
visibility`. At the time of writing, `mcmizzle-site` is the only public one
and every app repo is private — including the ones with live product pages
on this site, which is exactly what makes them feel public when they aren't.
A draft has already argued "this repo is public, so naming it carries less
risk" about a private repo. It generalized anyway and nothing leaked, but it
reached a safe answer from a false premise, and the same premise points the
other way just as easily. One command settles it; reasoning about it does not.

Note also that repo visibility is not the whole test. A repo being public
would not make its secrets, its users' data, or its unreleased work
publishable — those rules hold regardless.

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

### The dry bit

Kevin's writing has a wry, understated register, and posts should carry it.
It is not a joke layer applied on top of technical prose — it is *how the
technical thing gets described*. Read a page of his commit messages before
writing; that is the voice, and it is the best available sample of it.

The three moves that actually appear:

**The machine as an unreliable actor.** Systems do things *to* you, with
apparent intent, and stating that plainly is the joke.

> a dropped third strike could invent an out
> a finished game was blindfolding the poll
> the games and board sections were wired to nothing
> Stop the demo printer's detail screen offering settings that break it

**Exasperation carried by a single word.** *actually*, *at all*, *again*,
*a person*. Never a whole sentence of complaint — one word, then move on.

> Left-align Close so it can actually be focused
> Make cameras reachable at all
> Log the Top Shelf extension somewhere a person can actually read
> Put "Refresh from Cloud" next to the thing it refreshes

**Cost stated flatly, without self-pity.** The understatement is the point.

> Record the Top Shelf cache lesson that cost an evening
> Correct two CLAUDE.md claims that cost most of a verification session

Both published posts already do this in places — *"and then you're debugging
your own debugging,"* *"it kept faithfully drawing a tile from builds ago,"*
*"in the confident green of a goal you've already met."* More of that. It is
the register, not a departure from it.

**What this is not, and this matters more than the above.** This instruction
is the easiest one here to overshoot, and an overshot version is much worse
than a flat post. So:

- **No jokes, no puns, no wordplay.** The humor is structural — it lives in
  how a fact is framed. Nothing is ever *added* to be funny.
- **No punchlines and no signposting.** No "spoiler alert," no "plot twist,"
  no "narrator: it was not," no "(yes, really)," no rhetorical "guess what
  happened next."
- **No exclamation marks. No emoji. No parenthetical winking.**
- **No performed self-deprecation.** "I'm an idiot," "in my infinite wisdom,"
  "past me was a fool." Kevin states what a mistake cost and moves on; he
  does not perform embarrassment about it.
- **Never at the reader's expense.** The reader is stuck on this exact bug
  right now. The wryness is aimed at the platform, the machine, and Kevin's
  own wrong turns — never at someone who doesn't already know the answer.
- **Never at accuracy's expense.** If a funnier phrasing is less precise, the
  precise one wins, every time.

A good test: could this sentence appear in one of his commit messages? If it
reads like a tech-blog quip, it fails. If it reads like someone describing
what happened, slightly tired, entirely accurate, it passes.

Frequency: a handful across a post. It should feel like the writer's natural
register, not like a comedian doing tech support. **When in doubt, be flat.**
The reader came for the answer.

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

  <details class="eli5">
    <summary>ELI5: the jargon term</summary>
    <p>Two or three plain sentences. See "ELI5 asides" below.</p>
  </details>

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

#### ELI5 asides

A post's primary reader is an engineer who searched for their exact bug and
needs no hand-holding. But posts also reach people arriving from a link
rather than a search, and platform-specific jargon locks them out of a story
they'd otherwise follow.

So: `<details class="eli5">`, collapsed by default. The expert reader sees a
one-line summary and skims past it. Everyone else gets a way in. No
JavaScript is involved — collapsing is the element's own behavior, which is
also why it is keyboard operable and screen-reader friendly for free.

```html
  <details class="eli5">
    <summary>ELI5: what's an app extension?</summary>
    <p>
      A small separate program that ships inside your app and runs on the
      system's schedule rather than yours. It gets its own sandbox and can't
      simply reach into the app's files.
    </p>
  </details>
```

**Use one when** a term is load-bearing for the story and specific to a
platform, framework, or domain the general reader has no reason to know:
`.appex`, App Group, Top Shelf, background delivery, sandbox, complication.

**Don't use one for** general programming vocabulary (cache, nil, closure,
race), for anything the surrounding prose already explains, or to restate the
argument. An ELI5 supplies *background*, never the point of the post. If a
reader could skip every aside and still follow the piece, they're doing their
job.

Rules of thumb:

- **Two to four per post.** One suggests the jargon wasn't really a barrier;
  more than four means the post is written at the wrong level and should be
  edited instead.
- **Place it immediately after the paragraph that first uses the term**, not
  in a glossary at the end. It answers a question the reader just formed.
- **Two to four sentences.** If it needs more, it's a post of its own.
- **Summary line names the term**, so a skimmer can tell what's inside
  without opening it: "ELI5: what's an app extension?" not "ELI5: some
  background."
- **Plain language, no new jargon.** An explanation that needs its own
  explanation has failed. Analogies are fine; cuteness is not.
- **Same voice as the post.** These are Kevin explaining something simply,
  not a textbook footnote.

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

### 4. The Open Graph card

Each post gets its own preview image. A link shared to LinkedIn or Slack is
mostly its preview image, and every post pointing at the same monogram makes
two different posts look like the same post.

```
python3 -m venv .venv && .venv/bin/pip install Pillow    # once
.venv/bin/python tools/og-image.py <slug> "Post title"
```

That writes `assets/og-<slug>.png` at 1200×630. Point the post's `og:image`
at it instead of the shared `assets/og-image.png`:

```html
<meta property="og:image" content="https://mcmizzle.com/assets/og-SLUG.png">
```

`twitter:image` isn't needed — Twitter/X and LinkedIn both fall back to
`og:image`.

**If Pillow isn't available in your environment, skip this step** and leave
the shared `og-image.png` in place. The result is a worse preview, not a
broken page. Say so in the PR so it can be generated at review time. Do not
invent an `og:image` URL for a file you didn't create — a card that 404s is
worse than a generic one, because most social clients cache the failure.

### 5. The social copy

Add a section to `blog/SOCIAL.md`, newest first. See "Social copy" below.

### 6. The sitemap

```
python3 tools/sitemap.py
```

Standard library only — this one runs anywhere, including the agents'
sandbox. It rebuilds `sitemap.xml` from whatever directories actually contain
an `index.html`, so it can't drift out of sync with the posts. Commit the
result.

### Link the app the post came from

If the post grew out of work on one of the apps, name that app and link its
page (`/ambientcast/`, `/calorieburndown/`) the first time it comes up. App
discovery is one of the reasons the blog exists.

Name it plainly and move on — one link in the prose, not a pitch. The opening
paragraph's job is to confirm a searcher is in the right place, and it stops
doing that job if it turns into an advertisement. If the post isn't about an
app, skip this.

## Before opening the PR

- [ ] Every disclosure rule above holds. Re-read the diff specifically
      looking for secrets, verbatim private source, and other people's names.
- [ ] All five touched — post, `blog/index.html`, `blog/feed.xml`, the OG card
      (or an explicit note saying why not), and `blog/SOCIAL.md`. Plus
      `blog/CONSIDERED.md`.
- [ ] The `og:image` URL names a file that actually exists in `assets/`.
- [ ] Slug, canonical URL, and `og:url` agree with the actual directory.
- [ ] The topic is not already covered by an existing post under `blog/`.
- [ ] Every technical claim traces to something real in the repo history.
      No invented versions, numbers, or error messages.
- [ ] **The post agrees with itself.** Every count, figure, and quantity is
      consistent with every other mention of it across the post. Tracing each
      claim to the source separately is not enough to catch this: the first
      published draft said a failure path "coerced all four values to zero"
      two paragraphs after correctly arguing that only three could have been
      zero, and *both* halves were individually true of the real code. Read
      the numbers as a set, not one at a time.
- [ ] **Every external link actually resolves.** Fetch each one and confirm
      it returns 200 — do not reason about whether a documentation URL looks
      right. Plausible-but-wrong doc URLs are a specific failure mode here.
- [ ] **Every quotation is verbatim.** If the post block-quotes a spec or a
      doc page, fetch the source and compare word for word. Do not reproduce
      a quote from memory, and do not silently tidy up its wording.
- [ ] **Sample code is correct, not merely copied.** Reproducing what the
      repo does is necessary but not sufficient — the repo can be wrong, and
      a post turns its code into advice that strangers will follow. Check the
      snippet on its own merits. The tvOS post shipped `hashValue` as a
      content-derived identifier because the app does; Swift seeds `Hashable`
      randomly per process, so it was never stable, and the surrounding
      paragraph explaining *why* it worked was wrong. If you find a defect
      like this, fix the post **and** file it against the app repo.
- [ ] Serve the site locally and load the post, the index, and the feed —
      `python3 -m http.server`, then `http://localhost:8000/blog/`. Opening
      the file over `file://` loads it unstyled (see the root README).

## Answering forum threads

The highest-value thing this blog does. Every post should ship with a draft
reply to a real thread where somebody is stuck on the same problem, added to
`blog/SOCIAL.md` alongside the social copy.

It works because it is the only tactic that pays off on every goal at once
(see `AUTOMATION.md`): it helps a person who is stuck right now, it earns a
link from a high-authority domain, it reaches engineers who have the problem
rather than a general audience, and it is the opposite of self-promotion
while still being self-promotion. A reply on `developer.apple.com` is worth
more to a young domain than anything else available.

**Where to look.** Apple Developer Forums first for anything Apple-platform.
Also worth checking: GitHub issues on a relevant project, and subreddits like
r/iOSProgramming — but read the self-promotion rules first, several require a
participation ratio. Search the way an engineer with the bug would, not the
way someone promoting a post would.

### Picking a thread

The search that finds the post's competition also finds its threads. Judge
each candidate on:

- **Is it actually unanswered, or answered badly?** An unanswered thread with
  other people saying "I have this too" is the best possible target. A thread
  whose accepted answer diagnoses something else is nearly as good — that
  reader is being actively misled.
- **Does the behavior still exist?** If the post reproduces it on a current
  OS, say so with the version. That is often the exact thing readers of an old
  thread want to know.
- **Is it resolved with an accepted answer?** Then leave it alone. Replying to
  a settled thread is necroposting and reads as link-dropping. A first pass at
  this picked a decade-old thread with an accepted Apple staff answer; the
  right move was to discard it and search again for live ones.

Age alone doesn't disqualify a thread. One target used here had been open
since 2019 with three developers confirming through 2021 — old, but never
answered, and still reproducing.

### Writing the reply

**Answer the question. The link is evidence, not the point.** The test: delete
the link — does the reply still help? If not, it's an advertisement and it
will read as one.

- **Lead with the substance**, and put the link in the last line.
- **Concede what you can't solve, up front.** One reply here opens by
  admitting it has no way around the restriction the poster is asking about.
  That is what earns the rest of it.
- **Don't claim their bug is your bug.** If the symptoms differ, say so
  explicitly. Overclaiming a fix wastes the time of someone already stuck.
- **Include the searchable strings** — log lines, error codes, API names.
  Future searchers land on the thread, not the post, and those strings are
  how they find it.
- Same house style as a post, and the same disclosure rules: a forum reply is
  as public and permanent as anything under `/blog/`.

### After posting

Mark the block **Posted YYYY-MM-DD** in `SOCIAL.md`. Never post the same
reply twice — in a venue built on reputation, that reads as spam.

## Social copy

Every post gets a LinkedIn draft in `blog/SOCIAL.md`, written in the same PR
and posted by hand. Nothing auto-publishes to Kevin's professional network.

**Write it as a post, not a promotion.** The single most common failure is
copy that announces a blog post instead of telling the story. Nobody follows
a link to find out what the link is about. Give away the finding — the reader
who wants the detail will click, and the reader who doesn't still got
something from you.

- **The first two lines are everything.** LinkedIn cuts to "see more" there.
  Lead with the symptom or the surprise, never with "I wrote a new post about…"
- **Plain language.** This audience is much broader than the post's. Someone
  who has never written Swift should follow the shape of the problem. This is
  the same reason posts carry ELI5 asides.
- **Give the takeaway away, in full.** The generalizable lesson belongs in the
  social copy, not held back as bait.
- **No hype, no emoji ladders, no hashtag piles.** At most a couple of genuinely
  relevant tags, and only if they're real terms of art.
- **Never claim more than the post does.** If the post says something is
  unverified, the social copy does not quietly upgrade it to fact. Copy is
  where overstatement is most tempting and least visible.
- **Don't put the link in the body.** The feed demotes posts with external
  links. Post the text, then add the link as the first comment, and end the
  body pointing at it ("write-up below").

Length: 120–250 words. Long enough to carry the story, short enough to read
standing up.

**Never hard-wrap text inside the fenced blocks in `SOCIAL.md`.** Everywhere
this copy is going — LinkedIn's composer, the Apple Developer Forums editor —
preserves the line breaks you paste and does its own wrapping. Prose wrapped
at 76 characters arrives with a break every 76 characters and looks broken.
One paragraph per line, blank lines between paragraphs, lines as long as they
need to be. This is the one place in this repo where long lines are correct.

Code and log samples are the exception: keep their breaks and indentation,
because there the breaks carry meaning.

The same applies to any other paste-buffer added here later — forum replies,
Reddit comments, dev.to cross-posts.

## Record what you passed on

`blog/CONSIDERED.md` is the running record of topics that were weighed and
rejected, and why. Update it in the same PR as the post.

The point is that the reasoning survives. Deciding that a topic loses on the
search test, or that it needs heavy generalization before it could be
published safely, is real work — and if it only ever appears in one PR
description it gets buried, and the next run re-derives it from scratch and
may well reach a different answer.

**It is a record, not a queue.** Nothing in that file is owed a post. A topic
listed there still has to clear the bar on its own merits the week it comes
up, and "I already thought about this one" is not a reason to lower it.

If a run drafts nothing at all, it makes no commits, so that week's reasoning
lives only in the run log. That is a known gap and it is deliberate — opening
a PR that contains no post would trip the next run's "don't stack up drafts"
check for no benefit.

## Auditing published posts

A second agent audits the archive monthly. Its job is **accuracy and
currency**: a post that was true when written can rot when Apple ships an OS,
fixes the bug, changes an API, or moves a documentation page.

What it checks:

- Every external link still resolves. Documentation URLs move constantly.
- Every quotation still matches its source verbatim.
- Technical claims still hold on current OS versions — a "this is
  undocumented" or "there is no API for this" claim is exactly the kind that
  expires quietly.
- The post still agrees with itself and with the other posts.

**It corrects in place. It does not remove posts, and it does not rewrite
history.** A URL that has been up for a while has accumulated search position
and inbound links; deleting it discards both and leaves a 404, and this site
is static hosting with no way to issue a real redirect. Correcting a post
keeps the URL and everything it has earned.

So: fix the wrong sentence, repoint the dead link, update the stale version
claim. Match the existing voice — a reader should not be able to tell which
sentences were revised. If a post is so wrong that correcting it would mean
rewriting the argument, **do not remove it and do not gut it** — report it and
let Kevin decide. That call is his.

The audit cannot judge whether a post is *read*. This site runs no visitor
analytics by deliberate choice, so there is no traffic data and the agent
should not pretend to reason about popularity. It audits whether a post is
still *correct*. Nothing more.

The one exception is Google Search Console, which the audit agent has no
access to and should not reason about either. It reports Google's index, not
visitors, and reading it is Kevin's job. Nothing in this repo contains
traffic data of any kind, so any claim about how a post performed would be
invented.

Same rules as everything else here: it opens a PR, and a human merges it.

## Files in here

- `README.md` — this contract
- `CONSIDERED.md` — topics weighed and rejected, and why
- `SOCIAL.md` — LinkedIn copy per post, copied out by hand
- `AUTOMATION.md` — how posts reach LinkedIn and elsewhere
- `index.html`, `feed.xml` — the post index and RSS feed
- `<slug>/index.html` — one directory per post

`../tools/og-image.py` generates a post's Open Graph card.

## The agents

Two scheduled cloud agents share this file:

- **Weekly** — reviews all active repos and either opens a post PR or reports
  that nothing cleared the bar.
- **Monthly** — audits published posts for accuracy and currency.

Neither publishes. Every change is merged by a human.

Both prompts point at this file rather than restating its rules, so
**editing the rules above changes what the agents do** — no need to touch
either routine.
