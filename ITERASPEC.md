<!-- Sigue estrictamente `ITERASPEC.md` como protocolo principal de este proyecto. Léelo completo antes de actuar y obedécelo literalmente. -->
# IteraSpec Development Protocol: AI-Driven Universal Software Blueprint 🤖

## 💡 Objective
This protocol defines a repeatable, structured workflow for an Artificial Intelligence assistant to take raw project concepts or requested changes and autonomously develop production-ready software systems through iterative steps. It serves as a universal blueprint for both new software projects and existing systems, requiring minimal project-specific setup.

## Human Approval Rule
Every phase in this protocol is considered complete only when a human explicitly approves its output. The AI may prepare, refine, and propose deliverables autonomously, but it must not consider a phase closed without human validation.
This also applies to task completion: passing tests or reaching an apparently complete implementation is not sufficient to mark a task as finished without explicit human confirmation.

## Approval Input Rule
When IteraSpec requests a human approval decision, the human may answer with full words or with a short single-letter response.

- `A` or `a` means `[A]prueba`.
- If the human does not approve, they should state what they want changed instead of using a disapproval letter.
- The AI must interpret `A` or `a` as a valid approval decision for phases, backlog approval, task closure, and any other explicit approval gate in the protocol.
- If the user writes a longer response that clearly expresses approval, the AI must interpret it as approval. If the user writes requested changes, corrections, objections, or asks for modifications, the AI must interpret that as non-approval and continue with the requested adjustments.

## Implementation Boundary Rule
The AI must not write, modify, or generate production code in any phase other than the implementation phase inside the iterative development loop. Phases dedicated to discovery, specification, planning, or final review must remain focused on analysis, documentation, planning, and validation only.
This prohibition includes project scaffolding, repository bootstrapping, framework initialization, dependency setup, configuration files for executable software, build files such as `pom.xml`, `package.json`, `build.gradle`, Docker-related runtime files, source files, test files, and any other implementation artifact.

## Protocol Isolation Rule
IteraSpec is a development protocol and must remain isolated from the product, feature, or application being built.

- The AI must not expose, mention, render, or embed IteraSpec concepts inside the developed product unless the human explicitly requests that behavior.
- This includes references to IteraSpec itself, protocol phases, backlog states, task identifiers, refinement identifiers, approval mechanics, `.iteraspec/`, `status.md`, or any other workflow artifact.
- User-facing screens, labels, placeholder text, demos, seeded content, examples, logs intended for end users, and generated documentation for the product must describe the product domain itself, not the internal IteraSpec workflow.
- Internal IteraSpec artifacts may mention IteraSpec freely, but production-facing output must remain cleanly separated from the protocol.

## GUI Visual Independence Rule
When the AI designs or implements a GUI for the product being developed, it must not use the IteraSpec GUI as the visual, structural, or stylistic base unless the human explicitly requests that reuse.

- The AI must not copy or closely derive the layout, component hierarchy, color palette, typography, spacing system, panel styling, or overall composition from the root `gui/` directory reserved for IteraSpec.
- The AI must design the product GUI according to the product's own domain, tone, and user needs, even if a `gui/` directory already exists in the repository for IteraSpec itself.
- Similarity caused only by generic web conventions is acceptable, but the product GUI must not feel like a re-skinned IteraSpec viewer.

## Single-Task Execution Rule
The AI must implement only one task at a time. It must not code multiple backlog items in parallel, and it must not begin a new implementation task until the current task has been moved to `🟢 Done` or `⚫ Blocked` and a human has approved that outcome.

## Automatic Task Advance Rule
Once a human explicitly confirms that the current `🟡 In Progress` task is closed as `🟢 Done`, the AI must automatically select the next highest-priority task from `🔴 To Do`, move it to `🟡 In Progress`, update `.iteraspec/<feature_name>/current_task.md`, and begin the next implementation cycle without waiting for a separate approval to start that next task.
The AI must not auto-start the next task only if the human explicitly says they do not want to continue yet, do not want to start the next task, or want to pause after the current closure.
This automatic advance applies only inside Phase 3 after implementation has already been authorized. It does not override the requirement for explicit human approval to enter Phase 3 for the first time.

## Feature Workspace Rule
Each full IteraSpec cycle for a new feature, functionality, or change request must use its own dedicated workspace inside `.iteraspec/`, using the structure `.iteraspec/<feature_name>/`.
The `<feature_name>` should be a short, human-readable, filesystem-safe identifier that clearly represents the feature or functionality being developed.

