Smart Scheme Advisor - Minimal skeleton
====================================

What's included
- backend/: Flask-based API skeleton (models, api, seed)
- frontend/: React-based minimal UI with react-i18next
- docker-compose.yml to run Postgres + backend + frontend locally

Quick start (Linux/macOS)
1. Ensure Docker and docker-compose are installed.
2. From the project root (where docker-compose.yml is), run:
   docker-compose up --build
3. Backend API will be at http://localhost:5000/api
   Frontend dev server at http://localhost:3000

Notes
- This is a minimal skeleton for fast prototyping. Add real authentication, production-ready configs, migrations and secure secrets before deploying.
- To seed example data: exec into backend container and run `python seed.py` or run it locally with a configured DATABASE_URL.

Next steps I can do for you (tell me which):
- Generate the full admin UI code (React) with translation management pages.
- Add JWT auth and an admin CLI for managing schemes.
- Implement Postgres full-text search and Redis caching in the backend.
- Create GitHub Actions CI pipeline and a production-ready Dockerfile.

