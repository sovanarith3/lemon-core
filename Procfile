web: gunicorn -w 4 -b 0.0.0.0:8080 indra:app
worker: python indra.py $DATABASE_URL
