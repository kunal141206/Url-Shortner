from flask import request, redirect, jsonify, abort
from .models import URLStore
from .utils import generate_short_code, validate_url

def init_routes(app, url_store):
    """Initialize routes for the Flask application."""
    
    @app.route('/')
    def index():
        """Return a welcome message for the root URL."""
        return jsonify({
            'message': 'Welcome to the URL Shortener Service',
            'endpoints': {
                'shorten': 'POST /api/shorten',
                'redirect': 'GET /<short_code>',
                'stats': 'GET /api/stats/<short_code>',
                'health': 'GET /health'
            }
        })

    @app.route('/api/shorten', methods=['POST'])
    def shorten_url():
        """Create a short URL from a long URL."""
        data = request.get_json()
        if not data or 'url' not in data:
            abort(400, description="Missing 'url' in request body")

        url = data['url']
        if not validate_url(url):
            abort(400, description="Invalid URL format")

        short_code = generate_short_code(url_store)  # Pass url_store
        url_store.save(short_code, url)
        
        return jsonify({
            'short_code': short_code,
            'short_url': f"{request.host_url}{short_code}"
        }), 201

    @app.route('/<short_code>')
    def redirect_url(short_code):
        """Redirect to the original URL using the short code."""
        url_data = url_store.get(short_code)
        if not url_data:
            abort(404, description="Short URL not found")
        
        url_store.increment_clicks(short_code)
        return redirect(url_data['url'], code=301)

    @app.route('/api/stats/<short_code>')
    def get_stats(short_code):
        """Get analytics for a short code."""
        url_data = url_store.get(short_code)
        if not url_data:
            abort(404, description="Short URL not found")
        
        return jsonify({
            'url': url_data['url'],
            'clicks': url_data['clicks'],
            'created_at': url_data['created_at']
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': str(error.description)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': str(error.description)}), 404

    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({'status': 'healthy'}), 200