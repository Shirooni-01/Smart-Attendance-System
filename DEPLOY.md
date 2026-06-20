# Deployment Guide

This document explains simple ways to deploy the Smart Attendance System.

## Docker (recommended)

Build the image:

```bash
docker build -t smart-attendance-system:latest .
```

Run the container:

```bash
docker run -p 5000:5000 --env-file .env -v $(pwd):/app smart-attendance-system:latest
```

Or using docker-compose:

```bash
docker-compose up --build
```

## Heroku (quick test)

1. Create a Heroku app:

```bash
heroku create your-app-name
```

2. Push code to Heroku:

```bash
git push heroku main
```

3. Scale the web process (if needed):

```bash
heroku ps:scale web=1
```

Note: For production use, prefer a process manager like `gunicorn` and add it to `requirements.txt` if deploying to Heroku.

## GitHub

Push the repository to GitHub and enable GitHub Actions CI. The included workflow will validate dependencies and check basic syntax on push.
