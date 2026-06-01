import time
from litellm import (
    Router,
    completion_cost,
)
from core.config import MODEL_LIST, FALLBACK_CONFIG


class LLMClient:
    def __init__(self):
        self.router = Router(
            model_list=MODEL_LIST,
            routing_strategy="latency-based-routing",
            num_retries=2,
        )

    def generate(self, tier: str, messages: list):
        start_time = time.time()
        response = self.router.completion(
            model=tier, messages=messages, fallbacks=FALLBACK_CONFIG.get(tier, [])
        )
        latency_ms = round((time.time() - start_time) * 1000, 2)

        try:
            cost = completion_cost(completion_response=response)
        except Exception:
            cost = 0

        metadata = {
            "model": response.model,
            "latency_ms": latency_ms,
            "cost_usd": round(cost, 6),
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        return response, metadata
