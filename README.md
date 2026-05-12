# IteraSpec

Install it first:

```bash
./install.sh /path/to/target-project
```

If the target path does not exist, `install.sh` creates it and installs IteraSpec there.

Minimum installation:

- `ITERASPEC.md`
- `AGENTS.md`

If you want the full repository tooling, also keep:

- `DEVELOPER_PROFILE_CREATION.md`
- `gui/`
- reusable developer profiles under `.iteraspec/developers/` or `developers/`

## Quick Start

After installation, give your assistant one of these instructions:

```text
Sigue estrictamente `ITERASPEC.md` como protocolo principal de este proyecto. Léelo completo antes de actuar y obedécelo literalmente.
```

```text
Follow `ITERASPEC.md` strictly as the main protocol for this project. Read it completely before acting and obey it literally.
```

Then:

1. The assistant starts at `P0`.
2. Every phase and every task closure requires human approval.
3. You can approve with `A`, `a`, or any explicit approval message.

## What It Is

IteraSpec is a protocol for building software with AI while keeping human approval at every phase and executing one implementation task at a time.

## What It Includes

- `ITERASPEC.md`: the full protocol and canonical rules.
- `AGENTS.md`: local instructions for agents working in this repository.
- `DEVELOPER_PROFILE_CREATION.md`: the flow for creating reusable developer profiles.
- `gui/`: the IteraSpec artifact viewer.

## Phases

- `P0` - `Discovery`: `Discovery Lead`
- `P1` - `Specification`: `Product Owner`
- `P2` - `Planning`: `Tech Lead`
- `P3` - `Staffing`: `Engineering Manager`
- `P4` - `Implementation`: `Lead Senior Developer`
- `P5` - `Delivery`: `Release Manager`

## Workspace Structure

Each feature uses its own workspace inside `.iteraspec/`:

```text
.iteraspec/
  status.md
  developers/
  <feature_name>/
    specs.md
    backlog.md
    board.md
    staffing.md
    current_task.md
    delivery.md
```

Key rules:

- `status.md` is the global resume point.
- Every backlog task must map to exactly one `RFNN` or `RNFNN`.
- In `P3`, IteraSpec auto-assigns developer profiles if the user does not choose them.
- If no developer profiles exist, IteraSpec must assign a default generalist developer.
- Before the first backend task in `P4`, the testing strategy must be defined: `TDD` or deferred unit tests.

## Reuse In Another Repository

Minimum setup:

- `ITERASPEC.md`
- `AGENTS.md`

Optional files:

- `DEVELOPER_PROFILE_CREATION.md`
- `.iteraspec/developers/` or `developers/`, depending on how you organize profiles in the target repo

If you also want the viewer, copy the full `gui/` directory.

## References

- [ITERASPEC.md](/home/prezdev/git-projects/itera-spec/ITERASPEC.md)
- [AGENTS.md](/home/prezdev/git-projects/itera-spec/AGENTS.md)
- [DEVELOPER_PROFILE_CREATION.md](/home/prezdev/git-projects/itera-spec/DEVELOPER_PROFILE_CREATION.md)
