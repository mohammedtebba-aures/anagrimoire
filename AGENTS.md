# Anagrimoire

A word roguelike for PC (Windows and Linux). Godot 4 with C#. Solo project, run with team
practices deliberately.

## Non-negotiable architecture

**`src/WordRoguelike.Core` must never reference Godot.**

No `using Godot;`. No `Node`, `Vector2`, `Resource` or any engine type in a
signature. No `GD.Print`. If you find yourself wanting one, the logic belongs
in `src/WordRoguelike.Game` instead, or the dependency should be inverted
behind an interface.

This is what lets the entire rules engine run under `dotnet test` on a bare CI
runner in seconds, with no engine and no display server. Breaking it breaks the
pipeline and the project's whole reason for being structured this way.

**All randomness is seed-driven.**

Never `new Random()` inside Core. RNG is injected. Given the same seed, a run
must replay identically. This makes failures reproducible, makes tests possible,
and is the foundation a daily-challenge mode would be built on later.

**Solutions**

- `WordRoguelike.Core.sln` — Core + Tests only. This is what CI builds.
- `WordRoguelike.sln` — adds the Godot project. Local development only.

Godot regenerates `src/WordRoguelike.Game/*.csproj` if it goes missing. The
`ProjectReference` to Core is committed; re-check it after any Godot upgrade.

## Layout

```
src/WordRoguelike.Core/     pure C# rules engine
src/WordRoguelike.Game/     Godot project (project.godot here)
tests/WordRoguelike.Core.Tests/
docs/adr/                   architecture decision records
```

## Current state

Sprint 0. The rules engine does not exist yet. Issue #2 (proving C# desktop
export works end to end on Windows and Linux) should pass before game code is
built on top. ADR 0002 records why the target moved from Android to PC.

Sprints 0 and 1 produce **no UI**. The first milestone is a complete run
playable as text through a console harness. If it is not fun as text, art will
not save it. Do not start building Godot scenes ahead of that.

## Conventions

**Commits** follow Conventional Commits:

```
feat(core): weight letter bag by frequency table
fix(core): reshuffle discard when draw pile empties mid-hand
test(core): cover scoring multipliers for 7-letter words
```

Subject under 72 chars, imperative, no trailing period. Footer `Closes #42`.

**Branches** carry the issue number: `feat/42-letter-bag-draw`,
`fix/57-shuffle-off-by-one`, `chore/12-bump-godot`.

**Every change goes through a PR.** `main` is protected; no direct pushes.
One issue, one branch, one PR. Branches live hours to days. A branch older than
four days is too big and should be split.

**Run `dotnet format` before committing.** CI fails on unformatted code.

**Warnings are errors** via `Directory.Build.props`. Do not suppress a warning
to get a build green — fix it, or explain the suppression in the PR.

## Testing

xUnit. Test behaviour, not implementation. Every issue needs the happy path
plus at least two edge cases.

The edges that actually matter here: empty bag, drawing more than the bag
holds, reshuffle triggered mid-draw, a word reusing a single tile twice, a word
longer than the hand, zero-length input, removing the last copy of a letter.

Seeded tests must assert reproducibility, not just plausibility.

## Decisions

Non-reversible choices go in `docs/adr/` using `docs/adr/template.md`. Never
delete an ADR; supersede it and mark the old status.

Read `docs/adr/0001-csharp-and-engine-independent-core.md` before proposing any
change to the layering. It records what the C# choice costs as well as what it
buys.

## Known constraints

- Targets are Windows and Linux desktop (ADR 0002). Both must be tested on a
  real machine; "it exported" is not "it runs". Linux is also the path to
  Steam Deck.
- Release exports can behave differently from the editor. Anything reflective
  (save serialization is the usual culprit) must be verified in an exported
  release build, not just by running from the editor.
- C# web export is not supported. There is no browser build; playtests use
  downloadable builds.
- The word list licence is recorded in ADR 0003. Do not swap the word list
  without checking the replacement's licence permits commercial use.

## Working with me on this repo

Suggest the smallest change that closes the issue. If a change needs to touch
the layer boundary or an ADR, say so before writing code rather than after.

When something in this file conflicts with what seems convenient, the file
wins. Raise the conflict instead of quietly working around it.
