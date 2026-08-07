# Considered and passed on

Topics that were weighed for a post and rejected, with the reason. See
"Record what you passed on" in `README.md` for why this file exists.

**This is a record, not a queue.** Nothing here is owed a post. A topic
listed below still has to clear the bar on its own merits, and having been
considered before is not a reason to lower it.

Newest first. Note the date, the repo, the commit or issue if there is one,
and — most importantly — *why it lost*, specifically enough that a later run
doesn't have to re-derive the whole judgment.

---

## 2026-07-27

### AmbientCast — `AVSampleBufferDisplayLayer` fails after backgrounding
`f067101`, issue #80. The symptom is the best in any of the repos: the
sample-buffer layer went transparent when decoding was revoked, so the
composited layer behind it showed through and a decode failure presented as
the Pro watermark appearing over the dashboard. A UI bug that was really a
video bug.

**Lost on the search test.** Apple documents `requiresFlushToResumeDecoding`
and the flush-to-recover contract directly, and there is a long-standing
WebKit bug covering the backgrounding case. The rules exclude anything
already covered well by first-party docs.

*Worth revisiting only if reframed around the symptom* — the cause is
documented, but "the watermark appeared and it turned out to be a decode
failure" is not something a search currently answers.

### scorebridge — a link watchdog that killed healthy connections
`d65fb20`, issue #25. Genuinely excellent material. Liveness was measured via
ATT acks, only the keepalive produced one, and the keepalive was gated on
write-idleness — so activity suppressed the very probe that proves activity,
and the busier the link got, the faster it tore itself down. The fix renamed
the parameters so that passing the wrong clock now reads as wrong at the call
site.

**Lost on two counts:** it sits inside a reverse-engineered proprietary BLE
protocol, so it needs heavy generalization before it could be published
safely at all; and the lesson ("a health check must run on its own clock")
is closer to a design principle than a platform gotcha.

*Strongest candidate on this list.* It would have to be written as a
protocol-agnostic piece about liveness-probe design — no frame codes, no
vendor protocol details, no hardware specifics. If that version clears the
bar on its own, write it.

### AmbientCast — `INFOPLIST_KEY_UIBackgroundModes` not synthesized
Real, well-diagnosed, and genuinely undocumented — a canary key proved the
failure wasn't specific to that key name. **Lost on size:** it is a few
paragraphs, not a post, and there is no short-form format on this site.

### CalorieBurndown — the watch complication staleness saga
Issue #17, 16+ rounds. **Lost on shape.** Too long, too inconclusive, and its
honest ending is "this is the platform's ceiling and we accepted it." Several
individual lessons are sharp; the arc is not a post.

---

## 2026-08-03

### AmbientCast — hand-written pbxproj Top Shelf target
Issue #4. A fabricated `com.apple.product-type.tv-app-extension` and a
missing explicit `TVServices.framework` link. Strong story, but it overlaps
the Top Shelf cache post's subject area and only one topic ships per week.
**Genuinely queued** rather than rejected — no defect in the material.

### CalorieBurndown — watchOS background-refresh chain dies on one expired task
Issue #17, round 14. `scheduleNext()` ran only at the end of the task's async
work with no expiration handler, so a single revoked task ended the chain
permanently — recoverable only by reboot or the user reopening the app. Very
good material.

**Lost because the fix is still marked unverified** in CLAUDE.md: confirming
it needs a multi-hour hands-off cycle. Don't publish a fix that hasn't been
shown to work. Revisit once it's confirmed on device.

### scorebridge — the watchdog again
Reconsidered and rejected a second time, with sharper detail than the first
pass: the liveness probe was only sent after 4s of *write* idleness and only
the probe was written with-response, so busy traffic suppressed the signal
proving traffic was getting through — the busier the link, the faster the
watchdog fired, which is why a live game never triggered it.

Same two reasons as before. **If it's ever written, write it as a pure
CoreBluetooth write-with/without-response piece with the wire format
entirely absent.**
