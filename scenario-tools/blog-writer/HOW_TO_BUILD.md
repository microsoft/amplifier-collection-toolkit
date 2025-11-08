# How to Build Your Own Tool Like This

**You don't need to be a programmer. You just need to describe what you want.**

This document shows you how the Blog Writer tool was created with minimal input, so you can create your own tools the same way using the amplifier-dev pattern.

---

## What the Creator Did

The person who "created" this tool didn't write a single line of code. Here's what they actually did:

### Step 1: Described What They Wanted

They started a conversation with Amplifier and described their goal in natural language:

> *Create me a tool that will take some brain dump I've done on a topic and write up a blog post in my style.*
>
> *I should be able to point to a directory of my current writings for it to use to understanding my style, and then also a source document that contains my new idea or brain dump.*
>
> *From there, it should have a writer that can read all of that in and draft up a first pass, trying to mimic my style, voice, etc.*
>
> *Afterwards, it should pass the resulting draft and the input brain dump to a source-reviewer to verify that it has captured my input content well, if it has not, give feedback and return it to the writer for improvement and back to the source-reviewer.*
>
> *After this, it should do pass the draft and my other writings and pass those to a style-reviewer to verify that it has captured my style, voice, and prior patterns from my other writing well - same deal, if not return to writer.*
>
> *Once it all passes, write the final version out for me to review. Give me the opportunity to mark up the doc with [bracket-enclosed-comments] and then pass it back to the tool to take in my feedback as the final reviewer - start back with the writer and then review again with the others, including passing my feedback along with the other context they previously had.*

That's it. **No code. No architecture diagrams. No technical specifications.**

### Step 2: Described the Thinking Process (Metacognitive Recipe)

Notice what they described:

1. "Understand my style from my writings" → **Style Analysis** (analytical thinking)
2. "Draft content matching that style" → **Draft Generation** (creative thinking)
3. "Review for accuracy against my source" → **Source Review** (critical thinking)
4. "Review for style consistency" → **Style Review** (evaluative thinking)
5. "Get my feedback and refine" → **Feedback Incorporation** (interpretive thinking)

This is what we call a **metacognitive recipe** - the "how should this tool think about the problem?" They described the thinking process, not the implementation.

### Step 3: Amplifier Translated to Multi-Config Pattern

Here's what Amplifier did automatically:

**Identified 5 distinct cognitive roles** → Created 5 specialized configs:

```python
# 1. STYLE_ANALYZER_CONFIG (analytical, temp=0.3)
#    Precise analysis of writing patterns
{
    "session": {"orchestrator": "loop-basic"},
    "providers": [{
        "module": "provider-anthropic",
        "config": {"model": "claude-sonnet-4-5", "temperature": 0.3}
    }]
}

# 2. DRAFT_WRITER_CONFIG (creative, temp=0.7)
#    Flowing, generative content creation
{
    "session": {"orchestrator": "loop-streaming"},
    "providers": [{
        "module": "provider-anthropic",
        "config": {"model": "claude-opus-4-1", "temperature": 0.7}
    }]
}

# 3. SOURCE_REVIEWER_CONFIG (critical, temp=0.2)
#    Strict accuracy checking
{
    "session": {"orchestrator": "loop-basic"},
    "providers": [{
        "module": "provider-anthropic",
        "config": {"model": "claude-sonnet-4-5", "temperature": 0.2}
    }]
}

# 4. STYLE_REVIEWER_CONFIG (evaluative, temp=0.2)
#    Consistency assessment
{
    "session": {"orchestrator": "loop-basic"},
    "providers": [{
        "module": "provider-anthropic",
        "config": {"model": "claude-sonnet-4-5", "temperature": 0.2}
    }]
}

# 5. FEEDBACK_INCORPORATOR_CONFIG (balanced, temp=0.5)
#    Understanding and applying user guidance
{
    "session": {"orchestrator": "loop-streaming"},
    "providers": [{
        "module": "provider-anthropic",
        "config": {"model": "claude-sonnet-4-5", "temperature": 0.5}
    }]
}
```

