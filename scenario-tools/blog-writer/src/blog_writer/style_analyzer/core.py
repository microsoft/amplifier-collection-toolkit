"""Stage 1: Style analysis (analytical thinking).

Contract (Stud):
- Input: list[dict] with {"file": name, "content": text}
- Output: str (style profile description)
- Config: STYLE_ANALYZER_CONFIG (analytical, temp=0.3)

Philosophy:
- This is a BRICK - self-contained, regeneratable from this spec
- Config is POLICY - tool decided temp=0.3 for analytical precision
- AmplifierSession is MECHANISM - kernel unchanged
"""

from amplifier_core import AmplifierSession

from ..utils import extract_text_from_response

STYLE_ANALYZER_CONFIG = {
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
                "temperature": 0.3,  # Analytical precision
                "system_prompt": """You are an expert writing style analyst.

Your task is to analyze writing samples and create a detailed style profile.

Focus on:
- Voice (formal/casual, personal/impersonal, serious/playful)
- Tone (confident/tentative, warm/cool, optimistic/realistic)
- Structure (paragraph length, section patterns, headings usage)
- Vocabulary (technical/accessible, simple/sophisticated)
- Sentence structure (short/long, simple/complex, rhythm)
- Metaphors and examples (types, frequency)
- Transitions and connectors
- Opening and closing patterns

Provide a detailed profile that another AI could use to mimic this style.""",
            },
        }
    ],
}


async def analyze_style(style_samples: list[dict]) -> str:
    """Analyze writing style from samples.

    Args:
        style_samples: List of dicts with {"file": name, "content": text}

    Returns:
        Style profile as text string
    """
    # Format samples for prompt
    samples_text = "\n\n---\n\n".join([f"## {s['file']}\n\n{s['content']}" for s in style_samples])

    prompt = f"""Analyze the writing style from these samples and create a detailed style profile.

WRITING SAMPLES:

{samples_text}

Provide a comprehensive style profile covering:
- Voice and tone
- Structure patterns
- Vocabulary and sentence patterns
- Use of metaphors/examples
- Transitions and flow
- Any unique characteristics

Format as detailed text that another AI can use to mimic this style."""

    async with AmplifierSession(config=STYLE_ANALYZER_CONFIG) as session:
        response = await session.execute(prompt)

    return extract_text_from_response(response)
