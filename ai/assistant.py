import os

from openai import OpenAI

from telemetry import analysis, state

from . import context, prompts

DEFAULT_MODEL = "gpt-4o-mini"

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not found. Check your .env file.")
        _client = OpenAI(api_key=api_key)
    return _client


def get_advice() -> str:
    client = _get_client()
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)

    telemetry = state.get_latest()
    corner_min_speed = analysis.get_last_corner_min_speed(state.get_history())
    if corner_min_speed is not None:
        telemetry["last_corner_min_speed"] = corner_min_speed

    race_context = context.build_context(telemetry)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompts.SYSTEM_PROMPT},
            {"role": "user", "content": prompts.build_user_prompt(race_context)},
        ],
    )
    return response.choices[0].message.content
