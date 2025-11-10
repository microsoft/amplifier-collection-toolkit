# Blog Writer

**Transform brain dumps into polished blog posts in your writing style**

This tool takes your rough notes and creates a blog post that sounds like you wrote it, using your existing writings to understand your style, voice, and patterns.

---

## What It Does

1. **Learns your style** - Reads your existing blog posts to understand how you write
2. **Drafts content** - Creates a first version matching your style
3. **Verifies accuracy** - Checks the draft captures your ideas correctly
4. **Checks style** - Ensures it sounds like you
5. **Incorporates feedback** - Lets you provide comments and refines the draft

---

## Quick Start

```bash
# Install the toolkit collection (if not already installed)
amplifier collection add git+https://github.com/microsoft/amplifier-collection-toolkit@main

# Create a blog post
blog-writer \
  --source my-brain-dump.md \
  --style-dir ~/my-blog-posts/ \
  --output draft-post.md

# Review the draft, add [comments in brackets], then refine
blog-writer \
  --source my-brain-dump.md \
  --style-dir ~/my-blog-posts/ \
  --draft draft-post.md \
  --output final-post.md
```

---

## Usage

### Basic Usage

```bash
blog-writer --source <brain-dump> --style-dir <your-writings> --output <draft-file>
```

**Arguments**:
- `--source` - Your brain dump or rough notes (markdown file)
- `--style-dir` - Directory of your existing blog posts (learns from these)
- `--output` - Where to save the generated draft
- `--draft` (optional) - Existing draft with your feedback comments
- `--resume` (optional) - Resume from last checkpoint

### Interactive Mode (Default)

By default, the tool pauses after generating a draft for you to review and add feedback:

```bash
blog-writer --source ideas.md --style-dir ~/blog/ --output post.md

# Tool generates draft and pauses...
# Open .data/blog_writer_*/draft_iter_1.md
# Add [bracketed comments] inline
# Return to terminal and type 'done'
# Tool incorporates feedback and refines
```

Add feedback directly in the draft file:
```markdown
# My Title

This is the introduction. [Make this more engaging - add a hook]

## Section 1

Content here. [Add an example from the XYZ project]
```

Options at each pause:
- Type `done` - Apply your feedback and continue
- Type `approve` - Accept the draft as final
- Type `quit` - Save progress and exit

### Non-Interactive Mode

For automation or scripting:

```bash
blog-writer --source ideas.md --style-dir ~/blog/ --output draft.md --no-interactive
```

Or provide pre-marked feedback:

```bash
blog-writer --source ideas.md --style-dir ~/blog/ --draft draft-with-comments.md --output final.md
```

### Resume After Interruption

If the process is interrupted, resume where you left off:

```bash
blog-writer --source ideas.md --style-dir ~/blog/ --output draft.md --resume
```

---

## How It Works

### The Metacognitive Recipe

This tool uses **5 specialized AI configs**, each optimized for a specific thinking task:

1. **Style Analyzer** (precise, analytical)
   - Reads your existing writings
   - Identifies patterns, voice, structure preferences
   - Creates a style profile

2. **Draft Writer** (creative, generative)
   - Takes your brain dump + style profile
   - Generates initial draft matching your style
   - Focuses on capturing ideas naturally

3. **Source Reviewer** (precise, critical)
   - Compares draft to your original ideas
   - Checks for accuracy and completeness
   - Identifies missing or incorrect content
   - **Loops back to writer if issues found**

4. **Style Reviewer** (evaluative, critical)
   - Compares draft to your writing samples
   - Checks voice, tone, structure consistency
   - Identifies style mismatches
   - **Loops back to writer if issues found**

5. **Feedback Incorporator** (balanced, interpretive)
   - Reads your bracket comments
   - Understands your intent
   - Guides revision with your feedback
   - **Sends back through full review cycle**

### Why Multiple Configs?

Each stage needs different "cognitive settings":

- **Analysis** (style understanding): Precise, methodical (temp=0.3)
- **Creation** (drafting): Creative, flowing (temp=0.7)
- **Review** (accuracy/style): Critical, strict (temp=0.2)
- **Feedback** (interpretation): Balanced, empathetic (temp=0.5)

One config can't optimize for all these different thinking modes.

---

## Example Workflow

### Input: Brain Dump

