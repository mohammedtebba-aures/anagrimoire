## What and why

<!-- One paragraph. What changed, and what problem it solves. Not a file list;
     the diff already says which files changed. -->

Closes #

## How to verify

<!-- Exact steps a reviewer follows to confirm this works. A test name counts.
     "Run the game and look at it" does not. -->

1.

## Decisions and trade-offs

<!-- Anything you chose between. What you rejected and why. If a choice here is
     expensive to reverse later, it needs an ADR in docs/adr/ instead. -->

## Review brief

<!-- Tell the reviewer where to attack. Be specific. Generic requests get
     generic approvals, which are worthless. -->

Focus on:
- [ ] Correctness of the state transitions
- [ ] Edge cases I probably missed
- [ ] Whether the abstraction is earning its keep
- [ ] Test quality (are these testing behaviour or the implementation?)
- [ ] Other:

## Definition of Done

- [ ] Acceptance criteria in the issue are all met
- [ ] New logic lives in `Core` unless it is genuinely presentation
- [ ] Unit tests cover the happy path and at least two edge cases
- [ ] `Core` still has zero Godot dependencies
- [ ] Any randomness is seed-driven and reproducible
- [ ] `dotnet test` passes locally
- [ ] `dotnet format --verify-no-changes` passes
- [ ] No new compiler warnings
- [ ] Public types and non-obvious methods documented
- [ ] ADR written if a non-reversible choice was made
- [ ] Branch is short-lived and scoped to one issue
