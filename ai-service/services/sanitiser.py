import bleach
import logging
import re

logger = logging.getLogger(__name__)

# Known prompt injection patterns to detect and block
INJECTION_PATTERNS = [
    r"ignore (all |previous |above )?instructions",
    r"disregard (all |previous |above )?instructions",
    r"forget (all |previous |above )?instructions",
    r"you are now",
    r"act as",
    r"pretend (you are|to be)",
    r"jailbreak",
    r"dan mode",
    r"override (all |previous |all previous )?instructions",
    r"system prompt",
    r"new instructions",
    r"from now on",
]

def strip_html(text):
    """
    Remove all HTML tags from input text.
    Example: <script>alert('xss')</script> → alert('xss')
    """
    cleaned = bleach.clean(text, tags=[], strip=True)
    return cleaned.strip()


def detect_prompt_injection(text):
    """
    Check if input contains prompt injection attempts.
    Returns True if injection detected, False if clean.
    """
    text_lower = text.lower()
    
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            logger.warning(f"Prompt injection detected — pattern: {pattern}")
            return True
    
    return False


def sanitise_input(text):
    """
    Main sanitisation function.
    1. Strips HTML
    2. Checks for prompt injection
    
    Returns:
        (cleaned_text, error_message)
        If safe: (cleaned_text, None)
        If unsafe: (None, error_message)
    """
    
    # Check if input is empty
    if not text or not text.strip():
        return None, "Input cannot be empty"
    
    # Strip HTML tags
    cleaned = strip_html(text)
    
    # Check for prompt injection
    if detect_prompt_injection(cleaned):
        return None, "Invalid input detected — potential prompt injection"
    
    # Check length — reject if too long
    if len(cleaned) > 2000:
        return None, "Input too long — maximum 2000 characters allowed"
    
    return cleaned, None