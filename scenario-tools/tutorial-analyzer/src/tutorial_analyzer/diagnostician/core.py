"""Stage 3: Issue diagnosis (precision thinking).

Contract (Stud):
- Input: dict (learner experience), dict (analysis)
- Output: dict with keys: {issues, severity, root_causes, priority}
- Config: DIAGNOSTICIAN_CONFIG (precise, temp=0.1)

Philosophy:
- This is a BRICK - self-contained, regeneratable from this spec
- Config is POLICY - tool decided temp=0.1 for diagnostic precision
- AmplifierSession is MECHANISM - kernel unchanged
"""

from amplifier_collection_toolkit import create_standalone_session

from ..utils import extract_dict_from_response

DIAGNOSTICIAN_CONFIG = {
    "session": {
        "orchestrator": {
            "module": "loop-basic",
            "source": "git+https://github.com/microsoft/amplifier-module-loop-basic@main",
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
                "model": "claude-sonnet-4-5",
                "temperature": 0.1,  # Diagnostic precision
                "system_prompt": """You are a pedagogy expert identifying tutorial issues.

Diagnose pedagogical problems:
- What are the root causes of confusion?
- Which issues are most critical?
- What patterns of problems exist?
- How do issues cascade?

Return JSON with keys: issues, severity, root_causes, priority
""",
            },
        }
    ],
}


async def diagnose_issues(learner_experience: dict, analysis: dict) -> dict:
    """Diagnose pedagogical issues from learner perspective.

    Args:
        learner_experience: Simulation results from stage 2
        analysis: Analysis results from stage 1

    Returns:
        Dict with diagnosis: {issues, severity, root_causes, priority}
    """
    prompt = f"""Diagnose pedagogical issues:

LEARNER EXPERIENCE:
{learner_experience}

TUTORIAL ANALYSIS:
{analysis}

Identify:
- issues: Specific pedagogical problems
- severity: How critical each issue is (critical/major/minor)
- root_causes: Why these issues exist
- priority: Recommended fix order

Return as JSON with arrays of issue objects.
"""

    async with await create_standalone_session(config=DIAGNOSTICIAN_CONFIG) as session:
        response = await session.execute(prompt)

    return extract_dict_from_response(response)
