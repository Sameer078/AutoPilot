import re


class GuardrailViolation(Exception):
    """Raised when a request violates safety rules."""

    pass


class GuardrailManager:
    INJECTION_PATTERNS = [
        r".*ignore\s+(all\s+|the\s+)?(previous|prior|above)\s+(instructions?|prompts?|rules?).*",
        r".*disregard\s+(the\s+|all\s+)?(previous|prior|earlier).*",
        r".*forget\s+.*(everything|instructions?|rules?).*",
        r".*you\s+are\s+(now\s+|a\s+)?(DAN|jailbroken|unrestricted|unfiltered).*",
        r".*pretend\s+(you\s+are|to\s+be).*(no\s+restrictions?|uncensored).*",
        r".*</?(system|user|assistant|im_start|im_end)>.*",
        r".*new\s+(instructions?|system\s+prompt|rules?)\s*:.*",
        r".*reveal\s+your\s+(system\s+)?prompt.*",
        r".*what\s+(is|are|were)\s+your\s+(original\s+)?instructions?.*",
    ]

    TOXIC_PATTERNS = [
        r"hate",
        r"terror",
        r"kill",
        r"hack",
        r"suicide",
        r"racial slur",
        r"violent attack",
    ]

    def __init__(self):
        self.injection_regex = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.INJECTION_PATTERNS
        ]
        self.toxic_regex = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.TOXIC_PATTERNS
        ]

    def validate_input(self, content: str):
        self._check_prompt_injection(content)
        self._check_toxicity(content)

    def validate_output(self, output: str):
        blocked_patterns = [
            "system prompt",
            "internal instructions",
            "developer instructions",
            "confidential prompt",
        ]
        for pattern in blocked_patterns:
            if pattern.lower() in output.lower():
                raise GuardrailViolation("Unsafe output detected")

    def _check_prompt_injection(self, content: str):
        for regex in self.injection_regex:
            if regex.search(content):
                print(f"🚨 PROMPT INJECTION DETECTED: {regex.pattern}")
                raise GuardrailViolation("Prompt injection detected")

    def _check_toxicity(self, content: str):
        for regex in self.toxic_regex:
            if regex.search(content):
                print(f"🚨 TOXIC CONTENT DETECTED: {regex.pattern}")
                raise GuardrailViolation("Toxic content detected")
