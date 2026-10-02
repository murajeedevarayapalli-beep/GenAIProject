import os
from typing import Any, Dict, Optional

from openai import OpenAI


class LLMService:
    def __init__(self, model: Optional[str] = None):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None

    def generate_text(self, prompt: str) -> str:
        if not self.client:
            return (
                "Deterministic local fallback response: the request was processed with guarded "
                "deterministic logic because the OpenAI API is not configured in this environment."
            )

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text

    def structured_output(self, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self.client is None:
            return {
                "status": "ok",
                "summary": "Fallback structured output generated without external model.",
                "schema": schema,
            }

        completion = self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
