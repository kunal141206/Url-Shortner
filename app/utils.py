import string
import random
import validators

def generate_short_code(url_store):
    """Generate a unique 6-character alphanumeric code."""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(6))
        if not url_store.exists(code):
            return code

def validate_url(url):
    """Validate if the provided URL is valid."""
    return validators.url(url)