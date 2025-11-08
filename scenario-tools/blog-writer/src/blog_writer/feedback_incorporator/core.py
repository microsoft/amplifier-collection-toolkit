"""Stage 5: Feedback interpretation (balanced thinking).

Contract (Stud):
- Input: draft_with_feedback (str), source_content (str), style_profile (str)
- Output: dict with {feedback_items, overall_guidance, priority}
- Config: FEEDBACK_INCORPORATOR_CONFIG (balanced, temp=0.5)

Philosophy:
- This is a BRICK - self-contained, regeneratable from this spec
- Config is POLICY - tool decided temp=0.5 for balanced interpretation
- AmplifierSession is MECHANISM - kernel unchanged
"""

import re

from amplifier_core import AmplifierSession

from ..utils import extract_dict_from_response

FEEDBACK_INCORPORATOR_CONFIG = {
    "session": {
        "orchestrator": "loop-streaming",
        "context": "context-simple",
    },
    "providers": [
        {
            "module": "provider-anthropic",
            "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
            "config": {
                "model": "claude-sonnet-4-5",
                "temperature": 0.5,  # Balanced interpretation
                "system_prompt": """You are an expert at interpreting and applying feedback.

Your task is to understand user feedback (provided as [bracket comments] in text)
and create a revision plan.

You will be given:
1. Draft with [feedback comments]
2. Original source material
3. Style profile

Extract all feedback comments and interpret them:
- What specifically needs to change?
- Why did the user provide this feedback?
- How can this be addressed while maintaining style and accuracy?

Respond with JSON:
{
    "feedback_items": [
        {
            "location": "where in draft",
            "comment": "the [bracketed comment]",
            "interpretation": "what user wants",
            "action": "specific revision to make"
        }
    ],
    "overall_guidance": "summary of all feedback",
    "priority": "which feedback is most critical"
}

Be empathetic to user intent. Read between the lines when needed.""",
            },
        }
    ],
}


def extract_feedback_comments(draft_text: str) -> list[dict[str, str]]:
    """Extract [bracketed comments] from draft text."""
    pattern = r"\[([^\]]+)\]"
    matches = re.findall(pattern, draft_text)
    return [{"comment": match, "text": match} for match in matches]


async def interpret_feedback(draft_with_feedback: str, source_content: str, style_profile: str) -> dict:
    """Interpret user feedback comments.

    Args:
        draft_with_feedback: Draft with [bracket comments]
        source_content: Original source material
        style_profile: Author's style profile

    Returns:
        Dict with feedback interpretation: {feedback_items, overall_guidance, priority}
    """
    # Extract feedback comments first
    feedback_comments = extract_feedback_comments(draft_with_feedback)

    if not feedback_comments:
        return {"feedback_items": [], "overall_guidance": "No feedback provided", "priority": "none"}

    prompt = f"""Interpret user feedback comments and create revision guidance.

DRAFT WITH FEEDBACK (comments in [brackets]):
{draft_with_feedback}

ORIGINAL SOURCE MATERIAL:
{source_content}

STYLE PROFILE:
{style_profile}

Extract all [feedback comments] and interpret them.

Respond with JSON exactly in this format:
{{
    "feedback_items": [
        {{
            "location": "where in draft",
            "comment": "the [bracketed comment]",
            "interpretation": "what user wants",
            "action": "specific revision to make"
        }}
    ],
    "overall_guidance": "summary of all feedback",
    "priority": "which feedback is most critical"
}}"""

    async with AmplifierSession(config=FEEDBACK_INCORPORATOR_CONFIG) as session:
        response = await session.execute(prompt)

    return extract_dict_from_response(response)
