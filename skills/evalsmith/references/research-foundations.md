# EvalSmith Research Foundations

This file summarizes the primary-source ideas that shape EvalSmith. The point is not to cargo-cult papers. The point is to extract stable operating rules for a coding-agent skill that improves LLM systems inside real repositories.

## 1. Eval-driven, task-specific iteration beats vibe-based prompt editing

**Fact**

- OpenAI’s evaluation guidance says eval-driven development should happen early and often, with task-specific tests, automated scoring where possible, and continuous evaluation over time. It explicitly calls out vibe-based evaluation as an anti-pattern. Source: [OpenAI, Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
- Anthropic’s evaluation guidance says prompt engineering starts by defining specific, measurable, achievable, relevant success criteria, then building task-specific evals that mirror real-world distributions. Source: [Anthropic, Define success criteria](https://docs.anthropic.com/en/docs/test-and-evaluate/define-success) and [Anthropic, Develop tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests).

**Design implication for EvalSmith**

- Always derive the eval objective from the actual feature.
- Always include real-case distributions plus edge and adversarial cases.
- Prefer automated scoring whenever a reliable deterministic check exists.

## 2. Complex LLM systems need stage-level evaluation, not just final-output grading

**Fact**

- OpenAI’s trace grading guidance defines trace grading as assigning structured scores or labels to an agent trace so engineers can see where the system made mistakes, not merely whether the final output looked acceptable. Source: [OpenAI, Trace grading](https://developers.openai.com/api/docs/guides/trace-grading).
- DSPy models LM systems as text transformation graphs and optimizes entire pipelines against explicit metrics, not only single prompts. Source: [Khattab et al., 2023, DSPy](https://arxiv.org/abs/2310.03714).

**Design implication for EvalSmith**

- A workflow map is mandatory.
- Every workflow stage is a potential evaluation surface.
- Result interpretation should identify which stage most likely caused the failure.

## 3. LLM-as-judge is useful, but only with calibration and bias controls

**Fact**

- G-Eval showed stronger alignment with human judgments than earlier automatic metrics on summarization, but also highlighted bias toward LLM-generated text. Source: [Liu et al., 2023, G-Eval](https://arxiv.org/abs/2303.16634).
- MT-Bench / Chatbot Arena showed strong judges like GPT-4 can match human preferences reasonably well, while also documenting position, verbosity, and self-enhancement biases. Source: [Zheng et al., 2023, Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685).
- OpenAI’s grader guidance explicitly warns about grader hacking or reward hacking and recommends checking model-graded performance against expert human evaluation. Source: [OpenAI, Graders](https://developers.openai.com/api/docs/guides/graders).
- Anthropic recommends detailed rubrics, constrained output formats, and testing judge reliability before scaling. Source: [Anthropic, Develop tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests).

**Design implication for EvalSmith**

- Use LLM judges only when rule-based grading is insufficient.
- Make judge tasks discriminative: classification, pairwise choice, bounded scoring.
- Calibrate judge rubrics against a small human-reviewed set before trusting them.

## 4. Automated prompt optimization works, but only when the objective is explicit

**Fact**

- APE treats instruction search as program synthesis and reported better or comparable instructions to human-written prompts on many tasks. Source: [Zhou et al., 2022/2023, Large Language Models Are Human-Level Prompt Engineers](https://arxiv.org/abs/2211.01910).
- OPRO uses LLMs as optimizers over candidate prompts and reported task gains against human baselines on GSM8K and BBH. Source: [Yang et al., 2023/2024, Large Language Models as Optimizers](https://arxiv.org/abs/2309.03409).
- Self-Refine showed iterative feedback and refinement can improve first-pass outputs without additional training. Source: [Madaan et al., 2023, Self-Refine](https://arxiv.org/abs/2303.17651).
- TextGrad generalized the idea further by propagating textual feedback through compound systems and optimizing individual components against an objective function. Source: [Yuksekgonul et al., 2024, TextGrad](https://arxiv.org/abs/2406.07496).
- Revisiting OPRO found that optimizer quality is model-dependent and weaker models can be poor optimizers, which means naive auto-optimization is unreliable. Source: [Zhang et al., 2024, Revisiting OPRO](https://arxiv.org/abs/2405.10276).

**Design implication for EvalSmith**

- Optimization must be metric-driven.
- Recommendation-first is safer than blind auto-patching.
- The system should optimize the whole workflow when the prompt is not the real bottleneck.

## 5. RAG needs decomposed evaluation of retrieval and generation

**Fact**

- Ragas argues that RAG evaluation has multiple dimensions: retrieval quality, faithfulness to retrieved context, and generation quality, and proposes reference-free metrics for these dimensions. Source: [Es et al., 2023/2025, Ragas](https://arxiv.org/abs/2309.15217).
- OpenAI’s eval guidance for question answering over docs separates context recall, context precision, and answer quality rather than collapsing them into one generic score. Source: [OpenAI, Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

**Design implication for EvalSmith**

- For RAG, evaluate retrieval and answer generation separately.
- A bad final answer does not automatically imply a prompt problem.
- The artifact contract should keep retrieval evidence visible.

## 6. Stable rules EvalSmith should keep

1. Measure against explicit success criteria, not taste.
2. Grade the workflow at the stage where nondeterminism enters.
3. Prefer deterministic graders before LLM judges.
4. Treat judge models as fallible instruments that need calibration.
5. Optimize against a fixed benchmark slice so before/after claims are real.
6. Keep everything in the repo so humans can audit and edit the loop.

## 7. Prompt sensitivity is often instance-level, so forensic analysis must be case-level too

**Fact**

- ProSA argues that prompt sensitivity varies strongly across tasks, datasets, and models, and specifically emphasizes instance-level prompt variation. It also reports that larger models are generally more robust and that few-shot examples can reduce sensitivity. Source: [Zhuo et al., 2024, ProSA](https://arxiv.org/abs/2410.12405).

**Design implication for EvalSmith**

- Aggregate benchmark scores are not enough.
- The skill must read case-level traces and identify which prompt or context components are brittle on which cases.

## 8. Context faithfulness requires interventions that test whether context is actually controlling behavior

**Fact**

- Context-faithful Prompting shows that LLMs may ignore contextual cues in favor of parametric knowledge and that counterfactual demonstrations can improve faithfulness to the provided context. Source: [Zhou et al., 2023, Context-faithful Prompting](https://arxiv.org/abs/2303.11315).

**Design implication for EvalSmith**

- If a system uses retrieved or runtime context, the skill should test context influence explicitly.
- Counterfactual context swaps and chunk removals are valid forensic tools, not optional extras.

## 9. Inference: attribution requires controlled comparison, not just explanation

**Inference from sources**

The papers above do not provide a single universal prompt-forensics recipe. But taken together they support a practical rule:

- task-specific eval guidance says to measure real behavior on real distributions
- trace-grading guidance says to inspect intermediate steps
- prompt-sensitivity work says behavior can vary per instance
- context-faithfulness work says models can ignore provided context
- optimization papers say prompt improvements depend on the objective and model strength

Therefore EvalSmith should use a controlled attribution loop:

1. persist traces
2. inventory components
3. inspect failures case-by-case
4. run one-component-at-a-time manipulations
5. rerun the same slice
6. only then recommend changes
