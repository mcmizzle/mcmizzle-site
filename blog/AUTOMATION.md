# Reaching people

## The strategy, and why it looks like this

Written down because there is no measurement. Nothing here can be evaluated
against traffic data, so the *reasoning* has to survive instead — otherwise
it gets re-argued from scratch every few months and drifts toward whatever
felt clever most recently.

**Four goals, all real:** app discovery, professional reputation, genuinely
helping engineers, and audience size. They pull in different directions and
none is dominant.

**So the selection rule is: prefer tactics that serve more than one goal at
once.** When you can't tell what worked, the way to avoid being wholly wrong
is to only do things that pay off on several axes. By that test:

| | apps | reputation | helping | audience |
|---|---|---|---|---|
| Answering a stuck forum thread | ~ | yes | yes | yes |
| Publishing a genuinely good post | yes | yes | yes | yes |
| LinkedIn post | ~ | yes | ~ | ~ |
| Crawlability hygiene | yes | no | no | yes |
| Chasing an aggregator spike | no | ~ | ~ | ~ |

The top two rows are the strategy. The rest is supporting work.

Forum answers are now part of the weekly run rather than an afterthought:
every post ships with a draft reply to a real unanswered thread. See
"Answering forum threads" in `README.md` for how targets are picked and why
a reply that stops helping when you delete the link is an advertisement.

**Time is the dominant variable, not tactics.** The domain was registered
2026-08-01. A new domain takes weeks to months to be crawled, indexed, and
ranked, and there is no way to buy past that. Anything done in a given week
shows up, if at all, a quarter later. Treat any tactic that promises faster
than that with suspicion.

**What this means in practice:** keep publishing at an honest bar, answer
forum threads where someone is actually stuck, stay crawlable, and let the
compounding happen. That is close to the whole plan, and its unglamorousness
is the point.

**Deliberately not doing:** visitor analytics of any kind, buying links,
posting the same content to five aggregators, cross-posting to Medium without
a canonical link, or publishing more often than the material justifies.

## Measurement, and its limits

The site is registered with **Google Search Console** and nothing else.

**Why that isn't a reversal of the no-tracking position.** Analytics watches
your visitors. Search Console reports what Google already knows about your
pages. It puts no code on the site, sets no cookies, and cannot identify a
visitor. Verification is a DNS TXT record, so not one byte of the site
changed. The privacy policy's promises were always scoped to the apps; the
site now has its own short section saying this plainly, which is more
trustworthy than the silence it replaced.

**Why set it up before there's anything to see.** There is no backfill. Data
starts the day you verify. Registering during the site's first week costs
nothing and preserves the only historical record of this period that will
ever exist.

**Use it as a diagnostic and a writing input, not a scoreboard.** The two
questions worth opening it for:

1. *Is anything actually indexed, and are there crawl errors?* A brand-new
   domain can fail silently for months, and you would have no other way to
   find out.
2. *Which queries surfaced a page?* This is the genuinely valuable one. It
   feeds what to write next, which is the highest-leverage decision in the
   whole system — the weekly agent currently picks topics on judgment alone.

**What it cannot tell you, which is most of what happens.** Search Console
sees Google search only. Click-throughs from an Apple Developer Forums reply,
LinkedIn referrals, a link pasted into someone's Slack, direct visits — all
invisible. The outreach that this file argues is the highest-value work is
precisely the part that stays unmeasured. Do not let the one measurable
channel quietly become the only one you work on, just because it is the one
with a number next to it. That is the specific way this goes wrong.

### Setting it up

Two accounts, both free at this volume: **Buffer** holds the queue you
approve from, **Zapier** moves copy out of the feed into it. Neither is
strictly required — see "Is this worth it" at the end.

Nobody but Kevin can do this: it needs accounts in his name and an OAuth
grant to his LinkedIn.

**1. Buffer — the queue.**
Sign up at <https://buffer.com>, connect the LinkedIn profile (not a company
page, unless that's the target). In Buffer's settings for that channel, make
sure posting is **manual/approval**, not automatic — if Buffer publishes on
its own schedule there is only one gate and this whole arrangement is
pointless. Install the phone app; approving from a phone is the difference
between this happening and not.

**2. Zapier — the mapping.**
Sign up at <https://zapier.com>, then **Create → Zaps → new Zap**.

