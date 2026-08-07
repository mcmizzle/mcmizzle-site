# Social copy

One section per post, newest first. Written to be copied and pasted as-is.

A link with no words around it performs badly and reads like a bot. These are
drafted alongside the post, reviewed in the same PR, and posted by hand — the
same draft-then-human-merge rule as everything else here. See "Social copy" in
`README.md` for how to write them.

**Do not hard-wrap anything inside the fenced blocks.** Every destination here
— the Apple Developer Forums editor, LinkedIn's composer — preserves the line
breaks you paste and wraps the text itself. Hard-wrapped prose arrives looking
ragged, with a break every 70-odd characters that nothing in the destination
undoes. So each paragraph is one long line, separated by blank lines, and the
long lines are deliberate. Only genuine code and log samples keep their breaks,
because there the breaks are meaningful.

**Two LinkedIn mechanics worth knowing.** The feed demotes posts carrying an
external link in the body, so the usual move is to post the text, then add the
link as the first comment. And only the first ~2 lines show before "see more",
so the hook has to survive being cut there.

---

## Your tvOS Top Shelf tile is cached, and reinstalling won't clear it

`https://mcmizzle.com/blog/tvos-top-shelf-stale-cache/`

### Apple Developer Forums — thread 126398

Target: <https://developer.apple.com/forums/thread/126398> — *"Lifecycle of a
tvOS 13.2 TopShelf extension?"*

Opened Nov 2019, **never answered**, with three other developers confirming
the same thing through 2021 — and the behavior clearly still exists, since it
reproduces on the tvOS 27.0 public beta. The shared mystery is "a reboot fixes
it and nothing else does," which is exactly what happened here.

The draft is deliberate about not overclaiming: their symptom is the extension
not running at all, ours was a running extension whose output never reached
the screen. Those may be different bugs. Say so rather than implying a fix.

```
Late to this thread, but it still happens on the tvOS 27.0 public beta (24J5325d), on an Apple TV 4K (3rd gen), with an app whose deployment target is tvOS 17. I don't think the caching angle has come up here.

Something a reboot does that reinstalling doesn't: the Home screen process caches the *rendered* Top Shelf tile and dedupes incoming content against that cache. In my case that cache survived a changed item identifier and a full uninstall and reinstall of the app, and kept drawing a tile built from an earlier build for hours while the current code was correct.

The log line that finally showed it:

    Skipping content update for [com.example.app] because it is unchanged

If your item identifier is a constant, a corrected item is indistinguishable from the cached one, so a fix to what's *in* the tile can never reach the screen. Deriving the identifier from the content you're rendering closes that particular trap. (Use the content string itself, not its hashValue — Swift seeds Hashable per process, so a hash changes every launch regardless of content, which isn't what you want.)

I want to be careful not to overclaim: your symptom is the extension not running at all after an Xcode relaunch, and mine was a running extension whose output wasn't reaching the screen. Those may well be different bugs. But if you're in the position of "only a reboot fixes it," it's worth checking whether the system is even accepting your content before concluding the extension is dead.

Two other things that cost me an evening and are much easier to state than to discover:

- print() from a Top Shelf extension reaches nobody, and `log stream` has no device flag. os.Logger at .notice, read in Console.app with the Apple TV tethered, is the channel that works. Not .debug, which isn't persisted by default and so is missing from exactly the capture you collected.

- An extension can *read* the shared App Group container but is sandbox-denied from *creating files* in it — `deny(1) file-write-create`, surfacing as NSCocoaErrorDomain 513. The containing app has no such restriction. If you need something dynamic on the shelf, the app writes it and the extension only reads it.

Full write-up if it's any use: https://mcmizzle.com/blog/tvos-top-shelf-stale-cache/
```

### LinkedIn

