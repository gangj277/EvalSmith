#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


WORKFLOW_TYPES = {
    "single-prompt",
    "structured-output",
    "rag",
    "tool-calling",
    "multi-stage",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ValueError("feature name produced an empty slug")
    return slug


def build_paths(target_dir: Path, slug: str) -> dict[str, Path]:
    return {
        "workflow": target_dir / "evals" / "workflows" / f"{slug}.md",
        "spec": target_dir / "evals" / "specs" / f"{slug}.yaml",
        "cases": target_dir / "evals" / "cases" / slug / "cases.jsonl",
        "rubric": target_dir / "evals" / "rubrics" / f"{slug}.md",
        "components": target_dir / "evals" / "components" / f"{slug}.yaml",
        "ablation": target_dir / "evals" / "experiments" / slug / "ablation-plan.yaml",
        "forensic": target_dir / "evals" / "forensics" / f"{slug}.md",
        "traces_keep": target_dir / "evals" / "traces" / slug / ".gitkeep",
        "reports_keep": target_dir / "evals" / "reports" / ".gitkeep",
        "runs_keep": target_dir / "evals" / "runs" / ".gitkeep",
    }


def workflow_template(feature_name: str, slug: str, workflow_type: str) -> str:
    return f"""# {feature_name} Workflow Analysis

## Scope

- Feature: {feature_name}
- Slug: {slug}
- Workflow type: {workflow_type}

## Probable User Intent

- TODO: Describe the real user task this feature is supposed to complete.

## Entrypoints And Key Files

- TODO: List routes, services, prompts, adapters, tests, and schemas.

## Stage Map

1. Input collection
   - TODO
2. Context assembly or retrieval
   - TODO
3. Model invocation
   - TODO
4. Post-processing or tool use
   - TODO
5. Final output contract
   - TODO

## Evaluation Surfaces

- TODO: List stage-level and final-output evaluation points.

## Component Inventory Summary

- TODO: Enumerate atomic system-prompt clauses, user-input fields, retrieved context classes, examples, tool descriptions, and parser constraints.

## Trace Capture Plan

- TODO: Store the exact assembled system prompt, user message, retrieved context, tool inputs and outputs, intermediate model outputs, and final parser results for every benchmark case.

## Causal Hypotheses To Test

- TODO: Record which components may be causing which failure clusters.

## Open Assumptions

- TODO: Record uncertainty explicitly.
"""


def spec_template(feature_name: str, slug: str, workflow_type: str) -> str:
    return f"""feature_name: {feature_name}
slug: {slug}
workflow_type: {workflow_type}
entrypoint: TODO
success_criteria:
  - name: task_success
    description: TODO
dataset_sources:
  - fixtures
  - docs
  - logs
criteria:
  - name: schema_valid
    grader: code
    stage: output
    pass_threshold: 1
  - name: answer_quality
    grader: llm_rubric
    stage: generation
    pass_threshold: 4
    scale: [1, 5]
failure_modes:
  - instruction_following
  - hallucination
  - retrieval_miss
  - schema_breakage
component_inventory_file: evals/components/{slug}.yaml
experiments_file: evals/experiments/{slug}/ablation-plan.yaml
forensics_file: evals/forensics/{slug}.md
trace_capture:
  level: full
  store:
    - assembled_system_prompt
    - user_message
    - few_shot_examples
    - retrieved_context
    - tool_schemas
    - tool_calls
    - tool_outputs
    - intermediate_model_outputs
    - parser_result
forensic_analysis:
  required: true
  methods:
    - per_case_trace_read
    - component_inventory
    - component_ablation
    - counterfactual_context_swap
    - pairwise_diff
    - failure_clustering
  evidence_thresholds:
    min_supporting_cases: 3
    require_same_slice_rerun: true
    require_counterexample_check: true
run_settings:
  sample_count: 1
  tags:
    - happy-path
    - edge-case
    - adversarial
"""


def cases_template() -> str:
    record = {
        "id": "case_001",
        "tags": ["happy-path"],
        "input": {
            "user_query": "TODO: add a real user input from fixtures, logs, or product specs"
        },
        "expectations": {
            "must_include": [],
            "must_not_include": [],
        },
        "scoring": {
            "primary": ["schema_valid", "answer_quality"],
        },
        "notes": "Replace this synthetic starter with a repository-grounded case.",
    }
    return json.dumps(record, ensure_ascii=True) + "\n"


def rubric_template(feature_name: str) -> str:
    return f"""# {feature_name} Rubric

## Criteria

### schema_valid

- Pass if the output conforms to the expected parser or schema contract.
- Fail immediately on malformed JSON, missing required keys, or invalid enum values.

### answer_quality

Use a 1-5 rubric:

- 5: Fully satisfies the task, grounded, precise, and appropriately scoped
- 4: Correct with minor omissions or phrasing issues
- 3: Partially useful but misses an important requirement
- 2: Major factual or instruction-following problems
- 1: Fails the task or is unsafe to use

## Automatic Fail Conditions

- Unsupported claims presented as certain facts
- Missing mandatory fields required by the feature contract
- Tool output copied blindly without final synthesis when synthesis is required

## Calibration Notes

- Validate this rubric on a small human-reviewed set before scaling judge usage.
"""


def components_template(feature_name: str, slug: str) -> str:
    return f"""feature_name: {feature_name}
slug: {slug}
system_prompt_components:
  - id: SP1
    purpose: role_or_global_instruction
    text: TODO
    expected_effect: TODO
  - id: SP2
    purpose: constraint_or_format_requirement
    text: TODO
    expected_effect: TODO
user_input_fields:
  - id: U1
    field: user_query
    description: TODO
context_sources:
  - id: C1
    source_type: retrieved_chunk_or_runtime_context
    description: TODO
    expected_effect: TODO
few_shot_examples:
  - id: F1
    description: TODO
    expected_effect: TODO
tooling_components:
  - id: T1
    kind: tool_description_or_schema
    description: TODO
post_processing_components:
  - id: P1
    kind: parser_or_guardrail
    description: TODO
"""


def ablation_plan_template(feature_name: str, slug: str) -> str:
    return f"""feature_name: {feature_name}
slug: {slug}
experiments:
  - id: EXP1
    hypothesis: TODO
    target_components:
      - SP1
    manipulation:
      remove: []
      rewrite: []
      substitute: []
    controls:
      freeze_case_inputs: true
      freeze_model_and_sampling: true
      freeze_retrieval_where_possible: true
    expected_signal: TODO
    success_measure: TODO
  - id: EXP2
    hypothesis: TODO
    target_components:
      - C1
    manipulation:
      remove: []
      rewrite: []
      substitute: []
    controls:
      freeze_case_inputs: true
      freeze_model_and_sampling: true
      freeze_retrieval_where_possible: true
    expected_signal: TODO
    success_measure: TODO
"""


def forensic_template(feature_name: str, slug: str) -> str:
    return f"""# {feature_name} Forensic Analysis

## Scope

- Feature: {feature_name}
- Slug: {slug}
- Benchmark slice: TODO
- Run ids compared: TODO

## Case Reading Protocol

- Read every failing case end-to-end.
- Read a representative sample of passing cases for contrast.
- Capture exact assembled prompts, context, tool traces, and parser outputs before making causal claims.

## Failure Clusters

- TODO

## Component Influence Ledger

| Component ID | Suspected effect | Supporting cases | Counterexamples checked | Confidence |
| --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO |

## Counterfactual Or Ablation Evidence

- TODO: Document one-component-at-a-time manipulations and resulting behavior changes.

## High-Confidence Optimizations

- TODO: Only list optimizations backed by trace evidence plus ablation or rerun evidence.

## Rejected Or Low-Confidence Ideas

- TODO: Keep a record of tempting but weakly-supported edits.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a first-pass EvalSmith artifact layout inside a target repository."
    )
    parser.add_argument("target_dir", help="Path to the repository to scaffold")
    parser.add_argument("--feature-name", required=True, help="Human-facing feature name")
    parser.add_argument("--slug", help="Optional feature slug; defaults to a slugified feature name")
    parser.add_argument(
        "--workflow-type",
        required=True,
        choices=sorted(WORKFLOW_TYPES),
        help="Workflow type to seed into the starter templates",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files if they already exist",
    )
    return parser.parse_args()


def ensure_writable(paths: dict[str, Path], force: bool) -> None:
    existing = [path for path in paths.values() if path.exists()]
    if existing and not force:
        joined = "\n".join(f"- {path}" for path in existing)
        raise FileExistsError(f"refusing to overwrite files because they already exist:\n{joined}")


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> int:
    args = parse_args()
    target_dir = Path(args.target_dir).expanduser().resolve()
    slug = args.slug or slugify(args.feature_name)
    paths = build_paths(target_dir, slug)

    try:
        ensure_writable(paths, force=args.force)
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    write_file(paths["workflow"], workflow_template(args.feature_name, slug, args.workflow_type))
    write_file(paths["spec"], spec_template(args.feature_name, slug, args.workflow_type))
    write_file(paths["cases"], cases_template())
    write_file(paths["rubric"], rubric_template(args.feature_name))
    write_file(paths["components"], components_template(args.feature_name, slug))
    write_file(paths["ablation"], ablation_plan_template(args.feature_name, slug))
    write_file(paths["forensic"], forensic_template(args.feature_name, slug))
    write_file(paths["traces_keep"], "")
    write_file(paths["reports_keep"], "")
    write_file(paths["runs_keep"], "")

    for path in paths.values():
        print(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
