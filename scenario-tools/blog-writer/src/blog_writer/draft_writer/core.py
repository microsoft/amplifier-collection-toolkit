"""Stage 2: Draft generation (creative thinking).

Contract (Stud):
- Input: source_content (str), style_profile (str), revision_guidance (str | None)
- Output: str (blog post draft)
- Config: DRAFT_WRITER_CONFIG (creative, temp=0.7)

Philosophy:
- This is a BRICK - self-contained, regeneratable from this spec
- Config is POLICY - tool decided temp=0.7 for creative generation
- AmplifierSession is MECHANISM - kernel unchanged
"""

from amplifier_core import AmplifierSession

from ..utils import extract_text_from_response

DRAFT_WRITER_CONFIG = {
    "session": {
        "orchestrator": "loop-streaming",
        "context": "context-simple",
    },
    "providers": [
        {
            "module": "provider-anthropic",
            "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
            "config": {
                "model": "claude-opus-4-1",
                "temperature": 0.7,  # Creative generation
                "system_prompt": """You are an expert blog post writer.

Your task is to transform rough notes/brain dumps into polished blog posts
that match a specific writing style.

You will be given:
1. Source material (the ideas/brain dump)
2. Style profile (how to write)

Your output should:
- Capture ALL ideas from the source material
- Match the style profile precisely
- Flow naturally and engagingly
- Include appropriate examples and metaphors
- Have clear structure with good transitions
- Sound like the author wrote it themselves

Be creative in expression while faithful to the content.""",
            },
        }
    ],
}


async def generate_draft(source_content: str, style_profile: str, revision_guidance: str | None = None) -> str:
    """Generate blog post draft.

    Args:
        source_content: Source material (brain dump/notes)
        style_profile: Writing style to match
        revision_guidance: Optional guidance for revisions (from reviews or feedback)

    Returns:
        Blog post draft as text
    """
    if revision_guidance:
        # Revision based on feedback
        prompt = f"""Revise the blog post draft to address these issues:

REVISION GUIDANCE:
{revision_guidance}

ORIGINAL SOURCE MATERIAL:
{source_content}

STYLE PROFILE TO MATCH:
{style_profile}

Generate an improved draft that addresses all issues while maintaining style and accuracy."""
    else:
        # Initial draft
        prompt = f"""Write a blog post based on this source material, matching the specified writing style.

SOURCE MATERIAL (ideas/brain dump):
{source_content}

STYLE PROFILE TO MATCH:
{style_profile}

Generate a complete, polished blog post that:
1. Captures ALL ideas from the source material
2. Matches the style profile precisely
3. Flows naturally and engagingly
4. Includes appropriate examples and metaphors
5. Sounds like the author wrote it

Provide the complete blog post text."""

    async with AmplifierSession(config=DRAFT_WRITER_CONFIG) as session:
        response = await session.execute(prompt)

    return extract_text_from_response(response)
