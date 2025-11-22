"""
Main planning engine that orchestrates RAG + LLM + validation
"""
import json
import time
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.services.rag import build_rag_context
from app.services.llm_client import call_llm
from app.services.validation import extract_json_from_text, validate_event_plan
from app.config import settings
import logging

logger = logging.getLogger(__name__)


async def generate_plan(
    event_spec: Dict[str, Any],
    event_id: str,
    db: Session
) -> Dict[str, Any]:
    """
    Generate an EventPlan from EventSpec.
    
    Workflow:
    1. Convert event_spec to text for RAG
    2. Retrieve context (inventory, historic, templates)
    3. Build prompts
    4. Call LLM
    5. Extract and validate JSON
    6. Return EventPlan
    """
    start_time = time.time()
    
    # Convert event spec to text for RAG
    event_spec_text = json.dumps(event_spec, indent=2)
    
    # Build RAG context
    logger.info(f"Building RAG context for event {event_id}")
    context = build_rag_context(event_spec_text, db)
    
    # Load prompts
    try:
        with open("docs/prompts/system_prompt.txt", "r") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        system_prompt = """You are Lunaverse Show Brain, an elite Technical Director + Production Manager AI specializing in AV design, crew planning, and trucking logistics for corporate events."""
    
    try:
        with open("docs/prompts/json_format_spec.txt", "r") as f:
            format_spec = f.read()
    except FileNotFoundError:
        format_spec = "Output must be valid JSON matching the EventPlan schema."
    
    try:
        with open("docs/prompts/context_template.txt", "r") as f:
            context_template = f.read()
    except FileNotFoundError:
        context_template = "CONTEXT:\n{context}\n\nEVENT SPEC:\n{event_spec}"
    
    # Build user prompt
    user_prompt = f"""{format_spec}

{context_template.format(context=context, event_spec=event_spec_text)}

Generate the EventPlan JSON now:"""
    
    # Call LLM
    logger.info(f"Calling LLM for event {event_id}")
    llm_response = await call_llm(system_prompt, user_prompt, context)
    
    # Extract JSON
    generated_text = llm_response["text"]
    event_plan = extract_json_from_text(generated_text)
    
    if event_plan is None:
        logger.error(f"Failed to extract JSON from LLM response for event {event_id}")
        raise ValueError("LLM returned invalid JSON")
    
    # Validate structure
    is_valid, error_msg = validate_event_plan(event_plan)
    if not is_valid:
        logger.error(f"EventPlan validation failed: {error_msg}")
        raise ValueError(f"Invalid EventPlan structure: {error_msg}")
    
    # Add metadata
    generation_time = time.time() - start_time
    event_plan["metadata"] = {
        "model_used": settings.HF_MODEL_NAME,
        "generation_time_sec": round(generation_time, 2),
        "retrieval_context_count": len(context.split("\n"))
    }
    
    # Ensure event_id matches
    event_plan["event_id"] = event_id
    
    logger.info(f"Plan generated successfully for event {event_id} in {generation_time:.2f}s")
    
    return event_plan

