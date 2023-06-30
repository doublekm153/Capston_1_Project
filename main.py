"""
from flask import Flask, render_template, url_for, request, redirect
import video_keyword_search
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files["video"]

        video_folder = "D:/video-summarization-master/videos/ffmpeg_data/"
        if not os.path.isdir(video_folder):
            os.makedirs(video_folder)

        video_path = os.path.join(video_folder, video_file.filename)
        video_file.save(video_path)

        text_folder = "D:/video-summarization-master/videos/ffmpeg_text/"
        text_file_path = os.path.join(text_folder, os.path.splitext(video_file.filename)[0] + ".txt")

        keyword = request.form["keyword"]
        result = video_keyword_search.search_text_file(text_file_path, keyword)
        
        return render_template('search_result.html', video_path=video_path, result=result)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
기존 키워드입력 -> 해당 문장 출력
"""

"""
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import video_keyword_search
from video_keyword_search import search_keyword_in_text_file, create_screenshot

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files["video"]

        video_folder = "D:/video-summarization-master/videos/time_data/"
        if not os.path.isdir(video_folder):
            os.makedirs(video_folder)

        video_path = os.path.join(video_folder, video_file.filename)
        video_file.save(video_path)

        text_folder = "D:/video-summarization-master/videos/text_2/"
        text_file_path = os.path.join(text_folder, os.path.splitext(video_file.filename)[0] + ".txt")

        keyword = request.form["keyword"]
        result_line = search_keyword_in_text_file(text_file_path, keyword)

        if result_line is not None:
            screenshot_folder = "static/screenshots"
            if not os.path.exists(screenshot_folder):
                os.mkdir(screenshot_folder)

            screenshot_name = f"{secure_filename(video_file.filename)}_{result_line}.png"
            screenshot_path = os.path.join(screenshot_folder, screenshot_name)
            create_screenshot(video_path, result_line, screenshot_path)

            return render_template('search_result.html', screenshot_path=screenshot_path)
        else:
            return render_template('search_result.html', message="해당 키워드를 찾을 수 없습니다.")
    
    return render_template('index.html')

@app.route('/screenshots/<filename>')
def uploaded_file(filename):
    return send_from_directory('screenshots', filename)

if __name__ == '__main__':
    app.run(debug=True)
키워드 입력->static에 이미지 추출
"""

from flask import Flask, render_template, request, send_from_directory
import os
from video_keyword_search import generate_clips_from_keyword
from werkzeug.utils import secure_filename
import glob

app = Flask(__name__)
app.config["VIDEO_UPLOADS"] = "static/video"



def get_video_clips():
    clips_folder = os.path.join('static', 'result')
    clip_files = glob.glob(os.path.join(clips_folder, 'news_onair_4124_clip*.mp4'))
    relative_clip_files = [os.path.join('/static', 'result', os.path.basename(clip)) for clip in clip_files]
    return relative_clip_files

@app.route('/')
def index():
    clips = get_video_clips()
    return render_template("index.html", clips=clips)

@app.route('/process_video', methods=["POST"])
def process_video():
    if request.method == "POST":
        if request.files:
            video_file = request.files["video"]
            video_abs_path = os.path.join(app.config["VIDEO_UPLOADS"], video_file.filename)
            video_file.save(video_abs_path)
            
            keyword = request.form["keyword"]
            #txt_abs_path = "D:/video-summarization-master/videos/ssk_text"
            txt_abs_path = os.path.join("D:/video-summarization-master/videos/ssk_text", f"{video_file.filename.split('.')[0]}.txt")
            output_clips = generate_clips_from_keyword(video_abs_path, txt_abs_path, keyword) or []

            clips = []
            if output_clips:
                clips = [clip.replace('"', '') for clip in output_clips]
                return render_template("search_result.html", clips=clips)
            else:
                return render_template("search_result.html")

if __name__ == "__main__":
    app.run(debug=True)