```markdown
# Rough Notes on Modular Design

- systems are easier to understand when they're modular
- like lego bricks - you can see how pieces fit
- kernel stays simple, everything else swaps
- linux does this really well
- amplifier follows same pattern
```

### Output: First Draft

```markdown
# The Power of Modular Design: Lessons from Linux

When I look at complex systems, I'm always drawn to ones that feel
simple even when they're doing sophisticated things. The secret?
Modularity.

Think about LEGO. You don't need to understand the entire Death Star
to understand a single brick...

[rest of polished blog post in your style]
```

### With Your Feedback

Add comments: `[Add code example here] [This metaphor doesn't work - use containers instead]`

The tool incorporates your feedback and produces a refined version.

---

## Requirements

- Python >=3.11
- Amplifier core system
- amplifier-collection-toolkit
- At least 2-3 existing writing samples in `--style-dir`

---

## Philosophy

This tool embodies several key principles:

### Multi-Config Metacognitive Recipe

Code orchestrates thinking across specialized AI sessions:
- Code decides which config to use when
- Code manages state and checkpoints
- Code handles quality loops and user interaction
- Each AI session does one thing well

### State Checkpointing

Progress is saved after each expensive operation:
- Style analysis (cached)
- Draft generation
- Each review cycle

If interrupted, resume with `--resume` flag.

### Quality Loops

The tool doesn't just generate once - it checks and refines:
- Source accuracy loop (draft ↔ reviewer)
- Style consistency loop (draft ↔ reviewer)
- User feedback loop (feedback ↔ full cycle)

### Human-in-Loop

You control the final quality:
- Review the draft
- Add specific feedback
- Tool incorporates your guidance

---

## Tips

### Getting Better Results

1. **Provide multiple writing samples** (5-10 posts ideal)
2. **Use similar content** (if writing tech posts, use tech samples)
3. **Be specific in feedback** - "[Add example]" is better than "[improve this]"
4. **Iterate multiple times** - First draft → feedback → second draft → feedback

### Style Directory Structure

```
my-blog-posts/
  post-1.md
  post-2.md
  post-3.md
  ...
```

The tool reads all `.md` files recursively.

### Brain Dump Tips

- Don't worry about structure or polish
- Bullet points are fine
- Include examples, links, or references
- More detail = better output

---

## Advanced Usage

### Multiple Feedback Rounds

```bash
# Round 1
blog-writer --source ideas.md --style-dir ~/blog/ --output draft1.md

# Add feedback to draft1.md

# Round 2
blog-writer --source ideas.md --style-dir ~/blog/ --draft draft1.md --output draft2.md

# Add more feedback to draft2.md

# Round 3
blog-writer --source ideas.md --style-dir ~/blog/ --draft draft2.md --output final.md
```

### Custom Temperature Settings

Each stage module contains its config with temperature setting:
- `src/blog_writer/style_analyzer/core.py` - STYLE_ANALYZER_CONFIG (temp=0.3)
- `src/blog_writer/draft_writer/core.py` - DRAFT_WRITER_CONFIG (temp=0.7)
- `src/blog_writer/source_reviewer/core.py` - SOURCE_REVIEWER_CONFIG (temp=0.2)
- `src/blog_writer/style_reviewer/core.py` - STYLE_REVIEWER_CONFIG (temp=0.2)
- `src/blog_writer/feedback_incorporator/core.py` - FEEDBACK_INCORPORATOR_CONFIG (temp=0.5)

Adjust individual configs for more/less creativity in specific stages.

---

## Troubleshooting

### "Need at least 2 style samples"

**Cause**: Not enough files in `--style-dir`

**Fix**: Provide at least 2-3 existing writing samples

### "Draft has issues: [list]"

**Cause**: Source or style review found problems

**Action**: The tool automatically loops to fix these. If it keeps failing, check:
- Is your brain dump clear?
- Are your style samples consistent?
- Try providing more specific content

### Session Not Resuming

**Cause**: `--resume` flag needs an existing session directory

**Fix**: Check that `.data/blog_writer_*` directory exists, or run without `--resume` to create new session

---

## Contributing

Found a bug? Have an improvement? This tool follows the "describe what you want" pattern - just describe the change and Amplifier can help implement it.

---

## License

MIT License - see LICENSE file in the repository
