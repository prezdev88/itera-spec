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

Each feature or functionality handled with IteraSpec should keep its own workflow artifacts inside `.iteraspec/<feature_name>/`, for example `.iteraspec/user-authentication/specs.md`, `.iteraspec/user-authentication/backlog.md`, and `.iteraspec/user-authentication/current_task.md`.

## Reuse In Another Project

If you want to reuse IteraSpec in another repository, copy at minimum:

- `ITERASPEC.md`

If you also want the GUI viewer, copy these files into a `gui/` directory at the root of the target project:

- `gui/app.py`
- `gui/run.sh`
- `gui/requirements.txt`

Expected structure in the target project:

```text
your-project/
  ITERASPEC.md
  .iteraspec/
    <feature_name>/
      specs.md
      backlog.md
      current_task.md
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
