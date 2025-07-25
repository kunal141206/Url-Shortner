import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_shorten_url_valid(client):
    """Test creating a short URL with valid input."""
    response = client.post('/api/shorten', 
                         json={'url': 'https://example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert len(data['short_code']) == 6

def test_shorten_url_invalid(client):
    """Test creating a short URL with invalid input."""
    response = client.post('/api/shorten', 
                         json={'url': 'invalid-url'})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_redirect_valid(client):
    """Test redirecting with a valid short code."""
    # First, shorten a URL
    shorten_response = client.post('/api/shorten', json={'url': 'https://example.com'})
    data = shorten_response.get_json()
    short_code = data['short_code']
    
    # Then, test redirect
    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == 301
    assert response.location == 'https://example.com'

def test_redirect_invalid(client):
    """Test redirecting with an invalid short code."""
    response = client.get('/invalid', follow_redirects=False)
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_stats_valid(client):
    """Test getting stats for a valid short code."""
    # First, shorten a URL
    shorten_response = client.post('/api/shorten', json={'url': 'https://example.com'})
    data = shorten_response.get_json()
    short_code = data['short_code']
    
    # Then, get stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    stats = response.get_json()
    assert 'url' in stats
    assert 'clicks' in stats
    assert 'created_at' in stats
    assert stats['url'] == 'https://example.com'
    assert stats['clicks'] == 0  # since no redirect yet

    # Optionally, test after redirect
    client.get(f'/{short_code}', follow_redirects=False)
    response = client.get(f'/api/stats/{short_code}')
    stats = response.get_json()
    assert stats['clicks'] == 1

def test_stats_invalid(client):
    """Test getting stats for an invalid short code."""
    response = client.get('/api/stats/invalid')
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_concurrent_requests(client):
    """Test handling multiple rapid URL shortening requests."""
    num_requests = 10
    short_codes = []
    
    # Simulate rapid requests in a single thread
    for _ in range(num_requests):
        response = client.post('/api/shorten', 
                             json={'url': 'https://example.com'})
        assert response.status_code == 201
        data = response.get_json()
        short_codes.append(data['short_code'])
    
    # Verify all requests succeeded and short codes are unique
    assert len(short_codes) == num_requests
    assert len(set(short_codes)) == num_requests  # all unique
    # Verify each short code is valid and retrievable
    for short_code in short_codes:
        response = client.get(f'/api/stats/{short_code}')
        assert response.status_code == 200
        stats = response.get_json()
        assert stats['url'] == 'https://example.com'