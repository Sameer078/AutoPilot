import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_LIST = [
    {
        "model_name": "fast-cheap",
        "litellm_params": {
            "model": "groq/llama-3.3-70b-versatile",
            "api_key": GROQ_API_KEY,
        },
        "model_info": {"provider": "Groq", "description": "Ultra fast + low cost"},
    },
    {
        "model_name": "balanced",
        "litellm_params": {
            "model": "gemini/gemini-3.5-flash",
            "api_key": GEMINI_API_KEY,
        },
        "model_info": {
            "provider": "Google",
            "description": "Balanced quality and latency",
        },
    },
    {
        "model_name": "smart-coding",
        "litellm_params": {
            "model": "gemini/gemini-3.5-flash",
            "api_key": GEMINI_API_KEY,
        },
        "model_info": {"provider": "Google", "description": "Best reasoning + coding"},
    },
]


ROUTING_CONFIG = {
    "code": {
        "low": "balanced",
        "medium": "balanced",
        "high": "smart-coding",
    },
    "summary": {
        "low": "fast-cheap",
        "medium": "fast-cheap",
        "high": "balanced",
    },
    "general": {
        "low": "fast-cheap",
        "medium": "fast-cheap",
        "high": "balanced",
    },
    "reasoning": {
        "low": "fast-cheap",
        "medium": "balanced",
        "high": "smart-coding",
    },
    "math": {
        "low": "fast-cheap",
        "medium": "fast-cheap",
        "high": "smart-coding",
    },
    "default": {
        "low": "fast-cheap",
        "medium": "balanced",
        "high": "smart-coding",
    },
}

FALLBACK_CONFIG = {
    "fast-cheap": [
        "gemini/gemini-3.5-flash",
        "qwen/qwen3-32b",
        "groq/compound",
        "groq/llama-3.1-8b-instant",
    ],
    "balanced": [
        "gemini/gemini-2.5-flash",
        "gemini/gemma-4-26b",
        "openai/gpt-oss-120b",
        "groq/llama-3.1-8b-instant",
        "qwen/qwen3-32b",
        "groq/llama-3.3-70b-versatile",
        "groq/compound",
    ],
    "smart-coding": [
        "gemini/gemini-2.5-flash",
        "groq/llama-3.1-8b-instant",
        "gemini/gemma-4-26b",
        "groq/llama-3.3-70b-versatile",
    ],
}
