URL Shortener Service
Overview
This repository implements a simple URL shortening service similar to Bitly or TinyURL. The service provides endpoints to shorten URLs, redirect via short codes, view analytics, and check service health.
Built with Flask, entirely in-memory, with thread-safe operations and comprehensive tests.

Features
Shorten URLs: Generates unique 6-character alphanumeric codes.

Redirect Service: Resolves short codes with correct click counting.

Analytics: View click count, timestamps, and source URL.

URL Validation: Robust validation to ensure only correct URLs are shortened.

Thread-Safe: Protects storage and counters for concurrent requests.

Health Check Endpoint: Basic O.K. check for service monitoring.

Comprehensive Testing: Multiple Pytest test cases, covering success, errors, and edge cases.

Setup
Prerequisites
Python 3.8+

pip

Installation and Launch
bash
# Clone/download this repository
cd url-shortener

# Install dependencies
pip install -r requirements.txt

# Start the application
python -m flask --app app.main run

# The API will be available at http://localhost:5000

# Run tests
pytest
API Endpoints
1. Shorten URL
POST /api/shorten

Body:

json
{ "url": "https://www.example.com/very/long/url" }
Success Response:

json
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123"
}
Errors:

400: Invalid or missing URL

415: Incorrect Content-Type

2. Redirect
GET /<short_code>

Description: Redirects to original URL and increments click count.

On Success: HTTP 302 redirect to the long URL

Errors: 404 if code is not found

3. Get Analytics
GET /api/stats/<short_code>

Description: Returns analytics for a short code.

Success Response:

json
{
  "url": "https://www.example.com/very/long/url",
  "clicks": 5,
  "created_at": "2024-01-01T10:00:00"
}
Errors: 404 if not found

4. Health Check
GET /health

Response:

json
{ "status": "OK" }
File Structure
text
url-shortener/
│
├── app/
│   ├── main.py     # Application entrypoint
│   ├── models.py   # Data structures (if used)
│   ├── storage.py  # In-memory storage and thread-safe operations
│   ├── utils.py    # Helper functions (e.g., validation, short-code generation)
│   ├── blueprints/ # (Optional) Flask blueprints for route grouping
│   └── ...         # (Other modules as necessary)
├── tests/
│   ├── test_endpoints.py  # API endpoint tests, inc. error and concurrency
│   └── ...                # More test files as required
├── requirements.txt # Python dependencies
├── README.md        # (this file)
└── NOTES.md         # AI use documentation (if applicable)
Example Usage
Shorten a URL
bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'
Redirect
bash
curl -L http://localhost:5000/abc123
Get Analytics
bash
curl http://localhost:5000/api/stats/abc123
Health Check
bash
curl http://localhost:5000/health
Testing
To run the full test suite:

bash
pytest -v
Tests cover:

Valid/invalid shortening requests

Redirections (including error on missing code)

Analytics accuracy

Concurrency/multiple requests

Input validations and all documented errors

Notes
No database is used; everything is in-memory and resets on restart.

All key requirements (validation, code generation, thread-safety, error handling, test coverage) are met.

No authentication, UI, or custom user codes.