**Built orchestration code**:

```python
# Stage 1: Analyze style (once, then cached)
async with AmplifierSession(config=STYLE_ANALYZER_CONFIG) as session:
    style_profile = await session.execute(f"Analyze writing style: {samples}")
    save_state({"style_profile": style_profile})

# Stage 2: Draft content
async with AmplifierSession(config=DRAFT_WRITER_CONFIG) as session:
    draft = await session.execute(f"Write blog post: {source}\nStyle: {style_profile}")
    save_state({"draft": draft})

# Stage 3: Source review loop
while True:
    async with AmplifierSession(config=SOURCE_REVIEWER_CONFIG) as session:
        source_review = await session.execute(f"Review accuracy: {draft} vs {source}")

    if source_review["passed"]:
        break

    # Improve draft
    async with AmplifierSession(config=DRAFT_WRITER_CONFIG) as session:
        draft = await session.execute(f"Fix issues: {source_review['issues']}")

# Stage 4: Style review loop
# (similar pattern)

# Stage 5: User feedback loop
# (if feedback provided)
```

**The creator didn't need to know:**
- How to define multiple specialized configs
- When to use which temperature setting
- How to orchestrate between configs
- How to manage state across sessions
- How to implement quality loops
- How to parse user feedback
- Which orchestrator to use for each stage

### Step 4: Iterated to Refine

The tool didn't work perfectly on the first try. A few rounds of feedback like:

- "The style analysis should cache - it's expensive to rerun"
- "Draft review loop isn't terminating when it should"
- "User feedback comments aren't being extracted correctly"

Amplifier fixed these issues. Total time from idea to working tool: one conversation session.

---

## The Key Insight: Different Thinking Needs Different Settings

**This is the core of the amplifier-dev pattern:**

Traditional approach (single config):
```python
# One config tries to do everything
config = {"temperature": 0.5}  # Compromise between analytical and creative

# Mediocre at analysis (too high)
# Mediocre at creativity (too low)
# Mediocre at evaluation (not precise enough)
```

**Amplifier-dev approach (multi-config):**
```python
# Each stage optimized for its cognitive role
ANALYZER_CONFIG = {"temperature": 0.3}   # Precise analysis
WRITER_CONFIG = {"temperature": 0.7}     # Creative generation
REVIEWER_CONFIG = {"temperature": 0.2}   # Critical evaluation
```

**Result**: Each stage excels at what it does.

---

## How You Can Create Your Own Tool

### 1. Find a Need

Ask yourself:
- What repetitive task takes too much time?
- What process do I wish was automated?
- What would make my work easier?

**Examples from this collection:**
- "I need to write blog posts but it takes hours"
- "I need to improve tutorials based on learner experience"
- "I need to extract knowledge from documentation"

### 2. Describe the Thinking Process (Not the Code!)

Think about **how a human would approach this cognitively**:

**Good examples:**
- "First understand the user's style (analytical), then draft creatively, then review critically"
- "Read files to extract concepts (precise), then synthesize into summary (creative), then validate completeness (critical)"
- "Analyze current code (analytical), generate improvements (creative), evaluate quality (judgmental)"

**Bad examples:**
- "Use this library to do X" (too technical)
- "Create a function that does Y" (too implementation-focused)
- "Make it work" (too vague)

**Pro tip**: Think about different "cognitive modes":
- **Analytical**: Understanding, extracting, classifying (temp ~0.3)
- **Creative**: Generating, drafting, exploring (temp ~0.7)
- **Critical**: Evaluating, reviewing, catching errors (temp ~0.2)
- **Empathetic**: Simulating perspectives, understanding users (temp ~0.5)

### 3. Start the Conversation

```bash
# Use the toolkit-dev profile (optimized for tool building)
amplifier profile use toolkit-dev

# Start session
amplifier run --mode chat
```

Then describe your goal:

```
I need a tool that [your goal].

The thinking process should be:
1. First [analytical step] - understand X by doing Y
2. Then [creative step] - generate Z based on what was learned
3. Then [critical step] - evaluate if W criteria are met
4. Loop back if issues found

[Describe any human-in-loop points]
[Describe any state that should be cached]
```

### 4. Let Amplifier Identify the Configs

Amplifier will ask clarifying questions:

- "For the analysis step, should this be very precise or allow some creativity?"
- "Should drafting explore multiple options or follow constraints strictly?"
- "Should evaluation be strict pass/fail or provide detailed feedback?"

These questions help Amplifier choose the right temperature and model for each config.

### 5. Provide Feedback as Needed

When you try the tool, you'll likely find issues:

- "The analysis stage is too creative - make it more precise"
- "The drafting stage needs to be more adventurous"
- "The quality loop isn't terminating"

Just describe what's wrong in natural language. Amplifier will adjust the configs or flow.

### 6. Understand the Pattern (Optional But Valuable)

If you look at the generated code, you'll see:

```python
# Multiple specialized configs (one per cognitive role)
ANALYZER_CONFIG = {...}
CREATOR_CONFIG = {...}
EVALUATOR_CONFIG = {...}

# Code orchestrates which config when
async def process(input):
    # Analytical session
    async with AmplifierSession(config=ANALYZER_CONFIG) as session:
        analysis = await session.execute(...)

    # Creative session
    async with AmplifierSession(config=CREATOR_CONFIG) as session:
        creation = await session.execute(...)

    # Evaluative session
    async with AmplifierSession(config=EVALUATOR_CONFIG) as session:
        evaluation = await session.execute(...)

    # Code makes routing decisions
    if evaluation.score < threshold:
        # Loop back to creator
        pass
```

**Understanding this pattern helps you:**
- Describe future tools more precisely
- Debug issues more effectively
- Recognize when multi-config is beneficial

---

## Real Examples: What You Can Build

### Beginner-Friendly Ideas

**Documentation Improver**
- **Thinking process**: Write docs (creative) → Simulate confused reader (empathetic) → Identify unclear parts (analytical) → Rewrite (creative) → Loop
- **Configs needed**: 3 (writer, simulator, analyzer)

**Code Commenter**
- **Thinking process**: Read code (analytical) → Understand intent (interpretive) → Generate explanatory comments (creative)
- **Configs needed**: 3 (code analyzer, intent interpreter, comment writer)

### Intermediate Ideas

**Research Synthesizer**
- **Thinking process**: Extract concepts from papers (analytical) → Assess extraction quality (critical) → Detect gaps (analytical) → Re-read for gaps (focused) → Synthesize (creative)
- **Configs needed**: 4-5 (extractor, critic, gap detector, synthesizer)

**API Design Reviewer**
- **Thinking process**: Design API (creative) → Simulate client usage (empathetic) → Detect pain points (critical) → Redesign (creative) → Loop
- **Configs needed**: 4 (designer, simulator, critic, redesigner)

### Advanced Ideas

**Multi-Perspective Consensus Builder**
- **Thinking process**: Generate perspectives (creative) → Analyze independently (analytical) → Detect conflicts (critical) → Facilitate debate (balanced) → Synthesize consensus (creative)
- **Configs needed**: 5-6 (perspective generator, analyzers, conflict detector, debate facilitator, synthesizer)

**Tutorial Evolution Engine** (already exists - see tutorial-analyzer)
- **Thinking process**: Analyze content → Simulate learner → Diagnose issues → Plan fixes [HUMAN] → Apply → Re-simulate → Evaluate → Loop
- **Configs needed**: 6 (analyzer, simulator, diagnostician, planner, applier, evaluator)

---

## The Key Principles

### 1. Different Thinking = Different Configs

**Analysis** needs precision → temp=0.2-0.3
**Creation** needs exploration → temp=0.6-0.8
**Evaluation** needs strictness → temp=0.1-0.3
**Empathy** needs balance → temp=0.4-0.6

