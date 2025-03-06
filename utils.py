def validate_input(text):
    """
    Validate user input to ensure it meets basic requirements
    """
    # Check if the text is not empty after stripping whitespace
    if not text.strip():
        return False
        
    # Check if the text is not too long (arbitrary limit of 1000 characters)
    if len(text) > 1000:
        return False
        
    # Check for any obviously malicious content (basic check)
    dangerous_patterns = ['<script>', '</script>', 'DROP TABLE', 'DELETE FROM']
    return not any(pattern.lower() in text.lower() for pattern in dangerous_patterns)