*Trigger:*
- App: **RSS by Zapier**
- Event: **New Item in Feed**
- Feed URL: `https://mcmizzle.com/blog/social.xml`
- Test it. Two items should come back — the tvOS Top Shelf post and the
  HealthKit one. **Look at the test data before continuing.** You want to see
  the full LinkedIn copy in a field called `description`. If that field is
  empty or truncated, stop; something is wrong with the feed and it is worth
  fixing before building on it.

*Action:*
- App: **Buffer**
- Event: **Add to Queue** (not "Share Now")
- Connect the Buffer account, pick the LinkedIn channel
- **Text / Update field: insert the `description` field.** This is the whole
  point. Not `title`, not `link` — those give you the botlike title-plus-URL
  this file spends its length arguing against.
- Leave everything else default. Do **not** attach the `link` field; the URL
  goes in a first comment by hand.

Publish the Zap. It polls every 15 minutes on the free tier, so nothing
appears instantly.

**3. Prove it before trusting it.**
Both existing posts are already in the feed and unposted, so they will be the
first two queued. Open Buffer and read what actually landed. If it is the
full copy with paragraph breaks intact, the mapping is right. If it is a
title and a URL, the wrong field got mapped — go back to the action step.

**4. When you approve one.**
Post it, then immediately add the post URL as the first comment. The copy is
written expecting that, and it is the one part that cannot be automated.
Then mark the block **Posted YYYY-MM-DD** in `SOCIAL.md`.

**Labels move.** Both products redesign regularly, so if a button is named
something slightly different, the shape above still holds: RSS trigger,
Buffer queue action, map the description field, never auto-publish.

### Is this worth it

Honestly, maybe not. It is two accounts and two services in a chain, to
replace opening `SOCIAL.md` and pasting — about thirty seconds of work for
copy that is already written and reviewed.

It earns its place only if the friction of *remembering* is what stops posts
going out. If they would have gone out anyway, this is two more things to
maintain and two more places the chain can quietly break without telling you.

Try posting by hand for a few cycles first. If posts start getting skipped,
wire this up then. The feed costs nothing sitting unused.

### Why not deduplicate by removing items

Items stay in `social.xml` after they have been posted. Schedulers dedupe on
`<guid>`, which is the post URL and therefore stable, so each item is queued
exactly once. Pruning the feed would risk re-queueing everything if a
scheduler ever lost its state.

## The older option: Buffer's own RSS

If posting by hand stops happening, wire the feed up. `https://mcmizzle.com/blog/feed.xml`
is a valid RSS 2.0 feed with `title`, `link`, `guid`, `pubDate`, and
`description` on every item — everything a scheduler needs.

**Buffer** (free tier covers this): connect the LinkedIn account, add
`https://mcmizzle.com/blog/feed.xml` as a content source, and set it to queue
rather than publish automatically. Queueing keeps a human in the loop and lets
you replace the auto-generated text with the copy from `SOCIAL.md`.

**Zapier / IFTTT / Make** work the same way: *New item in feed* → *Create
LinkedIn post*. Same advice — draft, don't publish.

Whatever you use, feed polling is typically every 15–60 minutes on free tiers,
so a post won't appear instantly. That's fine; nothing here is time-sensitive.

### What not to build

A direct LinkedIn API integration. Posting to a personal profile needs a
LinkedIn app with the `w_member_social` scope and an OAuth flow, and their
app review is slow and unpredictable for a use case this small. Buffer already
solved it. Revisit only if you outgrow a scheduler, which one post a week will
not do.

## Elsewhere

Worth doing once per genuinely good post, by hand, not on a schedule:

- **Hacker News** — Show HN doesn't fit, but a plain submission does. Submit
  once; resubmitting the same URL is penalized.
- **lobste.rs** — invite-only, but a better audience for this material than HN.
  Tag `ios`/`swift`/`debugging`.
- **r/iOSProgramming**, **r/swift** — read each subreddit's self-promotion rule
  first; several require a participation ratio.
- **Apple Developer Forums** — the strongest option, and the least
  spammy-feeling. Both current posts identified real forum threads asking the
  exact question with no good answer. Answering the question *in the thread*,
  with the post as supporting detail, helps someone who is stuck right now and
  earns a link that will keep sending traffic for years.

The last one is the highest value per unit effort and the easiest to forget.

## A caveat about measuring any of this

None of the channels above can be evaluated by traffic. Search Console covers
Google search and nothing else, so a forum reply, a LinkedIn post, or a link
pasted into a Slack all land completely unmeasured. LinkedIn and Reddit report
their own engagement numbers, which is something, but you will not learn what
any of it did to the site.

That's a deliberate trade rather than an oversight — see "Measurement, and its
limits" above.
