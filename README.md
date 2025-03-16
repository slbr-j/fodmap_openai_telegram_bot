# Project Name

AI Telegram Bot for FODMAP Consultation

## Description

This bot helps users receive nutritional guidance related to the FODMAP diet.  
The assistant is powered by OpenAI Assistants API and integrated into Telegram.

## Features

✅ AI-powered responses to user questions  
✅ Button-based navigation: FAQ, Tips, Product Catalog  
✅ Deployable on Railway (free tier supported)

## Local Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn main:app --reload`

## Deployment on Railway

1. Connect your GitHub repository to Railway
2. Add ENV variables:
    - TELEGRAM_TOKEN
    - OPENAI_API_KEY
    - ASSISTANT_ID
3. Run the pipeline
4. Set up the webhook:  
   `https://api.telegram.org/bot<YOUR_TELEGRAM_TOKEN>/setWebhook?url=<RAILWAY_DOMAIN>/webhook`

## Author

@slbr-j
