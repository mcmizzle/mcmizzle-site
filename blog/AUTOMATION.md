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

**Time is the dominant variable, not tactics.** The domain was registered
2026-08-01. A new domain takes weeks to months to be crawled, indexed, and
ranked, and there is no way to buy past that. Anything done in a given week
shows up, if at all, a quarter later. Treat any tactic that promises faster
than that with suspicion.

**What this means in practice:** keep publishing at an honest bar, answer
forum threads where someone is actually stuck, stay crawlable, and let the
compounding happen. That is close to the whole plan, and its unglamorousness
is the point.

**Deliberately not doing:** analytics of any kind, buying links, posting the
same content to five aggregators, cross-posting to Medium without a canonical
link, or publishing more often than the material justifies.

## Getting posts onto LinkedIn

Two ways. Start with the manual one — it's better copy and takes two minutes.

## The recommended path: post by hand

Every post ships with a LinkedIn draft in `blog/SOCIAL.md`, written and
reviewed in the same PR. When the post merges:

1. Open `blog/SOCIAL.md`, copy the LinkedIn block for the newest post.
2. Paste it to LinkedIn. **No link in the body** — the feed demotes posts
   carrying external links.
3. Post, then immediately add the post URL as the first comment.

This wins on quality and costs almost nothing. Auto-posted RSS reads like a
bot, because it is one: the title plus a URL, with none of the hook that makes
someone stop scrolling.

## The automated path: RSS to Buffer

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

This site runs no analytics, deliberately — `/privacy/` promises none, and
both App Store listings point at that page. So none of the above can be
evaluated by traffic. LinkedIn and Reddit will show you their own engagement
numbers for your posts, which is something, but you will not know what any of
it did to the site. That's a deliberate trade, not an oversight. See #7.
