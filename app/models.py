from datetime import datetime
import threading

class URLStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._urls = {}  # short_code -> {url, clicks, created_at}

    def save(self, short_code, url):
        """Save a URL mapping with thread safety."""
        with self._lock:
            self._urls[short_code] = {
                'url': url,
                'clicks': 0,
                'created_at': datetime.utcnow().isoformat()
            }

    def get(self, short_code):
        """Retrieve URL data by short code with thread safety."""
        with self._lock:
            return self._urls.get(short_code)

    def increment_clicks(self, short_code):
        """Increment click count for a short code with thread safety."""
        with self._lock:
            if short_code in self._urls:
                self._urls[short_code]['clicks'] += 1

    def exists(self, short_code):
        """Check if a short code exists with thread safety."""
        with self._lock:
            return short_code in self._urls