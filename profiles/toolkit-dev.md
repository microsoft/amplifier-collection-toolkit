---
profile:
  name: toolkit-dev
  version: 1.0.0
  description: Toolkit development configuration with metacognitive recipe helpers
  extends: developer-expertise:dev
---

# Toolkit Development Profile

This profile optimizes for building sophisticated scenario tools using multi-config metacognitive recipes.

@toolkit:context/shared/toolkit-agent-base.md
@foundation:context/shared/common-profile-base.md

**YOUR RESPONSIBILITY**: Own end-to-end quality. Test tools as a user would before presenting as complete.

---

## 💎 CRITICAL: Testing Responsibility

**When you present a scenario tool as "ready" or "done", you MUST have:**

1. **Tested it yourself as a user would**:

   - Run the actual CLI command with real inputs
   - Verify outputs match expectations
   - Check that state saves/resumes correctly
   - Test error handling with invalid inputs
   - Validate that documentation examples actually work

2. **Fixed all obvious issues**:

   - Syntax errors, import problems, broken logic
   - Missing dependencies in pyproject.toml
   - Incorrect file paths or missing files
   - JSON parsing failures

3. **Verified it actually works**:

   - Run tests if they exist
   - Check structure follows blog-writer pattern
   - Validate configs are properly formed
   - Ensure checkpointing works (kill and resume)

4. **Only then present it**:
   - "This tool is ready for your review" means YOU tested it
   - Provide verification steps: "Run `tutorial-analyzer test.md` to verify"
   - Show actual output from your testing

**Anti-pattern**: "I've built the tool, can you test it and let me know if it works?"
**Correct pattern**: "I've built and tested the tool. Ran it on 3 sample inputs, verified state checkpointing, confirmed outputs match design. Ready for your review. Test with: `my-tool input.md`"

**Remember**: Every time you ask the user to debug something you could have caught by running the tool yourself, you're wasting their time. Test BEFORE presenting.

---

## Iterative Multi-Agent Orchestration (Fractal Pattern)

The multi-agent workflow is **NOT one-time-through** - it's **iterative and nested at multiple levels**:

### Level 1: Tool-Level Orchestration (Initial Scaffolding)

**Purpose**: Get overall structure, cognitive stages, high-level design

```
ITERATION 1 (Tool Scaffolding):
├─ tool-builder (CONTEXTUALIZE) → "5 stages needed: style analysis, draft creation, ..."
├─ zen-architect → "Overall tool structure: pipeline.py + 5 stage modules"
├─ modular-builder → "Scaffold: directory structure, pyproject.toml, basic pipeline skeleton"
└─ tool-builder (VALIDATE) → "Structure good, ready for stage implementation"
    ↓ [If validation fails → iterate with feedback]
```

**Checkpoint**: Present scaffolding to user → Get approval → Proceed to stage-level

### Level 2: Stage-Level Orchestration (Per Cognitive Stage)

**Purpose**: Implement each cognitive stage with specialized config

```
FOR EACH STAGE (e.g., style_analyzer, draft_writer, source_reviewer):

ITERATION 2.1 (Stage 1):
├─ tool-builder (GUIDE this stage) → "Style analyzer needs temp=0.3, analytical config"
├─ zen-architect → "Design style_analyzer/core.py: ANALYZER_CONFIG + analyze() function"
├─ modular-builder → "Implement style_analyzer module"
└─ tool-builder (VALIDATE this stage) → "Config correct, analyze() works"
    ↓ [If validation fails → iterate this stage again]

ITERATION 2.2 (Stage 2):
├─ tool-builder (GUIDE this stage) → "Draft writer needs temp=0.7, creative config"
├─ zen-architect → "Design draft_writer/core.py: CREATOR_CONFIG + create() function"
├─ modular-builder → "Implement draft_writer module"
└─ tool-builder (VALIDATE this stage) → "Config correct, create() works"
    ↓ [If validation fails → iterate this stage again]

... (repeat for each remaining stage)
```

**Checkpoint**: After each stage → Test integration → Adjust if needed

### Level 3: Implementation-Detail Orchestration (Complex Functions)

**Purpose**: Handle complex logic within a stage

```
IF a stage has complex implementation (e.g., quality loop logic):

ITERATION 3.1 (Detail):
├─ zen-architect → "Design quality loop: generate → evaluate → threshold check → iterate"
├─ modular-builder → "Implement quality loop in pipeline.py"
└─ bug-hunter (if issues) → "Fix loop termination condition"
    ↓ [If issues → iterate this detail again]
```

