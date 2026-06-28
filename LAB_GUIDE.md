# Week 2 Lab Guide — Context Engineering: Memory, CLAUDE.md & RAG

**Time budget:** ~35–40 min within the 90-min live session.

**Prerequisite:** Comfortable directing Claude Code through a multi-step task (Week 1). Today's deck covered the three layers of grounding — CLAUDE.md, memory, RAG — and what context debt looks like. If any of those terms are unfamiliar, flip back before continuing.

---

## 1. Setup

1. Clone this repo and open it in your terminal.
2. Create a virtual environment, install dependencies, and confirm the baseline passes:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pytest
   ```
   All 4 tests should pass. This is **Ledger** — a small, working order/billing service. Nothing here is broken and nothing needs refactoring. The problem today isn't the code — it's everything *around* the code that isn't written down.
3. Don't open `CHANGELOG.md` yet. You'll want it fresh for Step 1.

---

## 2. Quick-reference card

You just covered this in the slides — this is here so you don't have to flip back during the exercise.

| Layer | Covers | Lifespan |
|---|---|---|
| CLAUDE.md | Conventions, architecture notes, do/don't | Static — identical every session |
| Memory | Decisions made, preferences learned | Accumulates over time |
| RAG | Large or changing docs/codebases | Fetched on demand |

**The test:** how often does it change, and how big is it? Stable + small → CLAUDE.md. Durable decision → memory. Large + changing → RAG.

---

## 3. The exercise

### Step 1 — Audit Ledger cold

Open `ledger.py`. Without running Claude Code yet, try to answer this yourself: **what would you need to know to safely change this code?** Specifically:

- What does `PaymentClient.charge()`'s `idempotency_key` argument actually protect against — and what happens if a caller generates a *fresh* key on every retry instead of reusing the same one?
- Why does `refund_order()` raise `NotImplementedError` for partial amounts? Is that a bug, a missing feature, or a decision?

Now check `docs/architecture.md`. Does it answer either question? Then check `CHANGELOG.md` — that's the artifact standing in for "the six-month-old Slack thread" from the slides. In a real codebase, a decision like this is just as often buried in a changelog, a closed PR description, or an old issue thread as it is in chat.

**Checkpoint:** whatever you just had to dig for — that's the actual context debt. Now ask Claude Code the same question (*"What would I need to know to safely modify `ledger.py`?"*) before doing anything else, and compare its cold answer to what you just found by hand.

### Step 2 — Write Ledger's CLAUDE.md

Direct Claude Code:

> Read through this repo, including CHANGELOG.md, and write a CLAUDE.md for it. Cover: project overview, conventions, do/don't, architecture notes, and test commands. Keep it short — if a rule needs a paragraph to justify itself, put the paragraph in the relevant source file or doc, not in CLAUDE.md.

**Checkpoint:** Read what it produced. Does the idempotency-key convention show up under "do / don't"? Does the partial-refunds restriction show up as a "don't," with a one-line pointer to *why* (a deferred product decision, not a bug) rather than the full backstory?

### Step 3 — Capture the one decision that isn't anywhere a fresh session would look first

Direct Claude Code to save a memory entry — project-level, same category as the slides — capturing the partial-refunds decision: deferred from v1, needs product sign-off before any engineering work starts on it. One sentence is enough.

**Checkpoint:** Start a **new** Claude Code session (or clear context) and ask: *"Can I safely add partial refunds to Ledger?"* — without re-explaining anything. Does it surface the memory entry unprompted?

### Step 4 — Before / after

Ask the same question — *"Can I safely add partial refunds to Ledger?"* — but imagine asking it cold, with no CLAUDE.md and no memory. You can actually test this: temporarily rename `CLAUDE.md` out of the way, ask, then restore it and ask again.

- **Before:** a plausible implementation sketch, no awareness the feature was deliberately deferred.
- **After:** surfaces the deferred decision instead of quietly reopening something already closed.

That difference — same model, same question, same code — is everything you just built.

---

## 4. Reflection prompts

Discuss with the group (or jot down if working solo):

1. What did you find in Step 1 that surprised you — something Claude Code's cold answer got wrong, or something you yourself almost missed?
2. What did you choose to leave **out** of CLAUDE.md, and why?
3. Is the partial-refunds decision really "context debt," or is `NotImplementedError` + a changelog entry already a reasonable way to document it? Where's the line between good-enough and actually missing?
4. If Ledger had ten more decisions like the refund one, would memory entries still scale, or would you reach for RAG over an actual decision log instead?

---

## 5. APPLY — your reps this week

Audit one real project you work in regularly:

- What would a cold session need to know that isn't written down anywhere?
- Write or improve its CLAUDE.md — five sections, nothing more.
- Set up at least one persistent memory entry — a decision that keeps almost getting re-explained.

Bring your biggest find to next session.

---

## Look ahead

Week 3 is **Skills** — turning the things you do repeatedly into packaged capabilities Claude can invoke on its own.
