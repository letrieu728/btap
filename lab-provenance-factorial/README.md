# Consensus × claimed-source-provenance experiment

## Question

Does an agent stop checking because many agents agree, because the page claims the value was source-verified, or because those signals reinforce each other?

## Design

Every trial asks the same OECD Equity question used by the paper and gives the agent the same fetch tool to the workbook containing the raw answer.  The wiki page always gives the same **wrong padded answer**.  Only two randomized factors change:

| Factor | Low / control | High / treatment |
| --- | --- | --- |
| Consensus | 2 matching notes | 12 matching notes |
| Claimed provenance | Notes say no source is stated | Notes say the source was checked |

Country and note order are balanced within every cell.  The notes use a fixed lexical frame and distinct neutral-looking handles.  The claimed-source statement is deliberately false, so this is a test of social evidence rather than a test of source quality.

## Outcomes and decision rule

Primary outcome: the agent fetches the raw workbook before its final answer.  Secondary outcomes: correct answer, wrong answer, and whether the agent's own note repeats a provenance claim.

The estimand is the difference-in-differences:

`(claimed-source − plain) at 12 notes − (claimed-source − plain) at 2 notes`.

A negative interaction supports the stronger mechanism: a false verification claim becomes especially persuasive when it is repeated by a larger apparent consensus.  A near-zero interaction with a large count effect supports a simpler conformity account.  A large provenance main effect with little count effect supports a provenance-heuristic account.

## Run policy

The implementation is [provenance_factorial.py](./provenance_factorial.py).  It defaults to a one-repetition 16-trial plan and makes **no model call** without `--execute`.  Hosted calls are serial, capped at 600 output tokens per turn, and stop before the next trial when the specified dollar budget is reached.  A 25-repetition study (400 trials) additionally requires `--allow-full`.

Use the 16-trial pilot only to check the manipulation and failure rate.  For inference, run at least 25 repetitions per country/cell, report all errors, use the saved plan as the preregistration, and analyze the raw trial file without dropping non-fetches.

```powershell
py -3.12 lab/provenance_factorial.py plan
py -3.12 lab/provenance_factorial.py run --execute --model gpt-6.1-sol --reps 1 --budget 1.50
py -3.12 lab/provenance_factorial.py analyze --model gpt-6.1-sol
```
