"""
LLM-based grievance categorization service.

This module provides functionality to automatically categorize grievances
using a Large Language Model (OpenAI GPT) based on the details provided
by the complainant.
"""

import os
from typing import Optional, Dict, Any
from openai import OpenAI, OpenAIError
import json


# Vaka Sosiale grievance categories and subcategories
CATEGORIES = {
    "1": {
        "name": "Inquiries and suggestions",
        "subcategories": {
            "1.1": "Inquiries",
            "1.2": "Suggestions/feedback"
        }
    },
    "2": {
        "name": "Registration related",
        "subcategories": {
            "2.1": "HH not registered - not informed",
            "2.2": "HH not registered - could not attend",
            "2.3": "HH member not registered",
            "2.4": "Request to update data"
        }
    },
    "3": {
        "name": "Socioeconomic (PMT classification)",
        "subcategories": {
            "3.1": "Poor/vulnerable excluded",
            "3.2": "Non-poor included",
            "3.3": "HH not registered"
        }
    },
    "4": {
        "name": "Misbehavior of registrant",
        "subcategories": {
            "4.1": "Fraud (false information)",
            "4.2": "Discourtesy"
        }
    },
    "5": {
        "name": "Staff performance",
        "subcategories": {
            "5.1": "Fraud",
            "5.2": "Inaction to requests",
            "5.3": "Discourtesy or poor service",
            "5.4": "Collection of any kind"
        }
    },
    "6": {
        "name": "Gender-based violence",
        "subcategories": {
            "6.1": "Sexual exploitation and abuse",
            "6.2": "Sexual harassment"
        }
    },
    "7": {
        "name": "Others (please describe)",
        "subcategories": {}
    }
}


def _format_categories_for_prompt() -> str:
    """Format categories into a readable string for the LLM prompt."""
    lines = []
    for main_id, main_data in CATEGORIES.items():
        lines.append(f"{main_id}. {main_data['name']}")
        for sub_id, sub_name in main_data['subcategories'].items():
            lines.append(f"   {sub_id} {sub_name}")
    return "\n".join(lines)


def categorize_grievance(details: str, model: Optional[str] = None) -> Dict[str, Any]:
    """
    Categorize a grievance based on its details using an LLM.
    
    Args:
        details: The grievance details text provided by the complainant
        model: Optional OpenAI model name (defaults to env var or gpt-4o-mini)
        
    Returns:
        Dictionary containing:
        - category: The main category number (e.g., "1", "2", etc.)
        - subcategory: The subcategory code (e.g., "1.1", "2.3", etc.)
        - category_name: Human-readable main category name
        - subcategory_name: Human-readable subcategory name
        - confidence: Confidence level (high/medium/low)
        - reasoning: Brief explanation for the categorization
        
    Raises:
        ValueError: If details is empty or None
        OpenAIError: If there's an error communicating with OpenAI API
    """
    if not details or not details.strip():
        raise ValueError("Grievance details cannot be empty")
    
    # Get API key and model from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    if not model:
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Construct the prompt
    categories_text = _format_categories_for_prompt()
    
    system_prompt = """You are an expert grievance categorization assistant for Vaka Sosiale, a social protection program. 
Your task is to analyze grievance descriptions and categorize them into the appropriate category and subcategory.

Be precise and consistent in your categorization. Consider the context and intent of the grievance carefully."""
    
    user_prompt = f"""Please categorize the following grievance into the appropriate category and subcategory from the Vaka Sosiale system.

Categories and subcategories:
{categories_text}

Grievance details:
{details}

Respond with a JSON object containing:
- category: The main category number (e.g., "1", "2")
- subcategory: The subcategory code (e.g., "1.1", "2.3") or null if category 7 (Others)
- confidence: "high", "medium", or "low"
- reasoning: Brief explanation (1-2 sentences) for why you chose this category

Example response format:
{{
    "category": "2",
    "subcategory": "2.3",
    "confidence": "high",
    "reasoning": "The grievance clearly states that a household member was not registered during the enrollment process."
}}"""
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent categorization
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        result = json.loads(response.choices[0].message.content)
        
        # Validate and enrich the response
        category = result.get("category", "7")
        subcategory = result.get("subcategory")
        
        # Validate category exists
        if category not in CATEGORIES:
            category = "7"
            subcategory = None
        
        # Get category and subcategory names
        category_data = CATEGORIES[category]
        category_name = category_data["name"]
        subcategory_name = None
        
        if subcategory and subcategory in category_data["subcategories"]:
            subcategory_name = category_data["subcategories"][subcategory]
        elif category != "7" and category_data["subcategories"]:
            # If no valid subcategory provided but category has subcategories, default to first
            first_subcat = list(category_data["subcategories"].keys())[0]
            subcategory = first_subcat
            subcategory_name = category_data["subcategories"][first_subcat]
        
        return {
            "category": category,
            "subcategory": subcategory,
            "category_name": category_name,
            "subcategory_name": subcategory_name,
            "confidence": result.get("confidence", "medium"),
            "reasoning": result.get("reasoning", "Categorized based on content analysis")
        }
        
    except OpenAIError as e:
        # Re-raise OpenAI errors for proper handling upstream
        raise
    except json.JSONDecodeError as e:
        # Fallback to "Others" category if JSON parsing fails
        return {
            "category": "7",
            "subcategory": None,
            "category_name": "Others (please describe)",
            "subcategory_name": None,
            "confidence": "low",
            "reasoning": "Unable to parse categorization response"
        }
    except Exception as e:
        # Fallback to "Others" category for any other errors
        return {
            "category": "7",
            "subcategory": None,
            "category_name": "Others (please describe)",
            "subcategory_name": None,
            "confidence": "low",
            "reasoning": f"Error during categorization: {str(e)}"
        }


def get_category_display(category: str, subcategory: Optional[str] = None) -> str:
    """
    Get a formatted display string for a category and subcategory.
    
    Args:
        category: Main category number
        subcategory: Optional subcategory code
        
    Returns:
        Formatted string like "2.3 HH member not registered" or "1. Inquiries and suggestions"
    """
    if category not in CATEGORIES:
        return "7. Others (please describe)"
    
    cat_data = CATEGORIES[category]
    
    if subcategory and subcategory in cat_data["subcategories"]:
        return f"{subcategory} {cat_data['subcategories'][subcategory]}"
    
    return f"{category}. {cat_data['name']}"
