"""
Hugging Face LLM client
"""
import httpx
import json
from typing import Dict, Any
from app.config import settings
import hashlib
import logging

logger = logging.getLogger(__name__)


def hash_prompt(prompt: str) -> str:
    """Hash prompt for logging (SHA-256)"""
    return hashlib.sha256(prompt.encode()).hexdigest()[:16]


async def call_llm(
    system_prompt: str,
    user_prompt: str,
    context: str = ""
) -> Dict[str, Any]:
    """
    Call Hugging Face Inference Endpoint
    
    Returns the raw response from the LLM
    """
    if not settings.HF_API_URL or not settings.HF_API_KEY:
        raise ValueError("HF_API_URL and HF_API_KEY must be configured")
    
    # Build full prompt
    full_prompt = f"{system_prompt}\n\n{context}\n\n{user_prompt}" if context else f"{system_prompt}\n\n{user_prompt}"
    
    # Log prompt hash (not full prompt)
    prompt_hash = hash_prompt(full_prompt)
    logger.info(f"LLM call - prompt_hash: {prompt_hash}, model: {settings.HF_MODEL_NAME}")
    
    # Prepare request
    headers = {
        "Authorization": f"Bearer {settings.HF_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": full_prompt,
        "parameters": {
            "temperature": settings.HF_TEMPERATURE,
            "max_new_tokens": settings.HF_MAX_NEW_TOKENS,
            "return_full_text": False
        }
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                settings.HF_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract generated text
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
            elif isinstance(result, dict):
                generated_text = result.get("generated_text", "")
            else:
                generated_text = str(result)
            
            return {
                "text": generated_text,
                "prompt_hash": prompt_hash
            }
        except httpx.HTTPError as e:
            logger.error(f"LLM HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

