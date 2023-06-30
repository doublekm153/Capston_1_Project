"""
import os
import re

def search_text_file(text_filepath, keyword):
    matched_lines = []

    with open(text_filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if keyword.lower() in line.lower():
            matched_lines.append(line.strip())

    if not matched_lines:
        return ["죄송합니다. 해당 영상에는 사용자가 기입한 키워드가 없습니다."]
    else:
        return matched_lines
기존 키워드입력 -> 해당 문장 출력
"""


"""
import os
import re
import subprocess
from moviepy.editor import VideoFileClip
from typing import List, Tuple

def keyword_search(text_filepath, keyword):
    return search_text_file(text_filepath, keyword)

def search_text_file(text_filepath, keyword):
    matched_lines = []

    with open(text_filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if keyword.lower() in line.lower():
            matched_lines.append(line.strip())

    if not matched_lines:
        return ["죄송합니다. 해당 영상에는 사용자가 기입한 키워드가 없습니다."]
    else:
        return matched_lines
        
def extract_audio(video):
    return video.audio
    
def extract_video_clip(video_path, start_time, end_time, output_path):
    video = VideoFileClip(video_path)

    # Extract audio
    audio = extract_audio(video)

    # Cut video clip
    video_clip = video.subclip(start_time, end_time)

    # Add audio back
    video_clip.audio = audio

    # Save output
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

def search_keyword_in_text_file(text_file, keyword):
    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    keyword_occurrences = []
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            keyword_occurrences.append(i)

    if keyword_occurrences:
        return keyword_occurrences[0]  # 첫 번째 발생 이벤트로 예시
    else:
        return None

def create_screenshot(video_filepath, timestamp, output_image_filepath):
    command = f"ffmpeg -i \"{video_filepath}\" -ss {timestamp} -vframes 1 \"{output_image_filepath}\""
    subprocess.call(command, shell=True)

def search_video_and_create_screenshot(text_filepath, keyword, video_filepath, output_image_filepath):
    matched_lines = keyword_search(text_filepath, keyword)
    if len(matched_lines) > 0 and matched_lines[0] != "죄송합니다. 해당 영상에는 사용자가 기입한 키워드가 없습니다.":
        time_parts = matched_lines[0].split()[0].split(':')
        timestamp = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])
        create_screenshot(video_filepath, timestamp, output_image_filepath)
        return "스크린샷이 생성되었습니다: {}".format(output_image_filepath)

    return matched_lines

def find_sentences_with_keywords(sentences: List[str], keyword: str) -> List[Tuple[str, int]]:
    result = []
    for idx, sentence in enumerate(sentences):
        if keyword.lower() in sentence.lower():
            result.append((sentence, idx))
    return result
"""

import os
import subprocess
from moviepy.editor import *

import shutil

def clear_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def save_clip_with_new_name(ffmpeg_command):
    cmd_parts = ffmpeg_command.split()
    output_filename = cmd_parts[-1]

    if os.path.exists(output_filename):
        split_name = os.path.splitext(output_filename)
        i = 1
        while os.path.exists(output_filename):
            output_filename = f"{split_name[0]}_{i}{split_name[1]}"
            i += 1

    cmd_parts[-1] = output_filename
    new_ffmpeg_command = " ".join(cmd_parts)
    subprocess.run(new_ffmpeg_command, shell=True, text=True, encoding='utf-8')

    return output_filename

def extract_sentences_with_keyword(txt_path, keyword):
    keyword_sentences = []

    with open(txt_path, "r", encoding='utf-8') as file:
        for line in file:
            if keyword.lower() in line.lower():
                keyword_sentences.append(line)

    return keyword_sentences


def get_start_end_times(line):
    start_time_str, end_time_str = line.split(",")[1:]

    start_time = float(start_time_str.split("시작 시간:")[-1].replace("초","").strip())
    end_time = float(end_time_str.split("종료 시간:")[-1].replace("초","").strip())

    return start_time, end_time


def generate_clips_from_keyword(video_path, txt_path, keyword):
    sentences = extract_sentences_with_keyword(txt_path, keyword)
    output_clips = []

    clear_directory('static/result')

    for sentence in sentences:
        start_time, end_time = get_start_end_times(sentence)
        if start_time is not None and end_time is not None:
            output_file = f"static/result/{os.path.splitext(os.path.basename(video_path))[0]}_clip{len(output_clips)}.mp4"
            command = f"ffmpeg -i \"{video_path}\" -ss {start_time} -to {end_time} -c copy \"{output_file}\""

            new_output_file = save_clip_with_new_name(command)
            output_clips.append(new_output_file)

            """
            process = subprocess.run(command, shell=True, text=True, encoding='utf-8')
            if process.returncode == 0:
                output_clips.append(output_file)
            else:
                print(f"Error while generating clip {len(output_clips)}: {process.stderr}")
            """

    return output_clips


def create_clips(txt_file_path, video_file_path, keyword):
    clips = []

    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if keyword in line:
            start, end = get_start_end_times(line)
            clip = VideoFileClip(video_file_path).subclip(start, end)
            clips.append(clip)

    return clips