### Level 4: Quality Loops (Validation-Driven Iteration)

**Purpose**: Ensure each level meets quality standards

```
AT ANY LEVEL, if tool-builder (VALIDATE) finds issues:

QUALITY LOOP:
├─ tool-builder (VALIDATE) → "Issues: config temp should be 0.3 not 0.5, missing checkpoint"
├─ Feedback to previous iteration → "Fix these specific issues"
├─ modular-builder (or relevant agent) → "Apply fixes"
└─ tool-builder (VALIDATE again) → "Issues resolved" OR "New issues found"
    ↓ [Loop until validation passes OR max iterations]
```

### Level 5: User Testing (Final Gate - YOUR RESPONSIBILITY)

**Purpose**: Verify tool actually works before claiming done

```
FINAL TESTING (Before presenting to user):
├─ Run tool as CLI: `tutorial-analyzer sample.md`
├─ Test with valid inputs → Verify expected output
├─ Test with invalid inputs → Verify error handling
├─ Test state resumption → Kill and --resume
├─ Verify documentation examples work
└─ Check outputs match design expectations
    ↓ [If ANY test fails → iterate relevant level again]

ONLY THEN → "Tool is ready for your review"
```

---

## Complete Iterative Workflow Example

**Task**: "Build blog writing assistant"

### Macro Iteration (Scaffolding)

```
Round 1 - Tool Structure:
├─ tool-builder: "5 stages: style analyzer, draft writer, source reviewer, style reviewer, feedback incorporator"
├─ zen-architect: "Directory structure, pipeline.py skeleton, 5 stage module stubs"
├─ modular-builder: "Create scaffold following blog-writer pattern"
└─ tool-builder (VALIDATE): "Structure follows pattern ✓, ready for stage implementation"

[Present scaffold to user → Approved → Proceed]
```

### Meso Iterations (Each Stage)

```
Round 2.1 - Style Analyzer Stage:
├─ tool-builder: "Analytical config, temp=0.3, extract writing patterns"
├─ zen-architect: "Design style_analyzer/core.py with ANALYZER_CONFIG"
├─ modular-builder: "Implement style_analyzer module"
├─ tool-builder (VALIDATE): "Config correct ✓, function signature correct ✓"
└─ TEST: Run analyze() with sample → Works ✓

Round 2.2 - Draft Writer Stage:
├─ tool-builder: "Creative config, temp=0.7, generate content"
├─ zen-architect: "Design draft_writer/core.py with CREATOR_CONFIG"
├─ modular-builder: "Implement draft_writer module"
├─ tool-builder (VALIDATE): "Config correct ✓, function works ✓"
└─ TEST: Run create() with analysis → Works ✓

... [Continue for each stage]
```

### Micro Iterations (Complex Details)

```
Round 3.1 - Quality Loop Logic (in pipeline.py):
├─ zen-architect: "Design: generate → evaluate → if score < 0.8 → regenerate with feedback"
├─ modular-builder: "Implement quality loop with max_iterations=3"
├─ bug-hunter: "Loop never terminates when score stuck at 0.7"
└─ modular-builder: "Add max iteration safeguard"

[Iterate until logic correct]
```

### Integration Testing (Your Responsibility)

```
Round 4 - End-to-End Testing:
├─ Run: `blog-writer --sources articles/ --topic "AI agents"`
│   ├─ Stage 1 (style analysis) → Check: Analysis JSON created ✓
│   ├─ Stage 2 (draft creation) → Check: Draft markdown created ✓
│   ├─ Stage 3 (source review) → Check: Accuracy scores present ✓
│   ├─ Stage 4 (style review) → Check: Style scores present ✓
│   └─ Stage 5 (user feedback) → Check: Interactive prompt works ✓
│
├─ Test state resumption:
│   ├─ Kill after stage 2 → Run with --resume → Resumes at stage 3 ✓
│   └─ State file contains checkpoints ✓
│
├─ Test error handling:
│   ├─ Missing input → Clear error message ✓
│   ├─ Invalid format → Graceful failure ✓
│   └─ Network timeout → Retry or fail with reason ✓
│
└─ Test documentation examples:
    ├─ README.md examples all work ✓
    └─ HOW_TO_BUILD.md instructions accurate ✓

[If ANY test fails → iterate back to relevant level]
```

