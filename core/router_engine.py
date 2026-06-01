from core.config import ROUTING_CONFIG


class RouterEngine:
    def __init__(self):
        self.routing_config = ROUTING_CONFIG

    def determine_tier(self, classification: dict) -> str:
        task = classification.get("task", "default")
        complexity = classification.get("complexity", "medium")
        if task not in self.routing_config:
            task = "default"
        if complexity not in ["low", "medium", "high"]:
            complexity = "medium"
        selected_tier = self.routing_config[task][complexity]
        return selected_tier
