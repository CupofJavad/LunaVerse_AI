"""
JSON validation and repair utilities
"""
import json
import re
from typing import Dict, Any, Optional


def repair_json(text: str) -> Optional[str]:
    """
    Attempt to repair common JSON issues:
    - Remove trailing commas
    - Ensure keys are quoted
    - Fix single quotes to double quotes
    """
    # Remove trailing commas before closing braces/brackets
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    
    # Try to fix unquoted keys (basic attempt)
    # This is a simple heuristic - may not catch all cases
    text = re.sub(r'(\w+):', r'"\1":', text)
    
    # Fix single quotes to double quotes (if consistent)
    if text.count("'") > text.count('"'):
        text = text.replace("'", '"')
    
    return text


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from LLM response text.
    Tries multiple strategies:
    1. Direct JSON parse
    2. Extract JSON from code blocks
    3. Repair and parse
    """
    # Try direct parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    
    # Try to extract from markdown code blocks
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON object in text
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Try repair
            repaired = repair_json(json_str)
            if repaired:
                try:
                    return json.loads(repaired)
                except json.JSONDecodeError:
                    pass
    
    return None


def validate_event_plan(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate EventPlan structure.
    Returns (is_valid, error_message)
    """
    required_fields = ["event_id", "event_name", "summary", "assumptions", "rooms", "trucking", "metadata"]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate rooms structure
    if not isinstance(data["rooms"], list):
        return False, "rooms must be an array"
    
    for room in data["rooms"]:
        if not isinstance(room, dict):
            return False, "Each room must be an object"
        
        if "room_id" not in room or "name" not in room:
            return False, "Each room must have room_id and name"
        
        if "equipment" not in room or "crew" not in room:
            return False, "Each room must have equipment and crew arrays"
    
    # Validate trucking
    if not isinstance(data["trucking"], dict):
        return False, "trucking must be an object"
    
    if "estimated_trucks" not in data["trucking"]:
        return False, "trucking must have estimated_trucks"
    
    return True, None