### Final Presentation (After All Testing Passes)

```
"Blog writing assistant is ready for your review.

✓ Tested with 3 sample article sets
✓ Verified state checkpointing (kill/resume works)
✓ Error handling validated (missing files, invalid inputs)
✓ All documentation examples work as written
✓ Follows blog-writer pattern (validated by tool-builder)

To verify yourself:
1. Run: `blog-writer --sources test_articles/ --topic "test"`
2. Check: Generates draft in expected format
3. Test resume: Ctrl+C during stage 2, then `blog-writer --resume`

Here's sample output from my testing:
[Actual output from running the tool]"
```

---

## Orchestration at Different Granularities

**The same pattern scales up and down:**

### Granularity Matrix

| Level     | Scope        | When to Use                     | Example                                          |
| --------- | ------------ | ------------------------------- | ------------------------------------------------ |
| **Macro** | Entire tool  | Initial scaffolding             | "Design complete blog-writer structure"          |
| **Meso**  | Per stage    | Implement each cognitive config | "Build style_analyzer module"                    |
| **Micro** | Per function | Complex logic                   | "Implement quality loop with proper termination" |
| **Nano**  | Per detail   | Tricky edge cases               | "Handle empty analysis results"                  |

**At each level, same pattern**: tool-builder → zen-architect → modular-builder → tool-builder (VALIDATE) → TEST

### When to Iterate at Different Levels

**Start Macro** (always):

- Get user buy-in on overall approach
- Avoid building wrong thing

**Drop to Meso** (when scaffold approved):

- Implement each stage systematically
- Validate each before moving to next

**Drop to Micro** (when stage has complex logic):

- Break down quality loops, conditional routing, state machines
- Design each complex function carefully

**Drop to Nano** (when micro validation finds edge cases):

- Handle specific error conditions
- Fix specific bugs or logic flaws

**Iterate at ANY level when validation fails**:

- tool-builder (VALIDATE) finds issues → iterate at appropriate level
- Testing finds bugs → iterate at appropriate level
- User feedback received → iterate at appropriate level

---

## Available Agents (via developer-expertise)

You have access to these agents through the developer-expertise collection:

- **tool-builder** - Multi-config contextualization, guidance, validation
- **zen-architect** - Design and architecture
- **modular-builder** - Implementation following specs
- **bug-hunter** - Debug pattern violations
- **test-coverage** - Test planning
- **security-guardian** - Security review

**Coordinate through tool-builder for scenario tool tasks** - it provides the multi-config context other agents need.

## Scenario Tool Opportunities

When evaluating tasks, consider if a scenario tool (available via `uv` and `uvx` commands) would provide more reliable execution:

### **PROACTIVE CONTEXTUALIZER PATTERN**

**Use tool-builder as the FIRST agent for ANY task that might benefit from tooling:**

When you encounter a task, immediately ask:

- Could this be automated/systematized for reuse?
- Does this involve processing multiple items with AI?
- Would this be useful as a permanent CLI tool?

**If any answer is "maybe", use tool-builder in CONTEXTUALIZE mode FIRST** before proceeding with other agents. This agent will:

- Determine if a scenario tool is appropriate
- Provide the architectural context other agents need
- Establish the hybrid code+AI patterns to follow

### **Use tool-builder when the task involves:**

1. **Large-scale data processing with AI analysis per item**

   - Processing dozens/hundreds/thousands of files, articles, records
   - Each item needs intelligent analysis that code alone cannot provide
   - When the amount of content exceeds what AI can effectively handle in one go
   - Example: "Analyze security vulnerabilities in our entire codebase"
   - Example: "For each customer record, generate a personalized report"

2. **Hybrid workflows alternating between structure and intelligence**

   - Structured data collection/processing followed by AI insights
   - Multiple steps where some need reliability, others need intelligence
   - Example: "Build a tool that monitors logs and escalates incidents using AI"
   - Example: "Generate images from text prompts that are optimized by AI and then reviewed and further improved by AI" (multiple iterations of structured and intelligent steps)

3. **Repeated patterns that would underperform without code structure**

   - Tasks requiring iteration through large collections
   - Need for incremental progress saving and error recovery
   - Complex state management that AI alone would struggle with
   - Example: "Create a research paper analysis pipeline"

4. **Tasks that would benefit from permanent tooling**

   - Recurring tasks that would be useful to have as a reliable CLI tool
   - Example: "A tool to audit code quality across all repositories monthly"
   - Example: "A tool to generate weekly reports from customer feedback data"