Example:

```text
.iteraspec/
  user-authentication/
    specs.md
    backlog.md
    board.md
    current_task.md
  billing-export/
    specs.md
    backlog.md
    board.md
    current_task.md
```

## GUI Protection Rule
If a `gui/` directory exists at the root of the project, the AI must treat it as the IteraSpec GUI and must not modify, move, rename, delete, or repurpose it as part of the feature or application being developed.
This directory is reserved for the IteraSpec interface and is outside the normal implementation scope of the target project unless the human explicitly requests changes to that `gui/` directory.

## Global Status Rule
IteraSpec must maintain a global status file at `.iteraspec/status.md` to make the workflow resumable across sessions and across multiple features.

- **Resume First Rule:** At the beginning of a new session, if `.iteraspec/status.md` exists, the AI must inspect it before deciding which phase, feature, or task to continue.
- **Purpose Rule:** This file is the primary global checkpoint for understanding the current IteraSpec progress in the repository.
- **Multi-Feature Rule:** The file must identify the active feature and summarize the state of any other feature workspaces that are in progress, paused, blocked, or awaiting approval.
- **Update Rule:** The AI must update `.iteraspec/status.md` whenever a phase starts, a phase is approved, a task starts, a task is approved as done, a task becomes blocked, the workflow is paused, or the active feature changes.
- **Consistency Rule:** The information in `.iteraspec/status.md` must remain consistent with `.iteraspec/<feature_name>/specs.md`, `.iteraspec/<feature_name>/backlog.md`, `.iteraspec/<feature_name>/board.md`, and `.iteraspec/<feature_name>/current_task.md`.
- **Minimum Contents Rule:** The file must include at least the active feature, current phase, phase state, last approved phase, active task if any, active refinement if any, and the next expected action.

## Phase Persistence Rule
IteraSpec must persist the required workflow artifacts on disk before claiming that a phase has started, is in progress, or has completed.

- **No Invisible Progress Rule:** The AI must not claim to be in `P1`, `P2`, `P3`, or `P4` if the required files for that phase have not been created or updated on disk.
- **P0 Persistence Rule:** During `P0`, the AI must record the current context and expected next step in `.iteraspec/status.md` before claiming that initialization is in progress or complete.
- **P1 Persistence Rule:** The AI must not claim to have entered or completed `P1` unless `.iteraspec/<feature_name>/specs.md` exists and `.iteraspec/status.md` reflects that `P1` is active or approved.
- **P2 Persistence Rule:** The AI must not claim to have entered or completed `P2` unless `.iteraspec/<feature_name>/backlog.md` and `.iteraspec/<feature_name>/board.md` exist and `.iteraspec/status.md` reflects that `P2` is active or approved.
- **P3 Persistence Rule:** The AI must not claim to have entered or continued `P3` unless `.iteraspec/<feature_name>/current_task.md` exists for the active task and `.iteraspec/status.md` reflects that `P3` is active.
- **Approval Before Advance Rule:** Before requesting approval to advance from one phase to the next, the AI must first persist the corresponding artifacts and status updates for the current phase.

## Markdown Location Rule
Any Markdown file created by IteraSpec as part of the workflow must be stored inside the feature workspace for that cycle, inside `.iteraspec/<feature_name>/`. This includes specification files, backlog files, review notes, status reports, and any other Markdown artifacts generated by the protocol.

## Identifier Convention Rule
IteraSpec must use a fixed minimal identifier convention for phases, tasks, and refinements in every feature workspace.

- **Phases:** The protocol phases must be referenced as `P0`, `P1`, `P2`, `P3`, and `P4`.
- **Tasks:** Backlog tasks must use the format `TNN`, starting at `T01` and increasing sequentially (`T02`, `T03`, etc.). Task identifiers must always use two digits to preserve visual ordering and consistency.
- **Refinements:** Refinements must use the format `RNN`, starting at `R01` and increasing sequentially (`R02`, `R03`, etc.). Refinement identifiers must always use two digits.
- **Task-to-Refinement Rule:** Every task `TNN` must be associated with exactly one refinement `RNN`.
- **Refinement Grouping Rule:** A refinement `RNN` may group one or more tasks `TNN`.
- **Per-Feature Scope:** Task and refinement numbering is sequential within each `.iteraspec/<feature_name>/` workspace.
- **Uniqueness Rule:** Task and refinement identifiers must not be reused, even if an item is removed, blocked, or replaced later.
- **Active Context Rule:** During implementation, `.iteraspec/<feature_name>/current_task.md` must include the active task identifier. If the current work is a refinement, the file must also include the active refinement identifier.

