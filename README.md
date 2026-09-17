# Anagrimoire

A word roguelike for Android, built in Godot 4 with C#. Solo project run with team practices deliberately: CI, tests, code review, and architecture decision records.

## Architecture

The rules engine lives in `src/WordRoguelike.Core` and has **no Godot dependency**. It runs under `dotnet test` on a bare .NET SDK, so CI is fast and deterministic. The Godot project (`src/WordRoguelike.Game`) consumes Core but is not in the CI solution.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the working agreement and [ADR 0001](docs/adr/0001-csharp-and-engine-independent-core.md) for why the split exists.

## Current state

Sprint 0. Issue #2 (proving C# Android export works end to end) is **blocking**; nothing else should be built on top until it passes.

## Verify locally

```bash
dotnet format WordRoguelike.Core.sln --verify-no-changes
dotnet test WordRoguelike.Core.sln -c Release
```

Requires the .NET 9 SDK (Godot 4.5+ C# Android export needs it at build time).
