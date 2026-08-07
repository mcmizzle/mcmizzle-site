# Social copy

One section per post, newest first. Written to be copied and pasted as-is.

A link with no words around it performs badly and reads like a bot. These are
drafted alongside the post, reviewed in the same PR, and posted by hand — the
same draft-then-human-merge rule as everything else here. See "Social copy" in
`README.md` for how to write them.

**Two LinkedIn mechanics worth knowing.** The feed demotes posts carrying an
external link in the body, so the usual move is to post the text, then add the
link as the first comment. And only the first ~2 lines show before "see more",
so the hook has to survive being cut there.

---

## Your tvOS Top Shelf tile is cached, and reinstalling won't clear it

`https://mcmizzle.com/blog/tvos-top-shelf-stale-cache/`

### LinkedIn

```
I spent an evening debugging code that was already correct.

The Top Shelf tile for my tvOS app showed a placeholder instead of its
image. The title was right. The progress bar was right. Just no image. I
wrote two fixes, both wrong, and the thing that finally worked was
rebooting the Apple TV.

The part worth knowing: the system caches the rendered tile, dedupes
incoming content against that cache, and the cache survives a changed item
identifier and a full uninstall and reinstall of the app.

So if you have ever shipped even one build that handed the Top Shelf a bad
item, you can spend hours staring at correct code that produces a wrong
screen. Nothing about the symptom suggests a cache, which is exactly why it
costs so much time.

What I would carry past tvOS: all of my logging measured what the extension
sent. Nothing measured what the system drew, and the two had quietly
stopped being the same thing. When a fix that should work changes nothing —
not the symptom, not even its shape — stop refining the fix and start
asking whether your output is reaching the renderer.

Write-up below, including the exact log lines to search for, and what an
app extension can and can't do with an App Group.
```

---

## Why your HealthKit widget shows zero every morning

`https://mcmizzle.com/blog/healthkit-widget-shows-zero/`

### LinkedIn

```
My iPhone widget was wrong every morning, and right the moment I opened the
app.

The obvious read is that it's stale and needs to refresh harder. That was
wrong, and the tell was the timestamp: it said two minutes ago. The data
wasn't old. It was freshly wrong, which is a different bug with a different
cause, and it rules out every fix in the refresh-scheduling family.

HealthKit encrypts its store while the phone is locked. Background wakes
happen while the phone sits on a nightstand, so the reads most likely to
fail are precisely the ones running unattended — and a query that fails for
that reason reports no sum, identical to a day with genuinely no data.

I had written `?? 0`. So a failure became a confident zero, and every caller
downstream got a number that looked like data.

The general version is the part I'd actually keep: any `??`, `try?`, or
ignored error parameter whose default is 0 has made failure
indistinguishable from data. Zero is uniquely dangerous because it doesn't
look like an error state — it renders as a plausible, correctly formatted
number that nothing downstream can flag.

Write-up below, with the fix and the second bug that refusing to publish
garbage exposed.
```
