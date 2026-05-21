# qa-agent Interview Flow Script

This is a step-by-step script for walking through the `qa-agent` Claude Code plugin during an interview or live demo.

The core story:

> I am not hardcoding a Purchase-to-Pay tester. I am using a reusable QA-agent factory. The plugin gives me the structure: domain profile, agent contracts, evidence harness, adversarial testing, judge/evals, and guardrails. The specific business domain is configured through `domain_profile.yaml`.

---

## 0. Start Claude Code normally

From the target API/challenge repository, launch Claude Code:

```bash
claude
```

### What you are doing

You are starting from the actual project you want to test, not from inside the plugin repository.

The plugin will be installed into Claude Code and then used from this target repo.

### What to say

> I am launching Claude Code normally from the API repo. The QA tooling is packaged as a plugin, so I do not need a special local path or one-off setup script.

---

## 1. Add the plugin marketplace

Inside Claude Code, run:

```text
/plugin marketplace add jbcrane13/qa-agent
```

### What you are doing

You are telling Claude Code that the GitHub repository `jbcrane13/qa-agent` is a plugin marketplace.

This does not install the plugin yet. It only registers the marketplace as a source Claude Code can install from.

### What to say

> First I add my GitHub repo as a Claude Code plugin marketplace. This lets Claude install the QA-agent plugin by name instead of me copying files into the project.

---

## 2. Install the qa-agent plugin

Inside Claude Code, run:

```text
/plugin install qa-agent@qa-agent
```

### What you are doing

You are installing the `qa-agent` plugin from the `qa-agent` marketplace.

The format is:

```text
/plugin install <marketplace-name>@<plugin-name>
```

For this repo, both names are `qa-agent`, so the full install target is:

```text
qa-agent@qa-agent
```

### What to say

> Now I install the actual plugin from that marketplace. The repeated name looks a little funny, but it means plugin `qa-agent` from marketplace `qa-agent`.

---

## 3. Restart Claude Code

Exit Claude Code and start it again:

```bash
claude
```

Then verify inside Claude Code:

```text
/plugin list
```

### What you are doing

Restarting ensures Claude Code loads the newly installed plugin, including its commands, agents, skills, and hooks.

`/plugin list` confirms that the plugin is installed and enabled.

### What to say

> I restart once so Claude Code loads the plugin cleanly. Then I verify the plugin is enabled before I start generating any QA assets.

### Expected result

You should see `qa-agent` listed as enabled.

---

## 4. Run the narration helper

Inside Claude Code, run:

```text
/qa-agent:interview-narration
```

### What you are doing

You are asking the plugin to explain the architecture and demo story.

This command is useful at the start of rehearsal because it reminds you of the key framing:

- reusable QA-agent factory
- domain-driven profile
- separate explorer/adversary/judge roles
- auditable evidence log
- repeatable evals
- guardrails around tool use

### What to say

> I have a narration command in the plugin so the demo stays focused. The important thing is that the QA design is reusable: this challenge becomes a domain profile, not a one-off script.

---

## 5. Scaffold the QA harness

Inside Claude Code, run:

```text
/qa-agent:create-scaffold purchase_to_pay
```

### What you are doing

You are creating the domain-specific QA harness in the target project.

For this interview, the domain is `purchase_to_pay`, so the generated files should be tailored around a Purchase-to-Pay workflow while still using the generic plugin architecture.

The scaffold usually creates or updates files such as:

```text
qa_agents/
  domain_profile.yaml
  agent_contracts.md
  api_tool.py
  p2p_explorer_agent.py
  p2p_adversarial_agent.py
  p2p_judge.py
  evals/eval_report.py
```

### What to say

> This creates the local QA harness. The reusable plugin supplies the structure, and `purchase_to_pay` tells it which domain profile to initialize.

---

## 6. Inspect and explain the domain profile

Open or ask Claude to show:

```text
qa_agents/domain_profile.yaml
```

### What you are doing

You are checking the single source of truth for domain behavior.

This file should describe things like:

- entities
- workflow states
- allowed transitions
- business invariants
- invalid operations
- judge policy
- safety limits

### What to say

> This is the key abstraction. Instead of burying business rules inside agent prompts, I put the domain model in a small config file. That makes the agent factory reusable across APIs.

### Important framing

The agent should not be trusted because it sounds confident. It should be trusted because:

