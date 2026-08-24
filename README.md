# TrendPilot - TikTok Trend Intelligence

AI-powered trend detection and content generation platform.

## Features

- **Multi‑source adaptive scraping** – fetches trending hashtags, sounds, and topics from multiple TikTok endpoints and learns which sources work best.
- **Trend analysis** – top videos, why it's trending, how to beat, top locations, comments sentiment, and relatability.
- **Movement & gesture detection** – uses MediaPipe to detect trending gestures and body movements.
- **Local & international trends** – region‑based trend discovery.
- **User authentication** – JWT tokens and hashed passwords.
- **Premium features** – Stripe integration (test mode ready).
- **Email alerts** – subscribe to top opportunity alerts.
- **Machine learning predictions**:
  - Success probability classifier (RandomForest)
  - Performance predictor for views, likes, comments, shares (RandomForest)
- **Dark mode & mobile‑friendly UI**

## Structure

- ackend/ – FastAPI backend, database, ML models, detectors
- rontend/ – Dashboard UI
- scripts/ – Build, fix, and feature scripts
- deploy_server.py – Main server for Render
- index.html – Main frontend for GitHub Pages
- 	rend_model.pkl – Success classifier
- performance_model.pkl – Performance predictor

## Live URLs

- Frontend: https://tinashechim.github.io/tiktok-trend-intelligence/
- API: https://tiktok-trend-intelligence.onrender.com
- Docs: https://tiktok-trend-intelligence.onrender.com/docs
