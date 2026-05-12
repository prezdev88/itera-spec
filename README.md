# IteraSpec

IteraSpec is a human-approved AI workflow for building new software or changing existing systems through specification, planning, and one-task-at-a-time implementation.

![IteraSpec infographic](info.png)

## Usage

Give your AI assistant one of these instructions:

```text
Sigue estrictamente `ITERASPEC.md` como protocolo principal de este proyecto. Léelo completo antes de actuar y obedécelo literalmente.
```

```text
Follow `ITERASPEC.md` strictly as the main protocol for this project. Read it completely before acting and obey it literally.
```

Then let it start from `Phase 0` and approve each phase and task explicitly.

Phase roles:

- `P0`: `Discovery Lead`
- `P1`: `Product Owner`
- `P2`: `Tech Lead`
- `P3`: `Engineering Manager`
- `P4`: `Lead Senior Developer`
- `P5`: `Release Manager`

Developer staffing:

- In `P3`, the user may choose one or more named developer profiles from `.iteraspec/developers/`.
- If the user does not know or does not want to choose, IteraSpec assigns the default senior generalist profile automatically.
- If multiple developers are selected, IteraSpec designates one lead developer for `P4`.

Developer profile creation:

- IteraSpec can also create new developer profiles through a guided question flow.
- The detailed creation protocol lives in `DEVELOPER_PROFILE_CREATION.md`.

Formal delivery closure:

- `P5` is the formal delivery phase handled by `Release Manager`.
- The final delivery artifact is `.iteraspec/<feature_name>/delivery.md`.

When IteraSpec asks for approval, you can answer with `[A]prueba` or just `a`. If you do not approve, just say what you want changed.

If a receiving phase determines that the previous phase output is not acceptable, it may reject the handoff, return the workflow to the previous phase, and record the reason in `.iteraspec/status.md`.

Before the first backend implementation task, `P4` must ask the human whether backend work should follow TDD or whether unit tests should be deferred until the end of the approved implementation backlog.

Each feature or functionality handled with IteraSpec should keep its own workflow artifacts inside `.iteraspec/<feature_name>/`, for example `.iteraspec/user-authentication/specs.md`, `.iteraspec/user-authentication/backlog.md`, `.iteraspec/user-authentication/board.md`, `.iteraspec/user-authentication/staffing.md`, and `.iteraspec/user-authentication/current_task.md`.

Reusable named developer profiles should live under `.iteraspec/developers/`.

When the feature backlog is complete, IteraSpec should also prepare `.iteraspec/<feature_name>/delivery.md` as the formal delivery summary for final approval.

Each backlog task must be associated with exactly one approved requirement identifier from `specs.md`, using `RFNN` or `RNFNN`.

The GUI expects stable Markdown structures for `status.md`, `backlog.md`, `board.md`, and `current_task.md`. Use the canonical artifact formats documented in [`ITERASPEC.md`](/home/prezdev/git-projects/itera-spec/ITERASPEC.md).

IteraSpec should also maintain a global file at `.iteraspec/status.md`. On a new session, the AI should inspect that file first to understand which feature, phase, and next step are currently active.

## Reuse In Another Project

If you want to reuse IteraSpec in another repository, copy at minimum:

- `AGENTS.md`
- `DEVELOPER_PROFILE_CREATION.md`
- `ITERASPEC.md`
- `developers/`

If you also want the GUI viewer, copy these files into a `gui/` directory at the root of the target project:

- `gui/app.py`
- `gui/run.sh`
- `gui/requirements.txt`

Expected structure in the target project:

```text
your-project/
  AGENTS.md
  DEVELOPER_PROFILE_CREATION.md
  ITERASPEC.md
  .iteraspec/
    developers/
      lucas-rios-senior-generalist.md
      mateo-herrera-java-senior.md
      prezdev-java-senior.md
    status.md
    <feature_name>/
      specs.md
      backlog.md
      board.md
      staffing.md
      current_task.md
      delivery.md
  gui/
    app.py
    run.sh
    requirements.txt
```

The GUI reads `.iteraspec/` from the root of the target project. Run it with:

```bash
cd gui
./run.sh
```