## Active Task File Rule
During implementation, the AI must maintain a dedicated file at `.iteraspec/<feature_name>/current_task.md` containing the single backlog task currently being worked on for that feature. This file exists to avoid repeated full backlog reads and to make the active implementation scope explicit at all times.

## Backlog Separation Rule
IteraSpec must separate task definitions from task state tracking during planning and implementation.

- **Backlog Catalog Rule:** `.iteraspec/<feature_name>/backlog.md` must contain the full catalog of task definitions. Each task must keep its identifier, title, and implementation-relevant detail in a stable place that is not deleted when the task changes status.
- **Refinement Association Rule:** Each task definition in `backlog.md` must explicitly declare its associated refinement identifier so the relationship between tasks and refinements remains traceable.
- **Board Rule:** `.iteraspec/<feature_name>/board.md` must contain the operational state board only.
- **Board Content Rule:** `board.md` must track `🔴 To Do`, `🟡 In Progress`, `🟢 Done`, and `⚫ Blocked` using task identifiers only, plus a short blocker note when a task is blocked.
- **Board Scope Rule:** Refinements are grouping identifiers and must not replace tasks as the primary items tracked in `board.md`.
- **No Detail Loss Rule:** Moving a task between states must update `board.md` and must not remove or replace the task detail already stored in `backlog.md`.
- **Current Task Source Rule:** `current_task.md` may be copied or summarized from `backlog.md`, but the canonical long-lived task definition remains in `backlog.md`.

## Token Efficiency Rule
IteraSpec must minimize token usage across all phases without reducing correctness, traceability, or required human approvals.

- **Context Minimization Rule:** The AI must not repeatedly restate full approved specifications, full backlogs, or previously accepted analysis unless a human explicitly asks for a full restatement or a major change requires rebuilding that context.
- **Reference Instead of Repeat Rule:** After a document has been created and approved, the AI should reference it by file path, identifier, section, task code, or short summary instead of reproducing its contents.
- **Current Task First Rule:** During Phase 3, the AI must use `.iteraspec/<feature_name>/current_task.md` as the primary working context and must avoid rereading or reprinting the entire backlog unless reprioritization, re-planning, or blocker analysis requires it.
- **Board First Rule:** When the AI only needs to know task order or state, it should read `board.md` before reading the full task catalog in `backlog.md`.
- **Delta Reporting Rule:** Status updates, readiness reports, and refinement notes should describe only what changed since the previous approved or reported state, plus any information needed for validation or decision-making.
- **Concise Status Rule:** Routine progress updates should remain brief and focused. The AI should avoid long narrative recaps when a short operational summary is enough.
- **Refinement Compression Rule:** Refinements should record only the adjustment made, the reason for it, and the impact on acceptance or validation. The AI must not rewrite the full task description unless the task scope itself changed.
- **Phase Memory Rule:** Once a phase has been approved, the AI must treat that phase as closed reference context and must not reconstruct it in full unless the user requests a recap or a scope change reopens it.

## Change Request Rule
If the user requests a new feature, scope change, behavioral change, or any other requirement modification in any phase, the AI must not implement it immediately unless it is already reflected in the currently approved task. The AI must first evaluate the impact of the request and update the corresponding workflow artifacts before continuing.

- If the change affects requirements or architecture, the AI must update `.iteraspec/<feature_name>/specs.md` and request human approval again.
- If the change affects planning or task ordering, the AI must update the backlog and/or board and request human approval again.
- If the change affects the currently active implementation task, the AI must update `.iteraspec/<feature_name>/current_task.md` only after the human explicitly approves the scope change.
- If the change is substantial, the AI may return to an earlier phase before continuing.
- No new feature may be implemented until the change has been incorporated into the appropriate approved workflow artifact.

## Phase 0: Initialization & Context Setting
*   **Action:** The AI must first prompt the user with mandatory questions to define the scope, goals, and constraints of the system or change request (The "What" and "Why").
    *   *First Mandatory Question:* Ask the user which language they want to use for the entire workflow and development process.
    *   *Language Rule:* The language selected by the user in this phase must be used consistently throughout the entire protocol, including questions, specifications, backlog items, status updates, documentation, and any other workflow artifacts unless the user explicitly approves a change.
    *   *Project State Question:* Ask whether the work applies to a new project or an existing codebase/system.
    *   *Mandatory Questions:* Workflow language, project state (new or existing), primary objective, target users, core problem solved, expected output/deliverables.