1. it uses a deterministic API tool,
2. it records evidence,
3. it tests invariants from the domain profile,
4. and a separate judge checks the final report.

---

## 7. Build the explorer agent

Inside Claude Code, run:

```text
/qa-agent:build-explorer http://localhost:8000
```

### What you are doing

You are generating or refining the API explorer agent for the target API running at `http://localhost:8000`.

The explorer’s job is to learn the API shape and establish valid behavior.

It should focus on:

- discovering endpoints
- finding a happy path
- identifying required fields
- recording successful calls
- producing evidence, not guesses

### What to say

> The explorer is the constructive agent. It learns how the API is supposed to work and establishes a known-good workflow before we start attacking edge cases.

---

## 8. Build the adversarial invariant tester

Inside Claude Code, run:

```text
/qa-agent:build-adversary http://localhost:8000
```

### What you are doing

You are generating or refining the adversarial agent.

The adversary’s job is not random fuzzing. It is targeted invariant testing.

It should try things like:

- skipping required workflow steps
- using invalid state transitions
- exceeding approval/payment limits
- reusing IDs or stale state
- submitting contradictory payloads
- attempting operations the domain profile says should be forbidden

### What to say

> The adversary is separate from the explorer on purpose. The explorer proves the happy path. The adversary tries to break the business rules. Keeping those roles separate reduces prompt contamination.

---

## 9. Build the judge

Inside Claude Code, run:

```text
/qa-agent:build-judge
```

### What you are doing

You are generating or refining the judge agent.

The judge evaluates the evidence produced by the explorer and adversary.

The judge should answer questions like:

- Did we prove the happy path works?
- Did we test the important invariants?
- Are failures backed by reproducible API calls?
- Is the final report complete enough for engineering to act on?
- Are there claims without evidence?

### What to say

> I do not want the same agent that ran the test to grade itself. The judge is a separate role that reviews evidence and decides whether the report is credible.

---

## 10. Build evals

Inside Claude Code, run:

```text
/qa-agent:build-evals
```

### What you are doing

You are generating or refining eval checks for the final report.

The evals should encode requirements like:

- report has required top-level sections
- findings include severity and evidence
- invariants from the domain profile are covered
- unsupported claims are rejected
- API call evidence is present

### What to say

> The eval layer makes the QA output repeatable. I am not just eyeballing the final report; I am checking that it satisfies a contract.

---

## 11. Run evals against the report

After the agents produce a report, run:

```text
/qa-agent:run-evals report.json
```

### What you are doing

You are validating the final QA report against the eval rules.

This is the final quality gate before treating the agent output as useful.

### What to say

> This is the quality gate. The report needs evidence, invariant coverage, and a shape that another engineer can reproduce. If it fails evals, I tighten the harness instead of pretending the demo is done.

---

## Full command sequence

```text
/plugin marketplace add jbcrane13/qa-agent
/plugin install qa-agent@qa-agent
```

Restart Claude Code.

```text
/plugin list
/qa-agent:interview-narration
/qa-agent:create-scaffold purchase_to_pay
/qa-agent:build-explorer http://localhost:8000
/qa-agent:build-adversary http://localhost:8000
/qa-agent:build-judge
/qa-agent:build-evals
/qa-agent:run-evals report.json
```

---

## Common gotchas

### Use namespaced plugin commands

Correct:

```text
/qa-agent:create-scaffold purchase_to_pay
```

Wrong for marketplace plugin usage:

```text
/create-scaffold purchase_to_pay
```

Plugin commands are namespaced to avoid collisions with commands from other plugins.

### Install commands run inside Claude Code

These are Claude Code slash commands, not shell commands:

```text
/plugin marketplace add jbcrane13/qa-agent
/plugin install qa-agent@qa-agent
```

### The target API must be running

Before build/exploration commands, the challenge API should be available at the URL you pass in, for example:

```text
http://localhost:8000
```

### The plugin is generic; the scaffold is domain-specific

`qa-agent` is the reusable plugin.

`purchase_to_pay` is just this interview’s domain profile.

---

## Closing explanation

Use this if asked to summarize what you built:

> This is a reusable QA-agent factory for API testing. It separates exploration, adversarial invariant testing, and judging into distinct roles. The domain rules live in `domain_profile.yaml`, and every claim should be backed by API-call evidence. The eval layer checks the final report so the result is repeatable instead of just a persuasive agent transcript.
