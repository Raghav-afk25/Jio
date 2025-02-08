# Telegram JioSaavn and Spotify Voice Chat Music Bot

A Telegram bot that allows you to search for and stream music into a voice chat directly from both JioSaavn and Spotify. This bot does NOT use YouTube.

**Important Note:** This bot requires a user account to perform the audio streaming and you must fill the environment variables.

## Features

- Search for songs by name.
- Streams music directly from JioSaavn or Spotify into voice chats.
- Displays results from both services.
- No YouTube integration.
- Implements a queueing system.
- Downloads audio before streaming (Preview quality)
- Shows download progress

## Setup

### Environment Setup

1.  **Install Python and Pip**: You need to have python and pip installed
2.  **Create a Virtual Environment**: Navigate to your project directory and use `python3 -m venv venv` (or `python -m venv venv`)
3.  **Activate the Environment**:
    •   **Linux/macOS**: `source venv/bin/activate`
    •   **Windows**: `venv\Scripts\activate`
4.  **Install Dependencies**: `pip install -r requirements.txt`
5. **Install ffmpeg** you must install `ffmpeg` on your machine

### API Credentials

1.  **Telegram Bot Token:**
    •   Create a bot in Telegram with BotFather.
    •   Obtain your bot token.
2.  **Spotify API Credentials:**
    •   Go to the Spotify Developer Dashboard.
    •   Create a new app.
    •   Obtain your client ID and client secret.
3.  **Telegram User API Credentials**
    * Obtain a user API ID and API Hash from the telegram API website
    * Use pyrogram to generate a session string for the bot
4.  **Jio Saavn API**
    * You do not need to generate any API key, and should just be able to send requests to the API outlined

### Running the Bot

1. Create a `.env` file and add:
