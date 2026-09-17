# ADR 0001: C# with an engine-independent rules core

- **Status:** Accepted
- **Date:** 2026-09-17
- **Deciders:** Moh

## Context

The game is a word roguelike targeting Android, built in Godot 4, developed
solo in free time over a period measured in months. A secondary and explicit
goal is to practise engineering discipline that transfers to a hiring
conversation: automated tests, CI, code review, release process.

Godot offers GDScript and C#. Two things drive the choice:

1. The rules of a deckbuilder are almost entirely pure logic. Bag composition,
   draw and discard, word validation, scoring, relic modifiers, run
   progression. Almost none of it needs the engine.
2. Whatever runs in CI has to run fast and cheaply. A test suite that needs a
   headless engine boot on every push is slower, more fragile, and burns
   free-tier minutes.

## Decision

Use C#, and split the repository into a pure .NET class library holding the
rules engine and a Godot project that consumes it.

`WordRoguelike.Core` has no reference to Godot. No `using Godot;`, no engine
types in signatures, no `GD.Print`. Randomness enters through an injected seed.
The word list enters through an interface. The Godot project depends on Core;
Core depends on nothing.

CI builds a solution containing only Core and its tests, so the test job runs
on a bare ubuntu runner with the .NET SDK and nothing else.

## Consequences

**Positive**

- The entire rules engine is unit testable with xUnit and `dotnet test`, no
  engine, no display server, no headless runner.
- Seed-driven determinism makes runs reproducible, which makes failures
  reproducible and enables a daily-challenge mode later without rework.
- Static typing, real refactoring tooling, and NuGet.
- The architecture itself is defensible in an interview, which is part of the
  point of the project.
- The rules engine could later be driven from a different front end (a console
  harness, a web version) without touching it.

**Negative**

- C# mobile export in Godot 4 is still flagged experimental. Android support
  uses the linux-bionic Mono runtime, supports only arm64 and x64, and lacks
  Android bindings, so some platform APIs are unavailable or crash. Godot's own
  APIs must be preferred. Godot 4.5+ additionally needs the .NET 9 SDK at build
  time. This is the largest project risk and is why issue #2 validates a signed
  AAB on a physical device before any game code is written.
- C# web export is not supported, so there is no browser build for itch.io.
  That removes the cheapest channel for getting strangers to playtest early.
  Accepted: Android is the stated target, and playtesting will use the internal
  testing track instead.
- Most Godot tutorials and a portion of addons are GDScript. Expect translation
  friction.
- Slower iteration than GDScript because of the compile step.
- The layer boundary costs discipline. It is easy to leak a `Vector2` into Core
  to save five minutes. This is the first thing checked in code review.

## Alternatives considered

**GDScript.** Faster iteration, better tutorial coverage, first-class mobile
export with no experimental caveat. Rejected because the test story is weaker
(gdUnit4 or GUT running the engine headless in CI), the language is
Godot-specific so it carries less weight on a CV, and the dynamic typing works
against a codebase intended to grow over months.

**A different engine (Unity, Flutter, React Native).** React Native is the
familiar stack and would export to Android without caveats, but a roguelike
with animation and juice is not what it is good at. Rejected in favour of
building game-dev skill deliberately.

## Revisit when

- Godot removes the experimental flag from C# Android export.
- Issue #2 fails, meaning C# Android export does not work for this setup. In
  that case the fallback is GDScript for the Godot layer with Core ported, or
  reconsidering the engine entirely. Deciding this early is the entire reason
  #2 comes before any game code.
