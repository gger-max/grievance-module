"""
Router for LLM-based grievance categorization.

This module provides an API endpoint to categorize grievances using an LLM
before they are submitted to the backend.
"""

from fastapi import APIRouter, HTTPException
from openai import OpenAIError

from ..schemas import CategorizationRequest, CategorizationResponse
from ..services.llm_categorizer import categorize_grievance, get_category_display

router = APIRouter(prefix="/categorize", tags=["categorization"])


@router.post("/", response_model=CategorizationResponse)
def categorize_grievance_endpoint(request: CategorizationRequest):
    """
    Categorize a grievance based on its details using an LLM.
    
    This endpoint accepts grievance details and returns a suggested category
    and subcategory determined by analyzing the content with an LLM.
    
    Args:
        request: CategorizationRequest containing the grievance details
        
    Returns:
        CategorizationResponse with category, subcategory, confidence, and reasoning
        
    Raises:
        HTTPException: 400 if details are empty, 500 if LLM service fails
    """
    try:
        # Call the categorization service
        result = categorize_grievance(request.details)
        
        # Add display string
        display = get_category_display(result["category"], result["subcategory"])
        
        return CategorizationResponse(
            category=result["category"],
            subcategory=result["subcategory"],
            category_name=result["category_name"],
            subcategory_name=result["subcategory_name"],
            confidence=result["confidence"],
            reasoning=result["reasoning"],
            display=display
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except OpenAIError as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM service error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during categorization: {str(e)}"
        )
