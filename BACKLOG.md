# Seeded backlog

Copy each item into a GitHub issue using the task template. Numbers below
assume they are created in order.

## The target for the first two sprints

A complete run, playable start to finish, **in a console harness with no UI at
all**. No Godot scenes, no art, no animation. Just: a bag of letters, a hand, a
word, a score, an encounter resolved, a reward that changes the bag, repeat,
run ends.

If that is not fun to play as text output, no amount of art will save it. This
is also the cheapest possible way to find out whether the core mechanic works,
and it is 100% testable.

---

## Sprint 0 — De-risk and scaffold

The goal is not to build anything. It is to prove the ground is solid and the
pipeline is green.

### #1 Repository and solution skeleton
**Layer:** Infra · **Size:** M

- [ ] GitHub repo created, public
- [ ] `src/WordRoguelike.Core` class library, `tests/WordRoguelike.Core.Tests` xUnit project
- [ ] `WordRoguelike.Core.sln` contains only those two projects
- [ ] `Directory.Build.props` sets `TreatWarningsAsErrors`, `Nullable=enable`, `LangVersion=latest`
- [ ] One trivial passing test proves the harness works
- [ ] `.gitignore` for .NET and Godot (`.godot/`, `bin/`, `obj/`, `*.user`)
- [ ] CONTRIBUTING.md, PR template, issue template, ADR 0001 committed
- [ ] `ci.yml` added and green on the first PR
- [ ] Branch protection on `main`: no direct pushes, CI required to pass

### #2 Prove C# Android export end to end — BLOCKING
**Layer:** Infra · **Size:** M · **Risk:** high

Nothing else matters until this works. Do it before writing game code.

- [ ] Godot .NET build installed, version recorded in the ADR
- [ ] Minimal Godot project at `src/WordRoguelike.Game` with one button and one label
- [ ] Game project references `WordRoguelike.Core`, calls one method from it, displays the result
- [ ] Debug APK runs on a physical Android phone
- [ ] Release keystore generated and **backed up off this machine**
- [ ] Signed AAB produced
- [ ] AAB uploaded to Play Console internal testing track and installed from there
- [ ] Any workarounds needed are written down in ADR 0002

> If this fails, stop and reopen the language decision. That is what ADR 0001's
> "revisit when" clause is for.

### #3 Choose and license a word list
**Layer:** Core · **Size:** S

- [ ] Candidate lists compared (ENABLE, SOWPODS, dwyl/english-words and similar)
- [ ] Licence verified as compatible with a commercial Play Store release
- [ ] Decision and licence recorded in ADR 0003 with the source URL
- [ ] File committed or vendored with attribution as the licence requires
- [ ] Word count and file size recorded

### #4 Google Play developer account
**Layer:** Infra · **Size:** S

- [ ] Account registered, one-time fee paid
- [ ] Identity verification completed (this can take days, start it early)
- [ ] App listing created as a draft, internal testing track set up

---

## Sprint 1 — The rules engine

Every issue here is pure C# with tests. Zero Godot.

### #5 Letter tiles and the bag
**Layer:** Core · **Size:** M

- [ ] `LetterTile` record with letter, point value, and any modifier flags
- [ ] `Bag` holds a multiset of tiles
- [ ] Starting bag composition defined in data, not hardcoded in logic
- [ ] Bag construction is pure and takes no RNG
- [ ] Tests: composition totals, adding, removing, duplicate handling

### #6 Deterministic draw, discard and reshuffle
**Layer:** Core · **Size:** M

Determinism is not optional. It makes every later test possible and it is what
a daily-challenge mode would be built on.

- [ ] RNG injected as a seeded source, never `new Random()` inside logic
- [ ] Draw to a hand of N
- [ ] Played tiles go to discard
- [ ] Draw pile empty mid-draw reshuffles the discard and continues
- [ ] Tests: same seed produces an identical sequence across runs
- [ ] Tests: reshuffle mid-draw, drawing more than the bag holds, empty bag

### #7 Word validation
**Layer:** Core · **Size:** M

- [ ] `IWordSource` interface so Core does not know about files
- [ ] In-memory implementation backed by a `HashSet<string>`
- [ ] A word is valid only if it is in the list **and** buildable from the hand
- [ ] Case and whitespace normalised on load and on lookup
- [ ] Measure load time and memory on a real phone, record it in the issue
- [ ] Tests: valid word, word not in list, word using letters not in hand,
      word reusing a single tile twice, empty string

### #8 Scoring
**Layer:** Core · **Size:** M

- [ ] Base score from letter values
- [ ] Length multiplier curve, defined in data
- [ ] Per-tile modifiers apply in a defined, documented order
- [ ] Tests: each multiplier tier, modifier stacking order, minimum-length word

### #9 Encounter resolution
**Layer:** Core · **Size:** M

- [ ] `Encounter` with a target score and a limited number of turns
- [ ] Submitting a word advances the encounter and returns a result
- [ ] Win and loss conditions
- [ ] Tests: win on the final turn, loss by running out of turns, exact-target edge

### #10 Rewards that modify the bag
**Layer:** Core · **Size:** M

This is the roguelike loop. Without it the game is just a word game.

- [ ] Reward types: add a tile, upgrade a tile, remove a tile
- [ ] Three rewards offered after each encounter, drawn from the seeded RNG
- [ ] Applying a reward returns a new bag; bag mutation is explicit
- [ ] Tests: each reward type, offers are deterministic per seed, removing the
      last copy of a letter

### #11 Run state machine
**Layer:** Core · **Size:** L — consider splitting

- [ ] `RunState` sequences encounters, rewards, and run end
- [ ] Full run playable through a console harness in `tests/` or a scratch project
- [ ] A seed plus a list of played words fully reproduces a run
- [ ] Tests: complete winning run, run lost at encounter 2, reproducibility

### #12 Retro and CHANGELOG
**Layer:** Docs · **Size:** S

- [ ] Actual time recorded on every closed issue, compared against the estimate
- [ ] `CHANGELOG.md` started, Keep a Changelog format
- [ ] Retro notes in `docs/retros/sprint-01.md`

---

## Parked — deliberately not yet

Do not touch these until a run is playable as text.

- Godot UI, scenes, tile rendering, animation
- Save and resume
- Meta-progression between runs
- Daily challenge with a shareable spoiler-free result
- Audio
- Monetisation
- Art commission
- Steam or iOS
