"""Stage 2: Learner experience simulation (empathetic thinking).

Contract (Stud):
- Input: str (tutorial content), dict (analysis from stage 1)
- Output: dict with keys: {confusion_points, clarity_issues, missing_context}
- Config: LEARNER_SIMULATOR_CONFIG (empathetic, temp=0.5)

Philosophy:
- This is a BRICK - self-contained, regeneratable from this spec
- Config is POLICY - tool decided temp=0.5 for empathetic simulation
- AmplifierSession is MECHANISM - kernel unchanged
"""

from amplifier_collection_toolkit import create_standalone_session

from ..utils import extract_dict_from_response

LEARNER_SIMULATOR_CONFIG = {
    "session": {
        "orchestrator": {
            "module": "loop-streaming",
            "source": "git+https://github.com/microsoft/amplifier-module-loop-streaming@main",
        },
        "context": {
            "module": "context-simple",
            "source": "git+https://github.com/microsoft/amplifier-module-context-simple@main",
        },
    },
    "providers": [
        {
            "module": "provider-anthropic",
            "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
            "config": {
                "model": "claude-opus-4-1",
                "temperature": 0.5,  # Empathetic simulation
                "system_prompt": """You are a learner encountering this tutorial for the first time.

Simulate the learning experience:
- Where do you get confused?
- What assumptions does the tutorial make?
- What context is missing?
- Which transitions are unclear?
- What examples would help?

Return JSON with keys: confusion_points, clarity_issues, missing_context, suggestions
""",
            },
        }
    ],
}


async def simulate_learner(content: str, analysis: dict) -> dict:
    """Simulate learner experiencing the tutorial.

    Args:
        content: Tutorial markdown content
        analysis: Analysis results from stage 1

    Returns:
        Dict with learner experience: {confusion_points, clarity_issues, missing_context, suggestions}
    """
    prompt = f"""Simulate learning from this tutorial:

TUTORIAL:
{content}

ANALYSIS:
{analysis}

As a learner encountering this for the first time, report:
- confusion_points: Where did you get stuck or confused?
- clarity_issues: What was hard to understand?
- missing_context: What background knowledge was assumed?
- suggestions: What would have helped?

Return as JSON.
"""

    async with await create_standalone_session(config=LEARNER_SIMULATOR_CONFIG) as session:
        response = await session.execute(prompt)

    return extract_dict_from_response(response)