```
I spent an evening debugging code that was already correct.

The Top Shelf tile for my tvOS app showed a placeholder instead of its image. The title was right. The progress bar was right. Just no image. I wrote two fixes, both wrong, and the thing that finally worked was rebooting the Apple TV.

The part worth knowing: the system caches the rendered tile, dedupes incoming content against that cache, and the cache survives a changed item identifier and a full uninstall and reinstall of the app.

So if you have ever shipped even one build that handed the Top Shelf a bad item, you can spend hours staring at correct code that produces a wrong screen. Nothing about the symptom suggests a cache, which is exactly why it costs so much time.

What I would carry past tvOS: all of my logging measured what the extension sent. Nothing measured what the system drew, and the two had quietly stopped being the same thing. When a fix that should work changes nothing — not the symptom, not even its shape — stop refining the fix and start asking whether your output is reaching the renderer.

Write-up below, including the exact log lines to search for, and what an app extension can and can't do with an App Group.
```

---

## Why your HealthKit widget shows zero every morning

`https://mcmizzle.com/blog/healthkit-widget-shows-zero/`

### Apple Developer Forums — thread 756794

Target: <https://developer.apple.com/forums/thread/756794> — *"Background
Health Store Access for Lock Screen Widgets"*

Opened June 2024, still open. The poster wants widgets to update while the
phone is locked, and filed FB13879739 about it. **We can't solve that** — and
the draft says so up front rather than pretending otherwise.

What we can contribute is the failure mode *next to* their problem: what
happens when you work around the locked store badly. That's a real
contribution to an unanswered thread without overstating what we know.

Do not open with the link, and don't answer a question that wasn't asked.

```
I don't have a way around the locked-store restriction either. There's now an explicit DTS answer confirming reads aren't permitted while locked (thread 824819, May 2026), so I've stopped hoping for one.

What I can offer is the failure mode I hit while working around it, because it's easy to ship by accident and it presents as a completely different bug.

A statistics query that fails because the store is encrypted reports no sum. That is the same thing it reports for a day with genuinely no samples. So if your read does something like

    result?.sumQuantity()?.doubleValue(for: unit) ?? 0

and binds the error parameter to _, a failed read returns a confident 0. Mine then got published to the widget with a *current* timestamp, so every morning the widget showed a plausible, freshly-stamped, completely wrong zero until the app was next opened. It reads exactly like a refresh bug — I lost time on timeline reloads and App Group configuration before noticing the timestamp was fresh, which meant the data wasn't stale, it was freshly wrong.

What worked, given we can't read while locked:

- Return an optional from the read. nil for a failed query, and 0 only for HKError.errorNoData, which is HealthKit's way of saying the range really is empty.

- On failure, publish nothing and leave the previous values untouched. A widget showing yesterday's number is far better than one showing a wrong number today.

- Audit every path that writes to the widget, not just the one you fixed. A freshly-initialized model object is full of zeros too, and those are every bit as plausible as the ones a failed query produces.

- Carry the day the numbers describe separately from the "updated at" time. Once a write can be skipped, "when was this written" stops answering "which day is this about" — and that distinction is what lets you render a stale payload as visibly stale instead of asserting it.

None of that gets data while locked. It does stop the lock from producing wrong data, which in my case was the actual user-visible bug.

Longer version: https://mcmizzle.com/blog/healthkit-widget-shows-zero/
```

### LinkedIn

```
My iPhone widget was wrong every morning, and right the moment I opened the app.

The obvious read is that it's stale and needs to refresh harder. That was wrong, and the tell was the timestamp: it said two minutes ago. The data wasn't old. It was freshly wrong, which is a different bug with a different cause, and it rules out every fix in the refresh-scheduling family.

HealthKit encrypts its store while the phone is locked. Background wakes happen while the phone sits on a nightstand, so the reads most likely to fail are precisely the ones running unattended — and a query that fails for that reason reports no sum, identical to a day with genuinely no data.

I had written `?? 0`. So a failure became a confident zero, and every caller downstream got a number that looked like data.

The general version is the part I'd actually keep: any `??`, `try?`, or ignored error parameter whose default is 0 has made failure indistinguishable from data. Zero is uniquely dangerous because it doesn't look like an error state — it renders as a plausible, correctly formatted number that nothing downstream can flag.

Write-up below, with the fix and the second bug that refusing to publish garbage exposed.
```