*   **Persistence Rule:** The AI must update `.iteraspec/status.md` during this phase so the current context, active feature if known, current phase, and next expected action are persisted even before `specs.md` exists.
*   **Output Check:** Phase 0 is complete only after a human confirms that the initial context is correct and sufficient to continue to Phase 1.

## Phase 1: Requirement Formalization & Specification Generation
*   **Input:** Raw conversational data from Phase 0.
*   **AI Action:** Create the feature workspace if it does not already exist, then generate and finalize a comprehensive **Specification Document (`.iteraspec/<feature_name>/specs.md`)**. This document must be highly detailed, covering functional requirements (what the system must do), non-functional requirements (performance, security, usability), and initial architectural decisions.
*   **Existing System Rule:** If the work targets an existing project, the AI must analyze the current system before finalizing the specification. This analysis must identify the current architecture, relevant modules, dependencies, integration points, constraints, and likely regression risks. The resulting specification must clearly distinguish existing behavior from the requested changes.
*   **Technology Decision Rule:** During this phase, the AI must ask the user whether they want a specific technology stack, framework, language, or platform. If the user does not know, does not care, or does not want to answer, the AI must choose the most appropriate stack based on the project requirements and document that decision in `.iteraspec/<feature_name>/specs.md` with a brief justification.
*   **Specification Size Rule:** The specification must be detailed enough to support implementation and approval, but it must avoid unnecessary narrative repetition, long prose restatements, and exhaustive discussion of discarded alternatives that do not affect implementation.
*   **Persistence Rule:** Before asking for approval in this phase, the AI must ensure that `.iteraspec/<feature_name>/specs.md` exists and that `.iteraspec/status.md` marks `P1` as the current phase with the correct next action.
*   **Restriction:** No code may be written in this phase.
*   **Approval Gate:** The phase ends only when a human explicitly approves `.iteraspec/<feature_name>/specs.md`.
*   **Goal:** Transform ambiguous ideas into concrete, verifiable technical documentation.

## Phase 2: Backlog Decomposition & Task Planning
*   **Input:** The finalized `.iteraspec/<feature_name>/specs.md` from Phase 1.
*   **AI Action:** Generate a structured task catalog and state board inside the same feature workspace: `.iteraspec/<feature_name>/backlog.md` for full task definitions and `.iteraspec/<feature_name>/board.md` for operational task state. This process breaks down the system into atomic, self-contained User Stories or Tasks (e.g., "Implement user authentication endpoint").
*   **Restriction:** No code may be written in this phase.
*   **Restriction:** No implementation artifact may be created in this phase. The AI must not scaffold the project, initialize a framework, create build files, create dependency manifests, create source code, create tests, or start executing any backlog task.
*   **Sizing Rule:** The backlog must not target any fixed number of tasks. The number of tasks must emerge from the real scope and complexity of the approved feature.
*   **Sizing Rule:** The AI must not default to round-number backlogs such as 5, 10, or 15 items unless the feature genuinely requires that exact count.
*   **Sizing Rule:** The backlog must contain the minimum number of tasks needed to deliver the approved feature safely and incrementally. Small features may produce very short backlogs; larger features may produce longer ones.
*   **Granularity Rule:** Each task must be atomic enough to be implemented and validated independently, but large enough to represent meaningful progress.
*   **Granularity Rule:** The AI must avoid artificial task splitting done only to inflate the backlog, and it must avoid merging unrelated work into oversized tasks just to reduce the count.
*   **Lean Backlog Rule:** The AI should prefer the smallest backlog that still preserves safe incremental delivery, meaningful validation boundaries, and clear human review points.
*   **Justification Rule:** For each backlog item, the AI should be able to justify why that task exists as a separate unit of work and why it is not better merged with an adjacent item or split further.
*   **Persistence Rule:** Before asking for approval in this phase, the AI must ensure that `.iteraspec/<feature_name>/backlog.md` and `.iteraspec/<feature_name>/board.md` exist and that `.iteraspec/status.md` marks `P2` as the current phase with the correct next action.
*   **Structure Rule:** `backlog.md` must contain task definitions, while `board.md` must contain the prioritized state board:
    *   `🔴 To Do`: High priority task identifiers ready for implementation.
    *   `🟡 In Progress`: The single task identifier currently being implemented. Only one task may exist in this state at any time.
    *   `🟢 Done`: Task identifiers completed through relevant testing or explicit user approval.
    *   `⚫ Blocked`: Task identifiers that cannot continue due to a failure, dependency, missing decision, environment issue, or external constraint. Each blocked task entry must include a short description of the blocker.
