import os
import io
from google.cloud import speech_v1p1beta1 as speech
from moviepy.editor import *
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/user/Desktop/graduate-388812-57af2b042054.json"

def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

    
def transcribe_video(audio_path):
    client = speech.SpeechClient()

    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)
    return response


if __name__ == "__main__":
    video_dir = "D:/video-summarization-master/videos/new/data"
    audio_dir = "D:/video-summarization-master/videos/new/wav"
    text_dir = "D:/video-summarization-master/videos/new/text"

    video_filenames = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]

    for video_filename in video_filenames:
        video_path = os.path.join(video_dir, video_filename)
        
        audio_filename = f"{os.path.splitext(video_filename)[0]}.wav"
        audio_path = os.path.join(audio_dir, audio_filename)
        
        extract_audio_from_video(video_path, audio_path)
        
        response = transcribe_video(audio_path)

        text_filename = f"{os.path.splitext(video_filename)[0]}.txt"
        text_path = os.path.join(text_dir, text_filename)

        with open(text_path, "w") as text_file:
            for result in response.results:
                text_file.write(result.alternatives[0].transcript)
                text_file.write("\n")
                text_file.write("Confidence: {}\n".format(result.alternatives[0].confidence))

                text_file.write("\n")

                for word in result.alternatives[0].words:
                    text_file.write("Word: {}\n".format(word.word))
                    text_file.write("Start time: {} seconds\n".format(word.start_time.total_seconds()))
                    text_file.write("End time: {} seconds\n".format(word.end_time.total_seconds()))

                    text_file.write("\n")
