import json
from litellm import completion

class QueryClassifier:
    def __init__(self):
        self.model = "groq/llama-3.3-70b-versatile"

    def classify(self, query: str) -> dict:
        system_prompt = """
                    You are an intelligent AI routing judge.
                    Your task is to classify user prompts for LLM routing.
                    Return ONLY valid JSON.
                    Required JSON fields:
                    - task
                    - complexity

                    Allowed task values:
                    - code
                    - summary
                    - general
                    - reasoning
                    - math

                    Allowed complexity values:
                    - low
                    - medium
                    - high

                    Rules:
                    - Simple factual or casual queries => low
                    - Multi-step reasoning => medium
                    - Advanced coding/system design/research => high

                    Example Output:
                    {
                        "task": "code",
                        "complexity": "high"
                    }
        """

        response = completion(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            max_tokens=100,
        )

        content = response.choices[0].message.content
        parsed_response = json.loads(content)
        return self._validate_response(parsed_response)

    def _validate_response(self, response_data: dict) -> dict:
        valid_tasks = ["code", "summary", "general", "reasoning", "math"]
        valid_complexities = ["low", "medium", "high"]
        task = response_data.get("task", "general")
        complexity = response_data.get("complexity", "medium")

        if task not in valid_tasks:
            task = "general"

        if complexity not in valid_complexities:
            complexity = "medium"

        return {"task": task, "complexity": complexity}
