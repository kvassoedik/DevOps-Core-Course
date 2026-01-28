# LAB01 — DevOps Info Service (Python)

## 1) Framework Selection
I chose **Flask** because:
- It is lightweight and beginner-friendly.
- Minimal boilerplate for 2 endpoints.
- Perfect for small services and later containerization in Lab 2.

### Comparison
| Framework | Pros | Cons |
|---|---|---|
| Flask | Simple, minimal, easy to learn | No built-in async, fewer “auto features” |
| FastAPI | OpenAPI docs, async support, modern typing | Slightly more setup/learning |
| Django | Full ecosystem (ORM, admin) | Overkill for a small info service |

## 2) Best Practices Applied
- **Clean code organization:** helper functions for uptime/system/request info.
- **PEP8 style:** readable names, separated sections, docstrings.
- **Logging:** basic logging with configurable `LOG_LEVEL`.
- **Error handling:** JSON responses for 404 and 500.
- **Pinned dependencies:** exact version in `requirements.txt`.
- **Configuration via environment variables:** `HOST`, `PORT`, `DEBUG`, etc.

## 3) API Documentation

### GET /
Example:
```bash
curl -s http://127.0.0.1:5000/ | python -m json.tool
```
### GET /health
Example:
```bash
curl -s http://127.0.0.1:5000/health | python -m json.tool
```

## 4) Testing Evidence
The following screenshots confirm correct application behavior:

- docs/screenshots/01-main-endpoint.png - full JSON output from GET/
- docs/screenshots/02-health-check.png - response from GET/health
- docs/screenshots/03-formatted-output.png - pretty-printed JSON output

## 5) Challenges & Solutions
### Challenge
Correctly tracking application uptime and ensuring timestamps are always returned in UTC format.

### Solution
The application start time is stored once at startup using datetime.now(timezone.utc).
All timestamps and uptime calculations are based on UTC to avoid timezone-related issues.

## 6) GitHub Community
Starring repositories helps bookmark useful projects, increases their visibility, and shows appreciation to maintainers, which encourages open-source development.

Following professors, teaching assistants, and classmates helps build a professional network, improves collaboration, and allows learning from others’ activity and code in real time.