*   **Approval Gate:** The backlog catalog and board are considered finalized only after human approval.
*   **Goal:** Create a clear roadmap that guides development incrementally, ensuring traceability and manageability.

## Phase 3: Iterative Development Loop (The Core Cycle)
This phase repeats until the backlog is empty or marked complete by the user.
1.  **Select Task:** Move one task from `🔴 To Do` to `🟡 In Progress`.
    The AI must wait for explicit human approval before starting implementation of the first selected task in Phase 3. After that, each human-approved closure of a `🟢 Done` task authorizes the AI to automatically select and start the next task according to the Automatic Task Advance Rule.
2.  **Create Active Task Context:** Before writing any implementation artifact, the AI must copy or summarize the selected backlog task from `.iteraspec/<feature_name>/backlog.md` into `.iteraspec/<feature_name>/current_task.md`. This file must contain the current task identifier, description, acceptance criteria if available, and any relevant implementation notes.
3.  **Design/Code:** Develop the necessary code components, following established conventions and best practices (e.g., clean architecture). The AI must not implement anything that is outside the scope described in `.iteraspec/<feature_name>/current_task.md`.
4.  **Test:** Write the tests that are relevant for the feature being implemented (unit, integration, end-to-end, linting, typechecking, or other applicable validations). Execute all available and relevant verification commands (`npm run lint`, `pytest`, etc.).
5.  **Refactor & Review:** Review the code against the original specifications and improve structure/readability.
6.  **Report Readiness:** If the task satisfies the relevant tests or appears implementation-complete, the AI must report that the current task appears ready.
    The readiness report must be concise and should summarize only the implemented delta, relevant validations executed, outstanding risks if any, and the manual validation steps.
7.  **Provide Manual Validation Steps:** Before asking for approval, the AI must explain how the human can manually test or validate the task, including the expected successful result.
8.  **Resolve Status:** The task may move from `🟡 In Progress` to `🟢 Done` only after explicit human confirmation. Without that confirmation, the task must remain in `🟡 In Progress` even if all relevant tests pass. Once the human confirms the closure as `🟢 Done`, the AI must automatically continue with the next eligible `🔴 To Do` task if one exists, unless the human explicitly instructs the AI not to start the next task yet.
9.  **Retry Rule:** If implementation or validation fails, the AI may retry the task up to 3 times. After the third failed attempt, the task must be moved to `⚫ Blocked`.
10.  **Handle Failure or Blockers:** If the task cannot continue, fails validation 3 times, or reaches another blocking condition, move it from `🟡 In Progress` to `⚫ Blocked` and record a short description of the blocker and why the task could not be completed.
11.  **Approval Gate:** Each completed iteration is considered closed only when a human approves the task outcome or accepts its blocked state. Approval of a `🟢 Done` outcome also authorizes the automatic start of the next task within Phase 3 unless the human explicitly pauses the workflow.

## Transition Rule Between Phase 2 and Phase 3
Approval of `.iteraspec/<feature_name>/specs.md` or approval of the Phase 2 planning artifacts does not authorize implementation by itself. After Phase 2 is approved, the AI must remain in planning mode until a human explicitly authorizes Phase 3 or explicitly approves the start of the first backlog task. After that first approval, Phase 3 may continue task by task under the Automatic Task Advance Rule.

## Phase 4: Finalization & Deployment Readiness
*   **Action:** Once all tasks are complete (`🔴 To Do` is empty), the AI performs a final review of the entire codebase.
*   **Restriction:** No new feature code may be written in this phase. Only documentation, validation, and final readiness checks are allowed unless a human explicitly sends the work back to implementation.
*   **Output:** Update documentation (e.g., README, deployment guide) and provide a summary of how the system runs locally and how it can be deployed in production.
*   **Approval Gate:** The protocol is complete only when a human approves the final system state and documentation.
*   **Goal:** Deliver a fully documented, tested, and deployable software product.
