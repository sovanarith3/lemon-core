EcoPulse AI
Overview
EcoPulse AI is a lightweight application designed to monitor farm conditions, providing basic advice on irrigation and crop health. Built by Age Industry, it integrates with the Lemon Biochip project to support sustainable agriculture, deployed on Railway's Hobby plan (1GB RAM, 0.5 vCPUs).
Features

Real-time farm condition monitoring (simulated data).
Simple advice generation (e.g., "Irrigate now!" or "Conditions are good").
Web interface accessible via Railway deployment.

Setup Instructions

Prerequisites:

Python 3.12
Git
Railway account with Hobby plan


Installation:

Clone the repository: git clone <your-repo-url>
Navigate to the directory: cd lemon-core
Install dependencies: pip install -r requirements.txt


Local Testing:

Run the app locally: python app.py
Access at http://localhost:8080


Deployment:

Push changes to the GitHub repository.
Connect to Railway and deploy via the dashboard.
Monitor logs for status.



Files

app.py: Flask web application with / and /health routes.
ecopulse.py: Background worker for advice generation.
requirements.txt: Dependencies (Flask, Gunicorn, scikit-learn, numpy).
Procfile: Defines web and worker processes for Railway.

Usage

Visit https://lemon-core-production.up.railway.app/ to see the status.
The /health endpoint ensures deployment stability.

Notes

Current deployment uses simulated data; integrate real sensors for production.
Adjust ecopulse.py sleep interval (e.g., 21600s) to optimize resource use.
Contact Sovanarith So for further development.

License
© 2025 Age Industry. All rights reserved.
