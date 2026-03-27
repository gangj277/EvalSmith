# EvalSmith Method

Use this file when you need the detailed operating playbook for an EvalSmith run.

## 1. Scope The Target Feature

Before writing an eval plan, collect:

- likely user-facing feature name
- primary code entrypoint
- prompt assembly location
- model invocation site
- retrieval or tool dependencies
- structured output contract or parser
- existing tests, fixtures, and sample inputs
- any product spec, route name, or UI label that clarifies intent

If multiple candidate flows exist, rank them:

1. most likely primary user path
2. closest path with existing tests or fixtures
3. path with the clearest output contract

## 2. Build The Workflow Map

For each stage, capture:

- stage name
- source file or files
- inputs
- transformation performed
- deterministic or nondeterministic behavior
- dependency type: model, retrieval, tool, parser, business rule
- output artifact or contract
- likely failure surfaces

Then add a component inventory:

- atomic system-prompt clauses
- user-input fields
- retrieved context classes or chunk sources
- few-shot examples
- tool descriptions and schemas
- output parser or guardrail rules

Recommended workflow types:

- `single-prompt`
- `structured-output`
- `rag`
- `tool-calling`
- `multi-stage`

For `rag`, split retrieval and generation into separate stages.
For `tool-calling`, separate tool selection from tool argument construction and post-tool synthesis.
For `structured-output`, separate semantic quality from schema validity.

## 3. Design The Eval Plan

Every eval plan should answer:

- What is being tested?
- What does success look like?
- What case distribution is required?
- Which stages need direct grading?
- Which grader type is appropriate per criterion?

### Case Mix

Minimum benchmark mix:

- happy path
- edge case
- ambiguity case
- adversarial or abuse case
- regression case

### Grader Order

Use this order unless there is a specific reason not to:

1. code-based checks
2. schema validation
3. rule-based assertions
4. pairwise or categorical LLM grading
5. scalar LLM rubric grading
6. human review

### Failure Taxonomy

Use the smallest set that explains the system:

- instruction-following failure
- unsupported claim or hallucination
- missing required detail
- verbosity or brevity mismatch
- tone mismatch
- retrieval miss
- retrieval misuse
- wrong tool selected
- wrong tool arguments
- parser or schema failure
- state handoff failure
- stochastic instability

## 4. Execute The Smallest Useful Slice

Do not start with the entire benchmark if the harness is new.

Start with:

- 5 to 10 cases if wiring the harness
- one representative case per major failure mode
- repeated samples for only the most stochastic cases

Capture:

- case id
- raw input
- raw output
- stage outputs if available
- pass or fail per criterion
- aggregate score
- failure tags
- latency and cost when it matters
- exact trace artifacts needed to reconstruct each output

Do not call a slice “useful” if it cannot support later attribution.

## 5. Diagnose Before Editing

Use this symptom-to-cause discipline:

- bad final answer + good retrieval + valid schema
  - likely prompt or reasoning failure
- bad final answer + poor retrieval evidence
  - likely retrieval quality or ranking problem
- good semantics + schema failure
  - likely output contract or parser prompt problem
- wrong tool called
  - likely routing or tool description problem
- correct tool called + bad arguments
  - likely schema grounding or extraction problem
- highly variable outputs across repeated runs
  - likely underspecified instructions or brittle context

Distinguish:

- systematic failure: repeats on similar cases
- stochastic failure: passes and fails on the same case

Before proposing changes, perform a forensic pass:

1. Read every failing case trace end-to-end.
2. Read a sample of passing case traces for contrast.
3. Build a component influence ledger with confidence levels.
4. Write falsifiable causal hypotheses.
5. Run the smallest controlled manipulation that could falsify each important hypothesis.

Suggested attribution methods:

- prompt clause removal
- clause rewrite without changing intent
- context chunk removal
- context chunk replacement
- example substitution
- tool description tightening
- parser constraint removal or tightening
- order-only changes between otherwise identical prompts

## 6. Propose Changes In The Right Order

Prefer changes that reduce ambiguity before changes that add complexity.

Priority order:

1. clarify eval criteria and failure definitions
2. remove irrelevant or noisy context
3. improve retrieval filtering or chunk selection
4. tighten output contracts and examples
5. improve instruction ordering and constraints
6. split overloaded prompts into stages
7. add fallback handling or repair logic

For each recommendation, record:

- target stage
- target component ids
- expected causal mechanism
- evidence type: trace, contrastive case, ablation, rerun
- expected effect
- downside risk
- benchmark slice to rerun

## 7. What Good Looks Like

A strong EvalSmith run leaves the repo with:

- an auditable workflow map
- an eval plan another engineer could run
- benchmark cases tied to real behavior
- rubrics that are specific enough to calibrate
- a component inventory and attribution ledger
- trace artifacts rich enough to reconstruct behavior
- a result report that explains failures by stage
- an optimization proposal linked to evidence
