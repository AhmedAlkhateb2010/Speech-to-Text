import os
from pydub import AudioSegment
from openpyxl import Workbook
from langdetect import detect
import time
import speech_recognition as sr
from pydub.utils import which

# Set the ffmpeg path explicitly for pydub
AudioSegment.ffmpeg = r'C:\Users\Msi\Downloads\ffmpeg-2025-01-15-git-4f3c9f2f03-full_build\ffmpeg-2025-01-15-git-4f3c9f2f03-full_build\bin\ffmpeg.exe'


def process_audio_file(file_path):
    """
    Process an audio file: transcribe content, detect language, and calculate timestamp in minutes.
    """
    # Load the audio file
    try:
        audio = AudioSegment.from_file(file_path)
    except Exception as e:
        raise ValueError(f"Error loading audio file: {str(e)}")

    # Transcribe the audio file
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)  # Transcription logic
    except Exception as e:
        raise ValueError(f"Error transcribing audio file: {str(e)}")

    # Detect the language of the transcription
    try:
        language = detect(transcription)
    except Exception as e:
        raise ValueError(f"Error detecting language: {str(e)}")

    # Calculate duration in minutes
    duration_minutes = round(audio.duration_seconds / 60, 2)

    return {
        "transcription": transcription,
        "language": language,
        "duration_minutes": duration_minutes,
    }


def process_audio_to_excel(file_path, output_folder):
    """
    Process an audio file and save the transcription, language, and timestamps in an Excel file.
    """
    # Process the audio file
    try:
        audio_data = process_audio_file(file_path)
    except Exception as e:
        raise ValueError(f"Error processing audio file: {str(e)}")

    # Create an Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Transcription"
    ws.append(["Content", "Language", "Timestamp (min)"])

    # Add data to the Excel sheet
    ws.append([
        audio_data["transcription"],
        audio_data["language"],
        audio_data["duration_minutes"],
    ])

    # Save the Excel file
    timestamp = int(time.time())
    file_name = f"transcription_{timestamp}.xlsx"
    output_path = os.path.join(output_folder, file_name)

    try:
        wb.save(output_path)
    except Exception as e:
        raise ValueError(f"Error saving Excel file: {str(e)}")

    return output_path
