from google.oauth2 import service_account
from google.oauth2 import service_account
import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from google.cloud.speech_v1p1beta1 import enums
# 서비스 계정 키의 경로를 입력하세요.
key_path = "C:/Users/user/Desktop/graduate-388812-57af2b042054.json"

credentials = service_account.Credentials.from_service_account_file(key_path)
client = speech.SpeechClient(credentials=credentials)

import os
from google.cloud import speech_v1p1beta1 as speech

def transcribe_timestampped(wav_file, output_text_file):
    client = speech.SpeechClient()

    with open(wav_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR',
        enable_word_time_offsets=True
    )

    response = client.recognize(config, audio)

    timestamped_transcript = []

    with open(output_text_file, 'w', encoding='utf-8') as f:
        for result in response.results:
            alternative = result.alternatives[0]
            print('Transcript: {}'.format(alternative.transcript))
            print('Confidence: {}\n'.format(alternative.confidence))

            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time.seconds + word_info.start_time.nanos * 1e-9
                end_time = word_info.end_time.seconds + word_info.end_time.nanos * 1e-9
                timestamped_transcript.append((word, start_time, end_time))
                f.write('Word: {}, start_time: {}, end_time: {}\n'.format(word, start_time, end_time))

    return timestamped_transcript

input_wav_directory = 'D:\\video-summarization-master\\videos\\time_wav'
output_text_directory = 'D:\\video-summarization-master\\videos\\time_text'

for wav_filename in os.listdir(input_wav_directory):
    if wav_filename.endswith('.wav'):
        wav_file_path = os.path.join(input_wav_directory, wav_filename)
        output_filename = os.path.splitext(wav_filename)[0] + '.txt'
        output_path = os.path.join(output_text_directory, output_filename)
        timestamped_transcript = transcribe_timestampped(wav_file_path, output_path)