### 2. Code Orchestrates, AI Thinks

**Code handles**:
- Which config to use when
- State management across stages
- Quality loop decisions
- Human interaction points
- Flow control (loops, conditionals, jumps)

**AI handles**:
- Understanding natural language
- Analyzing content
- Generating content
- Making domain judgments

### 3. Multi-Config Makes Tools Smarter

Single-config tools are like asking one person to:
- Be analytical AND creative AND critical
- All at the same time

Multi-config tools are like having:
- An analyst (precise and thorough)
- A creator (imaginative and flowing)
- A critic (strict and uncompromising)
- Working together, each excelling at their role

### 4. You Describe, Amplifier Builds

You need to know:
- What problem you're solving
- How a human would think through it (cognitive roles)
- What quality looks like

You DON'T need to know:
- Python async/await
- How to configure LLM APIs
- State management patterns
- Error handling strategies

---

## Common Questions

**Q: Do I need to be a programmer?**
A: No. You need to understand the problem and describe the thinking process. Amplifier handles implementation.

**Q: How do I know how many configs I need?**
A: Count the distinct "cognitive roles" in your thinking process:
- Analysis = 1 config
- Creation = 1 config
- Multiple types of evaluation = multiple configs
Start with 2-3, add more if needed.

**Q: What if my tool needs 10+ configs?**
A: That's fine! The tutorial-analyzer has 6. More complex tools might have 10+. Each config stays simple because it does one thing.

**Q: How do I know what temperature to use?**
A: Ask Amplifier, or use these guidelines:
- Very precise/analytical: 0.1-0.3
- Balanced/interpretive: 0.4-0.6
- Creative/exploratory: 0.6-0.8

**Q: Can I modify configs after Amplifier creates them?**
A: Yes! Each stage module has its config in `src/your_tool/stage_name/core.py`. But it's usually easier to describe what you want changed and let Amplifier update it.

---

## Next Steps

### Study the Examples

1. **tutorial-analyzer** - 6 configs, complex flow, human-in-loop
2. **blog-writer** (this tool) - 5 configs, quality loops, feedback incorporation

### Try Building Something

Start simple:
- 2-3 cognitive roles (configs)
- Linear flow (no loops initially)
- One core capability

Example starter: "Documentation Quality Checker"
- Config 1: Read docs (analytical, temp=0.3)
- Config 2: Simulate confused reader (empathetic, temp=0.5)
- Config 3: Suggest improvements (creative, temp=0.6)

### Get Help

The `tool-builder` agent is available in the toolkit collection:

```bash
amplifier profile use toolkit-dev
amplifier run --mode chat

# Ask the tool-builder agent
"I want to create a tool that [describe your goal and thinking process]"
```

---

## The Power of This Pattern

**Before (single config)**:
- One config does everything
- Compromises on all tasks
- Hard to optimize
- Limited sophistication

**After (multi-config)**:
- Each config excels at its role
- No compromises
- Easy to tune (adjust individual configs)
- Unlimited sophistication (add more configs as needed)

**The magic**: Code orchestration + specialized configs = sophisticated emergent behavior

---

## Remember

The person who created this tool didn't write any code. They:

1. Described what they wanted (blog post generator)
2. Described the thinking process (analyze → draft → review → feedback)
3. Let Amplifier identify the cognitive roles (5 distinct roles)
4. Provided feedback to refine (a few iterations)

**You can do the same.**

The amplifier-dev pattern makes sophisticated tools accessible through natural language description of thinking processes.

For more examples and patterns, see:
- [Tutorial Analyzer](../tutorial-analyzer/README.md) - 6-config example
- [Toolkit Guide](../../docs/TOOLKIT_GUIDE.md) - Complete reference
- [Metacognitive Recipes](../../docs/METACOGNITIVE_RECIPES.md) - Advanced patterns

---

**Next**: Try creating your own tool using this pattern!
