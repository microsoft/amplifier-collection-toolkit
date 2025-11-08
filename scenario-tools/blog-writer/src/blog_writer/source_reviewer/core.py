"""Stage 3: Source accuracy review (critical thinking).

Contract (Stud):
- Input: source_content (str), draft (str)
- Output: dict with {passed, issues, severity, missing_concepts, incorrect_representations}
- Config: SOURCE_REVIEWER_CONFIG (critical, temp=0.2)

Philosophy:
- This is a BRICK - self-contained, regeneratable from this spec
- Config is POLICY - tool decided temp=0.2 for strict evaluation
- AmplifierSession is MECHANISM - kernel unchanged
"""

from amplifier_core import AmplifierSession

from ..utils import extract_dict_from_response

SOURCE_REVIEWER_CONFIG = {
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
                "system_prompt": """You are a strict accuracy reviewer.

Your task is to verify that a blog post draft accurately captures the source material.

You will be given:
1. Original source material (brain dump/notes)
2. Draft blog post

Check for:
- Missing ideas/concepts from source
- Incorrect representation of source ideas
- Added ideas not in source
- Misunderstandings or misinterpretations

Respond with JSON:
{
    "passed": true/false,
    "issues": ["list of specific issues if any"],
    "missing_concepts": ["concepts from source not in draft"],
    "incorrect_representations": ["where draft misrepresents source"],
    "severity": "none/minor/major/critical"
}

Be strict but fair. Minor rephrasing is OK. Missing key ideas is not.""",
            },
        }
    ],
}


async def review_source_accuracy(source_content: str, draft: str) -> dict:
    """Review draft for source accuracy.

    Args:
        source_content: Original source material
        draft: Blog post draft

    Returns:
        Dict with review results: {passed, issues, severity, missing_concepts, incorrect_representations}
    """
    prompt = f"""Review the draft blog post for accuracy against the source material.

SOURCE MATERIAL:
{source_content}

DRAFT BLOG POST:
{draft}

Check for missing concepts, incorrect representations, and added ideas not in source.

Respond with JSON exactly in this format:
{{
    "passed": true or false,
    "issues": ["list of specific issues"],
    "missing_concepts": ["concepts from source not in draft"],
    "incorrect_representations": ["where draft misrepresents source"],
    "severity": "none" or "minor" or "major" or "critical"
}}"""

    async with AmplifierSession(config=SOURCE_REVIEWER_CONFIG) as session:
        response = await session.execute(prompt)

    return extract_dict_from_response(response)
