from flask import Flask
from .models import URLStore
from .main import init_routes

def create_app():
    """Initialize the Flask application."""
    app = Flask(__name__)
    url_store = URLStore()

    from .main import init_routes
    init_routes(app, url_store)

    return app