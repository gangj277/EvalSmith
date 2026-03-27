# EvalSmith Artifact Contract

Use this file when creating or reviewing the repo-native artifacts produced by EvalSmith.

## Recommended Tree

```text
evals/
├── workflows/
│   └── <feature-slug>.md
├── specs/
│   └── <feature-slug>.yaml
├── cases/
│   └── <feature-slug>/
│       └── cases.jsonl
├── rubrics/
│   └── <feature-slug>.md
├── components/
│   └── <feature-slug>.yaml
├── experiments/
│   └── <feature-slug>/
│       └── ablation-plan.yaml
├── forensics/
│   └── <feature-slug>.md
├── traces/
│   └── <feature-slug>/
│       └── <run-id>/
│           └── <case-id>.json
├── reports/
│   └── .gitkeep
└── runs/
    └── .gitkeep
```

The exact structure can be adapted to the target repo, but the concepts should remain stable.

## Workflow Report

Path:

- `evals/workflows/<feature-slug>.md`

Required sections:

1. feature name and scope
2. probable user intent
3. entrypoints and key files
4. stage-by-stage workflow map
5. nondeterminism points
6. evaluation surfaces
7. open assumptions and missing evidence

## Eval Spec

Path:

- `evals/specs/<feature-slug>.yaml`

Required fields:

- `feature_name`
- `slug`
- `workflow_type`
- `entrypoint`
- `success_criteria`
- `dataset_sources`
- `criteria`
- `failure_modes`
- `component_inventory_file`
- `trace_capture`
- `forensic_analysis`
- `run_settings`

Suggested criterion record:

```yaml
- name: answer_groundedness
  grader: llm_rubric
  pass_threshold: 4
  scale: [1, 5]
  stage: generation
```

## Case File

Path:

- `evals/cases/<feature-slug>/cases.jsonl`

Each line should be one JSON object with this minimum shape:

```json
{
  "id": "case_001",
  "tags": ["happy-path"],
  "input": {
    "user_query": "..."
  },
  "expectations": {
    "must_include": [],
    "must_not_include": []
  },
  "scoring": {
    "primary": ["schema_valid", "answer_groundedness"]
  }
}
```

## Rubric File

Path:

- `evals/rubrics/<feature-slug>.md`

Required sections:

1. criterion definitions
2. pass or fail rules
3. ordinal or scalar rubric anchors if used
4. automatic fail conditions
5. known ambiguities or reviewer notes

## Component Inventory

Path:

- `evals/components/<feature-slug>.yaml`

Required sections:

1. `system_prompt_components`
2. `user_input_fields`
3. `context_sources`
4. `few_shot_examples`
5. `tooling_components`
6. `post_processing_components`

Every component should have a stable ID so forensic reports can reference it precisely.

## Ablation Plan

Path:

- `evals/experiments/<feature-slug>/ablation-plan.yaml`

Required fields per experiment:

- `id`
- `hypothesis`
- `target_components`
- `manipulation`
- `controls`
- `expected_signal`
- `success_measure`

The ablation plan is where EvalSmith states how it will test causal hypotheses instead of inferring causality from aggregate scores alone.

## Trace Artifact

Recommended path:

- `evals/traces/<feature-slug>/<run-id>/<case-id>.json`

Recommended fields:

- `case_id`
- `run_id`
- `assembled_system_prompt`
- `user_message`
- `few_shot_examples`
- `retrieved_context`
- `tool_schemas`
- `tool_calls`
- `tool_outputs`
- `intermediate_model_outputs`
- `final_output`
- `parsed_output`
- `grader_results`
- `failure_tags`

If the stack cannot capture every field, record what is unavailable and why.

## Forensic Analysis Report

Path:

- `evals/forensics/<feature-slug>.md`

Required sections:

1. benchmark slice and run ids
2. case reading protocol
3. failure clusters
4. component influence ledger
5. counterfactual or ablation evidence
6. high-confidence optimizations
7. rejected or low-confidence ideas

## Run Report

Recommended path:

- `evals/reports/<timestamp>-<feature-slug>.md`

Required sections:

1. evaluated commit or working state
2. benchmark slice used
3. aggregate results
4. case-level failures
5. failure clusters
6. likely root causes by stage
7. recommended next changes

## Comparison Report

Recommended path:

- `evals/reports/<timestamp>-<feature-slug>-comparison.md`

Required sections:

1. baseline run id
2. candidate run id
3. metric deltas
4. categories improved
5. categories regressed
6. confidence and caveats

## Bootstrap Tool

Use `python scripts/bootstrap_evalsmith.py <target-repo> --feature-name "<Feature Name>" --workflow-type <type>` to create the first-pass structure.

The generated files are starter artifacts, not final truth. They should be edited to fit the target repository.