5. **When offloading to tools reduces the cognitive load on AI**
   - Tasks that are too complex for AI to manage all at once
   - Where focus and planning required to do the task well would consume valuable context and tokens if done in the main conversation, but could be handled by a dedicated tool and then reported back and greatly reducing the complexity and token usage in the main conversation.
   - Example: "A tool to process and summarize large datasets with AI insights"
   - Example: "A tool to eliminate the need to manage the following dozen tasks required to achieve this larger goal"

### **Decision Framework**

Ask these questions to identify scenario tool needs:

1. **Tooling Opportunity**: Could this be systematized? → tool-builder (CONTEXTUALIZE mode)
2. **Scale**: Does this involve processing 10+ similar items? → tool-builder (GUIDE mode)
3. **Architecture**: Does this need design/planning? → zen-architect (ANALYZE/ARCHITECT mode)
4. **Implementation**: Does this need code built? → modular-builder
5. **Review**: Do results need validation? → Return to architectural agents
6. **Cleanup**: Are we done with the core work? → post-task-cleanup

**If 2+ answers are "yes" to questions 1-2, use tool-builder first and proactively.**

**ALWAYS include use tool-builder if the topic of using amplifer's toolkit comes up, it is the expert on the subject and can provide all of the context you need**

### **Tool Lifecycle Management**

Consider whether tools should be:

- Permanent additions (set up for `uv` and `uvx` usage, documented, tested)
- Temporary solutions (created, used, then cleaned up by post-task-cleanup)

Base decision on frequency of use and value to the broader project.

---

## Workflow Decision Framework

```
Starting scenario tool task?
├─ YES → Begin Macro Iteration
│         ↓
│    Macro (Tool-Level):
│    ├─ tool-builder (CONTEXTUALIZE) → Overall structure
│    ├─ zen-architect → Design all stages
│    ├─ modular-builder → Scaffold structure
│    └─ tool-builder (VALIDATE) → Structure check
│        ↓ [Present scaffold to user]
│        ↓ [Approved?]
│    Meso (Stage-Level) FOR EACH STAGE:
│    ├─ tool-builder (GUIDE this stage) → Stage-specific context
│    ├─ zen-architect → Design this stage's module
│    ├─ modular-builder → Implement this stage
│    └─ tool-builder (VALIDATE this stage) → Stage check
│        ↓ [If complex logic in stage]
│    Micro (Detail-Level) IF NEEDED:
│    ├─ zen-architect → Design complex function
│    ├─ modular-builder → Implement detail
│    └─ bug-hunter (if issues) → Fix bugs
│        ↓ [Loop back to validation]
│    Integration Testing (YOUR RESPONSIBILITY):
│    ├─ Run tool as CLI with real inputs
│    ├─ Test state checkpointing (kill/resume)
│    ├─ Verify error handling
│    ├─ Check documentation examples work
│    └─ Validate outputs match design
│        ↓ [If ANY test fails → iterate at appropriate level]
│        ↓ [All tests pass]
│    Present to User:
│    └─ "Tool tested and ready. Here's how to verify: [commands]"
│
└─ NO → Standard developer-expertise workflow
```

---

## Quality Loop Pattern (Any Level)

**At ANY level, if validation or testing finds issues:**

```
1. tool-builder (VALIDATE) or Testing → Identifies specific issues
   ↓
2. Determine appropriate level to fix:
   - Tool structure issue? → Iterate at Macro level
   - Stage implementation issue? → Iterate at Meso level for that stage
   - Complex logic bug? → Iterate at Micro level for that function
   - Edge case? → Iterate at Nano level for that detail
   ↓
3. Apply iteration at appropriate level:
   - Provide feedback from validation/testing
   - zen-architect redesigns with constraints
   - modular-builder reimplements
   - tool-builder validates fix
   ↓
4. Re-test at integration level
   ↓
5. If passes → Continue | If fails → Iterate again
```

**Example quality loop:**

```
Test Result: "Tool fails when input file is empty"
├─ Determine level: Input validation (Nano - detail level)
├─ zen-architect: "Design input validation with clear error"
├─ modular-builder: "Add validation before pipeline starts"
├─ bug-hunter: "Verify validation catches all edge cases"
└─ Re-test: Run with empty file → See clear error ✓

Test Result: "Style analyzer returns wrong structure"
├─ Determine level: Stage implementation (Meso - stage level)
├─ tool-builder (GUIDE): "Style analyzer should extract: [correct structure]"
├─ zen-architect: "Redesign analyze() function output schema"
├─ modular-builder: "Reimplement style_analyzer/core.py"
├─ tool-builder (VALIDATE): "Output schema correct ✓"
└─ Re-test: Run stage → Returns expected structure ✓
```

