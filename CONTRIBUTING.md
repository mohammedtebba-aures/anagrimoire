# Working agreement

This is a solo project run with team practices on purpose. The point is that
the process survives contact with a real codebase, not that it looks tidy.

## Repository layout

```
/
├── WordRoguelike.Core.sln       # Core + Tests ONLY. This is what CI builds.
├── WordRoguelike.sln            # Core + Tests + Godot project. Local dev.
├── src/
│   ├── WordRoguelike.Core/      # Pure C#. NO Godot reference. The rules engine.
│   └── WordRoguelike.Game/      # The Godot project (project.godot lives here).
├── tests/
│   └── WordRoguelike.Core.Tests/
├── docs/
│   └── adr/                     # Architecture Decision Records
└── .github/
    ├── workflows/ci.yml
    ├── ISSUE_TEMPLATE/
    └── pull_request_template.md
```

**The two-solution split is deliberate.** CI builds `WordRoguelike.Core.sln`,
which has no Godot dependency, so the test job runs in seconds on a plain
ubuntu runner with nothing but the .NET SDK. The Godot project is only needed
for export jobs and local work.

**`WordRoguelike.Core` must never reference Godot.** No `using Godot;`, no
`Node`, no `Vector2`, no `GD.Print`. If the rules engine needs randomness it
takes an injected seed. If it needs a word list it takes a `IWordSource`. This
is the rule that makes the whole test suite possible, and it is the first thing
to check in review.

> Godot regenerates `src/WordRoguelike.Game/*.csproj` if it goes missing, so the
> `ProjectReference` to Core is committed and should be re-checked after any
> Godot version upgrade.

## Branching

Trunk-based. `main` is always releasable and protected.

```
feat/42-letter-bag-draw
fix/57-shuffle-off-by-one
chore/12-bump-godot-4-6
docs/adr-0003-dictionary-source
```

Branch name carries the issue number. One issue, one branch, one PR.
Branches live hours to days, never weeks. If a branch is older than four days
it is too big and should be split.

## Commits

[Conventional Commits](https://www.conventionalcommits.org/). The type prefix
is what generates the changelog later.

```
feat(core): weight letter bag by frequency table
fix(core): reshuffle discard when draw pile empties mid-hand
test(core): cover scoring multipliers for 7-letter words
chore(ci): cache nuget packages between runs
docs(adr): record dictionary licence decision
refactor(core): extract EncounterResolver from RunState
```

Subject line under 72 characters, imperative mood, no trailing period.
Body explains *why* when the why is not obvious. Footer: `Closes #42`.

## Pull requests

Every change goes through a PR. No direct pushes to `main`, including yours.
Branch protection enforces this so the habit is not optional.

1. Open the PR against `main` with the template filled in.
2. CI must be green. A red PR is not reviewable.
3. Request review. Paste the diff or the PR link into the review session.
4. **Brief the reviewer adversarially.** Say "find the three worst problems
   with this" rather than "review this". A reviewer who helped design the
   thing will drift toward approving it unless explicitly told to attack it.
5. Respond to every comment. Push back where you disagree and say why. Silent
   acceptance of review comments teaches you nothing.
6. Squash merge. The PR title becomes the commit message, so it follows
   Conventional Commits too.
7. Delete the branch.

### What review looks for, in order

1. Does `Core` still have zero Godot dependencies?
2. Is the new logic deterministic and seed-driven?
3. Are the tests testing behaviour, or just re-stating the implementation?
4. What happens at the boundaries: empty bag, zero-length word, duplicate
   letters, a word longer than the hand?
5. Is this the smallest change that closes the issue?
6. Naming, readability, dead code.

## Definition of Done

An issue is not done until every line is true. No partial credit.

- [ ] Acceptance criteria in the issue are all met
- [ ] New logic lives in `Core` unless it is genuinely presentation
- [ ] Unit tests cover the happy path and at least two edge cases
- [ ] `dotnet test` passes locally
- [ ] `dotnet format --verify-no-changes` passes
- [ ] CI is green on the PR
- [ ] No new compiler warnings
- [ ] Public types and non-obvious methods have XML doc comments
- [ ] If a non-reversible technical choice was made, an ADR exists
- [ ] PR reviewed, comments answered, approved
- [ ] Squash merged, branch deleted, issue auto-closed

## Iteration cadence

One week, Monday to Friday. Weeks are fixed; scope is not.

**Monday, sprint planning (~30 min).** Agree one sprint goal, stated as an
outcome not a task list. Pull issues from the backlog into the board. Write
acceptance criteria on each one before it enters the sprint. Anything without
acceptance criteria is not ready and stays in the backlog.

**Daily standup (2 lines).** Yesterday / today / blockers. This is not a status
report, it is practice at articulating a blocker precisely enough that someone
could unblock you.

**Friday, demo and retro (~30 min).** Demo means actually running it, not
describing it. Retro answers three questions: what worked, what did not, what
one thing changes next week. Write the CHANGELOG entry for anything merged.

**Sprint goal examples**

- Good: "A full run can be played end to end in the console with no UI."
- Bad: "Finish the bag, scoring, and dictionary."

## Estimation

Size issues in S / M / L before starting, then record actual time. Do not
convert to hours. After four sprints you will have a personal velocity number
and, more usefully, a calibration record showing which kinds of work you
routinely underestimate. That calibration is the actual skill.

## When to break the rules

If a full week passes with zero merged PRs because the process ate the week,
the process is wrong and gets cut. Ship first, refine the workflow second.
