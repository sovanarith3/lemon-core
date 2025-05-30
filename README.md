# Indra AI Project

This is a Flask-based web application with an Indra AI worker, deployed on Railway.

## Project Structure
- `app.py`: Flask web application
- `indra.py`: Indra AI worker logic
- `templates/index.html`: HTML template for the status page
- `Procfile`: Defines web and worker processes
- `requirements.txt`: Python dependencies

## Deployment
- Deployed on Railway at `lemon-core-production.up.railway.app`
- Uses Gunicorn for the web process and a Python worker for Indra AI tasks

## Routes
- `/`: Status page
- `/health`: Health check
- `/logs`: Download logs
- `/memory`: Download memory data
