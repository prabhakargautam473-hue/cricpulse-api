# CricPulse API

A Python and Flask-based IPL cricket analytics REST API service with user registration/login, API key generation and JSON persistence, custom route authentication (`@require_api_key`), and interactive HTML pages styled with Tailwind CSS.

## Key Features

- **User Registration & Login:** Web forms (`/perform_registration`, `/login`) with JSON-backed credential storage (`user.json`).
- **API Key Generation & Storage:** Generate unique API keys (`key_<hex>`) via `/generate-key` and persist them in `api_keys.json` using standard Python file handling.
- **Protected API Endpoints (`@require_api_key`):** Secures IPL analytics endpoints (`X-API-Key` header validation) and returns clear JSON responses and status codes (`200`, `401`, etc.).
- **Cricket Analytics Endpoints:** Endpoints covering IPL teams, batters, bowlers, and season Orange Cap / Purple Cap records.
- **Themed Frontend Templates:** Standalone Jinja2 + Tailwind CSS templates (`register.html`, `login.html`, `api_key.html`, `docs.html`) with matching gradient/card styling and custom `<link rel="icon">` tab icons.

## Tech Stack

- **Backend:** Python, Flask
- **Data Persistence:** JSON files (`user.json`, `api_keys.json`)
- **Frontend:** HTML5, Jinja2, Tailwind CSS, Font Awesome
- **API Testing / Client:** Python `requests`

## Project Structure

```text
cricpulse-api/
├── app.py                  # Flask routes, auth/key logic, and @require_api_key decorator
├── api_keys.json           # Generated API keys and status records
├── user.json               # Registered user credentials/records
├── templates/
│   ├── register.html       # User registration page
│   ├── login.html          # User login page
│   ├── api_key.html        # API key generator & copy UI
│   └── docs.html           # API documentation page
└── README.md
```

## Setup & Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/your-repo-name.git](https://github.com/YOUR_USERNAME/your-repo-name.git)
   cd your-repo-name
   ```

2. **Install Flask and Requests:**
   ```bash
   pip install flask requests
   ```

3. **Start the Flask server:**
   ```bash
   python app.py
   ```
   The server runs by default at `http://127.0.0.1:8080`.

## Usage Example

### 1. Generate an API Key
Open `http://127.0.0.1:8080/generate-key` in your browser, submit your email, and copy the generated `key_...` value.

### 2. Call a Protected Endpoint with Python `requests`
```python
import requests

BASE_URL = "[http://127.0.0.1:8080](http://127.0.0.1:8080)"
API_KEY = "YOUR_GENERATED_API_KEY"

headers = {
    "X-API-Key": API_KEY
}

response = requests.get(f"{BASE_URL}/api/team", headers=headers, timeout=10)
print("Status:", response.status_code)
print("Data:", response.json())
```

If the `X-API-Key` header is missing or invalid, protected routes respond with HTTP `401` and a JSON error message (`{"error": "Invalid or missing API key"}`).

## Future Roadmap

- Add active/inactive key revocation checks directly inside `@require_api_key` and rate limiting.
- Migrate JSON file storage (`user.json`, `api_keys.json`) to a relational database (such as MySQL or SQLite).
- Integrate automated data pipelines / web scraping for fresher match stats and predictive analytics.