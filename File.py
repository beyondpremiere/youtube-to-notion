import os
import youtube_dl
from moviepy.editor import VideoFileClip
import whisper
from notion_client import Client


# Function to download video from YouTube
def download_video(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'video.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'video.mp3'


# Function to transcribe audio using Whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path)
    return result['text']


# Function to add transcription to Notion
def add_to_notion(notion_token, database_id, title, content):
    notion = Client(auth=notion_token)
    new_page = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]
    }
    notion.pages.create(**new_page)


def main():
    video_url = input("Enter the YouTube video URL: ")

    notion_token = 'SECRET KEY'
    database_id = 'SUPER EASY TO GET'

    # Download the video
    audio_file = download_video(video_url)

    # Transcribe the audio
    transcription = transcribe_audio(audio_file)

    # Add transcription to Notion
    title = "Transcription of YouTube Video"
    add_to_notion(notion_token, database_id, title, transcription)

    print("Transcription added to Notion successfully!")


if __name__ == "__main__":
    main()