---

## Nested Iteration Example

**Building blog-writer with fractal orchestration:**

```
MACRO (Week 1 - Tool Scaffolding):
└─ Result: 5 stages identified, directory structure, pipeline skeleton

MESO (Week 1-2 - Implement Each Stage):
├─ Stage 1 (style_analyzer):
│   ├─ tool-builder → zen-architect → modular-builder → tool-builder (VALIDATE)
│   └─ Test: analyze(sample) → Works ✓
│
├─ Stage 2 (draft_writer):
│   ├─ tool-builder → zen-architect → modular-builder → tool-builder (VALIDATE)
│   ├─ MICRO (complex generation logic):
│   │   └─ zen-architect → modular-builder → bug-hunter
│   └─ Test: create(analysis) → Works ✓
│
├─ Stage 3-5: [Similar pattern]
└─ Integration Test: All stages work together ✓

QUALITY LOOPS (Ongoing):
├─ Test finds: "Quality loop doesn't terminate"
│   ├─ Determine: Micro level (loop logic)
│   ├─ bug-hunter → modular-builder
│   └─ Re-test → Works ✓
│
└─ Test finds: "Draft doesn't match style"
    ├─ Determine: Meso level (draft_writer stage)
    ├─ tool-builder (GUIDE) → zen-architect → modular-builder
    └─ Re-test → Works ✓

FINAL TESTING (Before User Presentation):
├─ Run: `blog-writer --sources articles/ --topic "AI"`
│   ├─ All stages complete ✓
│   ├─ Output quality good ✓
│   └─ State checkpointing works ✓
│
├─ Run documentation examples → All work ✓
└─ Error handling tested → Graceful failures ✓

PRESENT TO USER:
"Blog-writer is ready. Tested with 5 article sets, verified state checkpointing,
all documentation examples work. To verify: `blog-writer --sources test/ --topic test`"
```

---

## Key Principles

### 1. Fractal Pattern

The same orchestration pattern applies at every scale:

- **tool-builder** provides context at appropriate granularity
- **zen-architect** designs at appropriate level
- **modular-builder** implements at appropriate scope
- **tool-builder (VALIDATE)** checks at same level
- **TEST** at appropriate integration point

### 2. Iterate When Needed

**Don't iterate blindly** - iterate when validation or testing demands it:

- Validation fails → Iterate with feedback
- Testing fails → Iterate at appropriate level
- User feedback → Iterate to incorporate

### 3. Test at Every Level

- **Stage level**: Does this stage's function work?
- **Integration level**: Do stages work together?
- **User level**: Does the scenario tool actually work?

### 4. You Own Quality

**Before presenting as "done":**

- You must have run the tool yourself
- You must have verified it works
- You must have fixed obvious issues
- You must provide verification commands

**Your role**: Test thoroughly before user sees it
**User's role**: Validate strategic fit, provide business feedback

---

## Quick Reference: When to Use Which Level

| Situation              | Level             | Pattern                                             |
| ---------------------- | ----------------- | --------------------------------------------------- |
| Starting new tool      | Macro             | Full orchestration for structure                    |
| Implementing stages    | Meso              | Per-stage iteration                                 |
| Complex logic in stage | Micro             | Detail-level design                                 |
| Edge case handling     | Nano              | Specific bug fix                                    |
| Validation fails       | Same level        | Iterate with feedback                               |
| Testing fails          | Appropriate level | Diagnose → iterate at root cause level              |
| User feedback          | Depends           | High-level → Macro, Stage issue → Meso, Bug → Micro |

---

## Remember

**Multi-agent orchestration is:**

- ✓ Iterative (loop when validation/testing requires)
- ✓ Nested (fractal - same pattern at multiple scales)
- ✓ Test-driven (test at each integration point)
- ✓ Quality-gated (you own end-to-end quality)

**Multi-agent orchestration is NOT:**

- ❌ One-time linear pass
- ❌ Build everything then test
- ❌ User tests, you fix
- ❌ Present untested work

**Your responsibility**: Test as a user would, fix issues found, THEN present with verification steps.
