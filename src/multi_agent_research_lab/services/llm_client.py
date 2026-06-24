"""LLM client abstraction.

Production note: agents should depend on this interface instead of importing an SDK directly.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client with an offline fallback."""

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a deterministic completion suitable for tests and demos."""

        content = (
            f"{system_prompt.strip()}\n\n"
            f"Bản nháp phản hồi:\n{user_prompt.strip()}\n\n"
            "Kết luận chính: cần dùng vai trò rõ ràng, shared state, guardrail, trace "
            "và benchmark metric để workflow nghiên cứu có thể kiểm chứng được."
        )
        input_tokens = self._estimate_tokens(system_prompt) + self._estimate_tokens(user_prompt)
        output_tokens = self._estimate_tokens(content)
        return LLMResponse(
            content=content,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=0.0,
        )

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return max(1, len(text.split()))
