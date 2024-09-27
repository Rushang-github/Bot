
# MiniTake - YouTube Audio Downloader Bot

**MiniTake** is a Telegram bot that allows users to download the audio from any YouTube video in just a few seconds. It's built using Python and utilizes `yt-dlp` for extracting audio.

## Features

- Download audio from YouTube by sending the video link.
- Automatically sends the downloaded MP3 file back to the user.
- Deletes the downloaded file after sending it to avoid storage issues.
- Provides real-time updates during the download and upload process.

## Requirements

To run the bot, you will need:

- Python 3.x
- The following Python libraries:
  - `telebot`
  - `yt-dlp`
  - `os`

You can install the required libraries using the following command:

```bash
pip install pyTelegramBotAPI yt-dlp
```

## Usage

1. Start the bot on Telegram by sending the `/start` command.
2. Send a YouTube video link to the bot, and it will download the audio for you.
3. The bot sends you the MP3 file once the download is complete.

## Example

1. `/start`: Welcomes the user to MiniTake.
2. Send a YouTube link: The bot will respond with "Downloading the music..." and then deliver the MP3 file.
