# ADR 0002: Target PC (Windows and Linux) instead of Android

- **Status:** Accepted
- **Date:** 2026-11-25
- **Deciders:** Moh

## Context

ADR 0001 chose C# with an engine-independent Core for a game targeting
Android. Since then the project's goal has shifted: it is built for its own
sake, and if it turns out well the plan is to sell it on Steam. Steam is a PC
storefront, and the roguelike/deckbuilder audience there is large and used to
paying for small indie games.

Android was also the source of ADR 0001's largest risk. C# Android export in
Godot 4 is flagged experimental, and issue #2 existed to prove it worked before
any game code was written.

## Decision

Target PC: Windows and Linux desktop builds, distributed through Steam if the
game is released. Android is dropped as a target. No macOS build is planned.

ADR 0001's decision (C#, with a rules Core that never references Godot) is
unchanged. Only its platform context is superseded.

## Consequences

**Positive**

- C# desktop export in Godot 4 is not experimental, so ADR 0001's largest
  risk goes away. Issue #2 shrinks to a quick confirmation instead of a
  blocker that could invalidate the language choice.
- No keystore, no AAB, no Play Store signing to manage.
- A Linux build is close to free with Godot and is a step towards running on
  Steam Deck.
- Mouse and keyboard make typing words natural, which suits a word game.

**Negative**

- C# still has no web export, so there is no browser build on itch.io.
  Playtesting needs a downloadable build (itch.io or Steam Playtest), which
  is more friction for strangers than a browser link.
- Two desktop platforms to test instead of one phone. Linux builds need
  testing on a real Linux machine or Steam Deck, not just "it exported".
- Steam has a one-off fee per game and a store page to maintain, and the PC
  roguelike market is crowded.
- The UI is now designed for a large screen with a mouse. Porting back to
  touch later would mean reworking input and layout.

## Alternatives considered

**Stay on Android.** Rejected: the plan to sell is on Steam, and Android
carried the only experimental export path in the stack.

**Android and PC together.** Rejected for now: two input models and the
experimental Android path double the testing for one person. Core stays
platform-free, so a mobile port remains possible later.

**Switch the Godot layer to GDScript to get a web build.** Rejected: the
reasons for C# in ADR 0001 (testable Core, typing, CV value) still hold, and
a downloadable playtest build is an acceptable cost.

## Revisit when

- Godot ships C# web export, which would bring back cheap browser playtests.
- A mobile release becomes a real plan, e.g. after a Steam launch does well.

---

Note: issue #2 previously reserved ADR 0002 for recording the Godot version.
That record now goes in ADR 0003.
