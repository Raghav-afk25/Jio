
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from pytgcalls.types import AudioPiped
from pyrogram import Client
import io
import requests

# Spotify API credentials
SPOTIPY_CLIENT_ID = '95f4f5c6df5744698035a0948e801ad9'  # Replace with your actual client ID
SPOTIPY_CLIENT_SECRET = '4b03167b38c943c3857333b3f5ea95ea'  # Replace with your actual client secret

# Telegram Bot and Assistant credentials
TELEGRAM_TOKEN = '7073381155:AAHsMLX0Us5PTTFi1tKqO2ODJGrcCU-psz4' # Replace with your actual bot token

ASSISTANT_API_ID = 27898596  # Your assistant account's API ID from my.telegram.org
ASSISTANT_API_HASH = "621e4f1af531b312917560d4608f18b8"  # Your assistant account's API hash from my.telegram.org
ASSISTANT_SESSION_STRING = "BQGC-ccAWwiLhsvQpd7jdiZmReOM8zqPb-Ra9Je4THqbS0mq6jYnFQS-K9LDpz-YHqQUMsLOuLqgHdD1edUMQmQhPyjF38VcurIT2b4LYZVeFSzfjXoUKwOUsGIFzlvfo6bUrzM7ouhcP86quH4IR2LfueSXWJdDnvu8qS3Gm5-d7W2M13vebJ5NfEymsUAJW6zjR9IusQ8f5Nei7UzUZsl1ww6cI8T_gcu6wiSP1LfWjOVQ97G6ab3-2jxJ-nPlA3cGi8q5dHhIB81LRZymSq03oSXEMJihIOXPfj2pI0XGlI-Y85nC60hSwXuV5Y02_VmAZ_j157Co39b2r77gjfXzvfMcjgAAAAG0-mQtAA"  # Get this manually or through phone number auth

# Initialize Spotify client
spotify = Spotify(auth_manager=SpotifyClientCredentials(client_id='95f4f5c6df5744698035a0948e801ad9', client_secret='4b03167b38c943c3857333b3f5ea95ea'))

# Global variables
bot = None  # Telegram Bot Client
assistant = None  # Telegram Assistant Client
pytgcalls = None  # PyTgCalls instance

# Helper function to get a playable audio stream URL from Spotify
async def get_spotify_audio_stream(track_id):
    """Gets a playable audio stream URL for a Spotify track ID."""
    try:
        # IMPORTANT: This is a placeholder. Direct streaming *from* Spotify is
        # very difficult due to DRM and proprietary codecs. This tries to
        # find a playable stream from a *different* source corresponding to
        # the same track.

        track = spotify.track(track_id)
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        # VERY IMPORTANT: This is a placeholder! You'll need to replace this
        # with code that actually finds an audio stream for the song from a
        # *different* source. Many services exist that provide music
        # streams, but they typically require authentication.

        # This section simulates searching for audio URL; replace it with an
        # actual implementation.
        search_query = f"{track_name} {artist_name} audio stream"  # Simplistic web search

        # For demonstration purposes, using a direct link to a sample sound
        # Replace with a proper streaming URL
        stream_url = "https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"

        # Download file from URL and create in-memory file-like object
        response = requests.get(stream_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Wrap the content in an io.BytesIO object to simulate a file-like object
        audio_stream = io.BytesIO(response.content)

        return audio_stream
    except Exception as e:
        print(f"Error getting audio stream: {e}")
        return None


# Function to play a song by name on VC using the assistant account
async def play_song(update: Update, context: CallbackContext):
    """Plays a song from Spotify in the voice chat using the assistant account."""
    global pytgcalls
    chat_id = update.effective_chat.id
    query = ' '.join(context.args)

    if not query:
        await update.message.reply_text("Please provide a song name.")
        return

    try:
        results = spotify.search(query, limit=1, type='track')
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            track_id = track['id']
            spotify_url = track['external_urls']['spotify']

            await update.message.reply_text(f"Searching for: {track_name} - {artist_name}...")

            audio_stream = await get_spotify_audio_stream(track_id) #Get track info

            if audio_stream:
                await update.message.reply_text(f"Playing: {track_name} - {artist_name}...")

                try:
                    await pytgcalls.join_group_call(
                        chat_id,
                        audio=AudioPiped(audio_stream),
                        stream_type=StreamType().pulse_stream,
                    )

                except Exception as e:
                    await update.message.reply_text(f"Error playing audio: {e}")

            else:
                await update.message.reply_text("Could not find a playable audio stream for this song.")

        else:
            await update.message.reply_text("Song not found on Spotify.")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")


# Function to stop playing audio
async def stop_song(update: Update, context: CallbackContext):
    """Stops the audio playback in the voice chat."""
    global pytgcalls
    chat_id = update.effective_chat.id

    try:
        await pytgcalls.leave_group_call(chat_id)
        await update.message.reply_text("Stopped playing audio.")
    except Exception as e:
        await update.message.reply_text(f"Error stopping audio: {e}")


# Function to handle errors
async def error_handler(update: Update, context: CallbackContext):
    """Logs errors caused by updates."""
    print(f"Update {update} caused error {context.error}")


# Function to create voice chat
async def create_voice_chat(chat_id):
    """Creates a voice chat in the specified chat using the assistant account."""
    global assistant
    try:
        await assistant.create_group_call(chat_id)  # Pyrogram function
        print(f"Voice chat created in chat {chat_id}")
        return True
    except Exception as e:
        print(f"Error creating voice chat: {e}")
        return False


# Function to handle the join command
async def join_command(update: Update, context: CallbackContext) -> None:
    """Joins the voice chat (creating it if necessary) using the assistant."""
    chat_id = update.effective_chat.id

    try:
        created = await create_voice_chat(chat_id)

        if created:
            await update.message.reply_text("Created and joined voice chat (if it didn't exist).")
        else:
            await update.message.reply_text("Failed to create voice chat.")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")


# Main function to set up and run the bot
async def main() -> None:
    """Sets up and runs the Telegram bot."""
    global bot, assistant, pytgcalls

    # Initialize Pyrogram clients
    bot = Client("music_bot", bot_token=TELEGRAM_TOKEN)
    assistant = Client(
        "assistant", api_id=ASSISTANT_API_ID, api_hash=ASSISTANT_API_HASH, session_string=ASSISTANT_SESSION_STRING
    )
    await bot.start()
    await assistant.start()

    # Initialize PyTgCalls
    pytgcalls = PyTgCalls(bot)  # Use the BOT client for pytgcalls
    await pytgcalls.start()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("play", play_song,  pass_args=True, run_async=True))
    application.add_handler(CommandHandler("stop", stop_song, run_async=True))
    application.add_handler(CommandHandler("join", join_command, run_async=True))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    await application.start_polling()

    # Run the bot until the user presses Ctrl-C
    await application.idle()

    # Stop the clients
    await bot.stop()
    await assistant.stop()

if __name__ == "__main__":
    asyncio.run(main())
