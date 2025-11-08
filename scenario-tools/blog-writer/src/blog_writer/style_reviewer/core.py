"""Stage 4: Style consistency review (evaluative thinking).

Contract (Stud):
- Input: style_profile (str), style_samples (list[dict]), draft (str)
- Output: dict with {passed, issues, severity, voice_issues, tone_issues, structure_issues}
- Config: STYLE_REVIEWER_CONFIG (evaluative, temp=0.2)

Philosophy:
- This is a BRICK - self-contained, regeneratable from this spec
- Config is POLICY - tool decided temp=0.2 for strict evaluation
- AmplifierSession is MECHANISM - kernel unchanged
"""

from amplifier_core import AmplifierSession

from ..utils import extract_dict_from_response

STYLE_REVIEWER_CONFIG = {
    "session": {
        "orchestrator": "loop-basic",
        "context": "context-simple",
    },
    "providers": [
        {
            "module": "provider-anthropic",
            "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
            "config": {
                "model": "claude-sonnet-4-5",
                "temperature": 0.2,  # Strict evaluation
                "system_prompt": """You are a strict writing style reviewer.

Your task is to verify that a blog post draft matches the author's writing style.

You will be given:
1. Style profile (the author's style)
2. Draft blog post
3. Writing samples (for comparison)

Check for:
- Voice consistency (formal/casual, personal/impersonal)
- Tone consistency (the overall feeling)
- Structure patterns (paragraph length, headings, flow)
- Vocabulary level and choice
- Sentence patterns and rhythm
- Use of metaphors and examples
- Transition patterns

Respond with JSON:
{
    "passed": true/false,
    "issues": ["list of specific style mismatches"],
    "voice_issues": ["specific voice inconsistencies"],
    "structure_issues": ["structural pattern mismatches"],
    "tone_issues": ["tone inconsistencies"],
    "severity": "none/minor/major/critical"
}

Be strict. If it doesn't sound like the author, it doesn't pass.""",
            },
        }
    ],
}


async def review_style_consistency(style_profile: str, style_samples: list[dict], draft: str) -> dict:
    """Review draft for style consistency.

    Args:
        style_profile: Author's style profile
        style_samples: List of dicts with {"file": name, "content": text}
        draft: Blog post draft

    Returns:
        Dict with review results: {passed, issues, severity, voice_issues, tone_issues, structure_issues}
    """
    # Format samples for prompt
    samples_text = "\n\n---\n\n".join([f"## {s['file']}\n\n{s['content']}" for s in style_samples])

    prompt = f"""Review the draft blog post for style consistency.

STYLE PROFILE:
{style_profile}

WRITING SAMPLES (for comparison):
{samples_text}

DRAFT BLOG POST:
{draft}

Check for voice, tone, structure, vocabulary, and pattern consistency.

Respond with JSON exactly in this format:
{{
    "passed": true or false,
    "issues": ["list of specific style mismatches"],
    "voice_issues": ["voice inconsistencies"],
    "structure_issues": ["structural pattern mismatches"],
    "tone_issues": ["tone inconsistencies"],
    "severity": "none" or "minor" or "major" or "critical"
}}"""

    async with AmplifierSession(config=STYLE_REVIEWER_CONFIG) as session:
        response = await session.execute(prompt)

    return extract_dict_from_response(response)
