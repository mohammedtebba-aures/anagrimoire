#!/usr/bin/env bash
#
# Seeds labels, milestones and the Sprint 0 / Sprint 1 backlog into a fresh repo.
#
# Prerequisites:
#   gh auth login
#   run from inside the cloned repo
#
# IMPORTANT: run this BEFORE creating any other issue. Issue numbers are
# assigned in order and ci.yml + BACKLOG.md reference #2, #3 etc. by number.
#
# Usage:
#   chmod +x seed-issues.sh
#   ./seed-issues.sh            # create everything
#   ./seed-issues.sh --dry-run  # print what it would do

set -euo pipefail

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

run() {
  if $DRY_RUN; then
    printf '  [dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

# --- preflight -------------------------------------------------------------

command -v gh >/dev/null || { echo "gh not found. Install the GitHub CLI first."; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Not authenticated. Run: gh auth login"; exit 1; }

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Repository: $REPO"

EXISTING=$(gh issue list --state all --limit 1 --json number -q 'length')
if [[ "$EXISTING" != "0" ]]; then
  echo
  echo "WARNING: this repo already has issues. Numbering will not match BACKLOG.md."
  read -rp "Continue anyway? [y/N] " reply
  [[ "$reply" == "y" ]] || exit 1
fi

$DRY_RUN && echo && echo "DRY RUN — nothing will be created" && echo

# --- labels ----------------------------------------------------------------

echo
echo "Creating labels..."

create_label() {
  run gh label create "$1" --color "$2" --description "$3" --force
}

create_label "layer:core"   "1D76DB" "Rules engine. Pure C#, no Godot."
create_label "layer:game"   "5319E7" "Godot scenes, input, rendering."
create_label "layer:infra"  "0E8A16" "CI, build, release, tooling."
create_label "layer:docs"   "CFD3D7" "Documentation and ADRs."
create_label "size:s"       "C2E0C6" "Under 2 hours."
create_label "size:m"       "FEF2C0" "Half a day."
create_label "size:l"       "F9D0C4" "A day or more. Consider splitting."
create_label "blocking"     "B60205" "Nothing else proceeds until this is resolved."
create_label "risk:high"    "D93F0B" "Could invalidate an architectural decision."

# --- milestones ------------------------------------------------------------

echo
echo "Creating milestones..."

create_milestone() {
  if $DRY_RUN; then
    printf '  [dry-run] milestone: %s\n' "$1"
    return
  fi
  gh api "repos/$REPO/milestones" \
    -f title="$1" \
    -f description="$2" \
    --silent 2>/dev/null || echo "  (milestone '$1' already exists, skipping)"
}

create_milestone "Sprint 0" "De-risk and scaffold. Prove the ground is solid before writing game code."
create_milestone "Sprint 1" "The rules engine. A full run playable as text, zero Godot."

# --- issues ----------------------------------------------------------------

echo
echo "Creating issues..."

new_issue() {
  local title="$1" labels="$2" milestone="$3" body="$4"
  if $DRY_RUN; then
    printf '  [dry-run] #%s  %s\n' "?" "$title"
    return
  fi
  gh issue create \
    --title "$title" \
    --label "$labels" \
    --milestone "$milestone" \
    --body "$body"
}

# ---------- Sprint 0 ----------

new_issue "Repository and solution skeleton" "layer:infra,size:m" "Sprint 0" \
'## Outcome

A green CI pipeline on an empty but correctly structured repository.

## Acceptance criteria

- [ ] `src/WordRoguelike.Core` class library created
- [ ] `tests/WordRoguelike.Core.Tests` xUnit project created
- [ ] `WordRoguelike.Core.sln` contains only those two projects
- [ ] `Directory.Build.props` sets `TreatWarningsAsErrors`, `Nullable=enable`, `LangVersion=latest`
- [ ] One trivial passing test proves the harness works
- [ ] `.gitignore` covers .NET and Godot (`.godot/`, `bin/`, `obj/`, `*.user`)
- [ ] CONTRIBUTING.md, PR template, issue template, ADR 0001 committed
- [ ] `.github/workflows/ci.yml` added and green on the first PR
- [ ] Branch protection on `main`: no direct pushes, CI required

## Notes

The two-solution split is deliberate. CI builds the Core solution only, so it
needs nothing but the .NET SDK.'

new_issue "Prove C# Android export end to end" "layer:infra,size:m,blocking,risk:high" "Sprint 0" \
'## Outcome

A signed build of a minimal C# Godot project runs on a physical Android device.

**Nothing else proceeds until this works.** Do it before writing any game code.

## Acceptance criteria

- [ ] Godot .NET build installed, exact version recorded in ADR 0002
- [ ] Minimal Godot project at `src/WordRoguelike.Game` with one button and one label
- [ ] Game project references `WordRoguelike.Core` and calls one method from it
- [ ] Debug APK sideloaded and running on a physical phone
- [ ] Release keystore generated and backed up OFF this machine
- [ ] Signed AAB produced
- [ ] AAB verified locally via `bundletool build-apks --local-testing`
- [ ] Any workarounds needed are written into ADR 0002

## Notes

C# Android export in Godot 4 is still flagged experimental. Android uses the
linux-bionic Mono runtime, supports arm64 and x64 only, and lacks Android
bindings, so some platform APIs are unavailable. Godot 4.5+ additionally needs
the .NET 9 SDK at build time.

Debug APK and release AAB fail differently. Trimming in release builds can
break reflection-based code that works fine in debug.

## If this fails

Stop and reopen ADR 0001. Fallback is GDScript for the Godot layer with Core
kept as-is, or reconsidering the engine.'

new_issue "Choose and license a word list" "layer:core,size:s" "Sprint 0" \
'## Outcome

A word list is committed, and its licence provably permits commercial use.

## Acceptance criteria

- [ ] Candidates compared (ENABLE, dwyl/english-words, others)
- [ ] Licence verified as compatible with a paid Play Store release
- [ ] Decision, source URL and licence recorded in ADR 0003
- [ ] File committed or vendored with attribution as the licence requires
- [ ] Word count and file size recorded in this issue

## Notes

The licence check IS the work here, not the download. Collins and TWL lists are
proprietary and owned; shipping one commercially without a licence is a real
legal problem. ENABLE is public domain.'

new_issue "Google Play developer account" "layer:infra,size:s" "Sprint 0" \
'## Outcome

A verified developer account with a draft listing and an internal testing track.

## Acceptance criteria

- [ ] Dedicated Google account created, not personal, not employer-owned
- [ ] 2FA enabled, recovery codes saved offline with the keystore backup
- [ ] Registration fee paid
- [ ] Identity verification submitted
- [ ] Draft app listing created
- [ ] Internal testing track configured
- [ ] Confirmed whether Algeria supports Play merchant registration for selling

## Notes

Identity verification can take days. Start it now and let it run in the
background. Developer registration and merchant/selling eligibility are
different things; check both.'

# ---------- Sprint 1 ----------

new_issue "Letter tiles and the bag" "layer:core,size:m" "Sprint 1" \
'## Outcome

A bag holds a defined multiset of letter tiles, constructed deterministically.

## Acceptance criteria

- [ ] `LetterTile` record: letter, point value, modifier flags
- [ ] `Bag` holds a multiset of tiles
- [ ] Starting composition defined in data, not hardcoded in logic
- [ ] Bag construction is pure and takes no RNG
- [ ] Tests: composition totals, add, remove, duplicate handling'

new_issue "Deterministic draw, discard and reshuffle" "layer:core,size:m" "Sprint 1" \
'## Outcome

Drawing is fully reproducible from a seed.

Determinism is not optional. It makes every later test possible and it is what
a daily-challenge mode would be built on.

## Acceptance criteria

- [ ] RNG injected as a seeded source. Never `new Random()` inside Core
- [ ] Draw to a hand of N
- [ ] Played tiles move to discard
- [ ] Draw pile emptying mid-draw reshuffles the discard and continues
- [ ] Tests: identical seed produces an identical sequence across runs
- [ ] Tests: reshuffle mid-draw, drawing more than the bag holds, empty bag'

new_issue "Word validation" "layer:core,size:m" "Sprint 1" \
'## Outcome

A word is accepted only if it is real and buildable from the current hand.

## Acceptance criteria

- [ ] `IWordSource` interface so Core does not know about files
- [ ] In-memory `HashSet<string>` implementation
- [ ] Validity requires both dictionary membership AND buildability from hand
- [ ] Case and whitespace normalised on load and lookup
- [ ] Load time and memory measured on a real phone, recorded in this issue
- [ ] Tests: valid word, word absent from list, letters not in hand, reusing a
      single tile twice, empty string'

new_issue "Scoring" "layer:core,size:m" "Sprint 1" \
'## Outcome

A valid word produces a score from letter values, length and modifiers.

## Acceptance criteria

- [ ] Base score from letter values
- [ ] Length multiplier curve defined in data
- [ ] Per-tile modifiers apply in a defined, documented order
- [ ] Tests: each multiplier tier, modifier stacking order, minimum-length word'

new_issue "Encounter resolution" "layer:core,size:m" "Sprint 1" \
'## Outcome

An encounter can be won or lost by submitting words against a target.

## Acceptance criteria

- [ ] `Encounter` with a target score and a turn limit
- [ ] Submitting a word advances the encounter and returns a result
- [ ] Win and loss conditions implemented
- [ ] Tests: win on the final turn, loss by running out of turns, exact-target edge'

new_issue "Rewards that modify the bag" "layer:core,size:m" "Sprint 1" \
'## Outcome

Finishing an encounter offers a choice that permanently changes the bag.

This is the roguelike loop. Without it the game is just a word game.

## Acceptance criteria

- [ ] Reward types: add a tile, upgrade a tile, remove a tile
- [ ] Three rewards offered after each encounter, drawn from the seeded RNG
- [ ] Applying a reward returns a new bag; mutation is explicit
- [ ] Tests: each reward type, offers deterministic per seed, removing the last
      copy of a letter'

new_issue "Run state machine" "layer:core,size:l" "Sprint 1" \
'## Outcome

A complete run is playable start to finish through a console harness.

No Godot, no UI, no art. If this is not fun as text output, art will not save it.

## Acceptance criteria

- [ ] `RunState` sequences encounters, rewards and run end
- [ ] Full run playable through a console harness
- [ ] A seed plus a list of played words fully reproduces a run
- [ ] Tests: complete winning run, run lost at encounter 2, reproducibility

## Notes

Sized L. Split it if it does not fit in a day.'

new_issue "Sprint 1 retro and CHANGELOG" "layer:docs,size:s" "Sprint 1" \
'## Outcome

The sprint is closed out with a calibration record and a changelog.

## Acceptance criteria

- [ ] Actual time recorded on every closed issue, compared against the estimate
- [ ] `CHANGELOG.md` started, Keep a Changelog format
- [ ] Retro notes in `docs/retros/sprint-01.md`: what worked, what did not, one
      thing changing next sprint

## Notes

The estimate-versus-actual comparison is the point. After a few sprints it
shows which kinds of work you routinely underestimate.'

echo
echo "Done."
echo
echo "Next:"
echo "  1. gh issue list --milestone \"Sprint 0\""
echo "  2. Create a Project board in the web UI and link this repo"
echo "  3. Start with #2. Nothing else matters until the export works."
