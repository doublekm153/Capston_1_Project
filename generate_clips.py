import os
from datetime import timedelta
from video_keyword_search import search_keyword  
from cut_video import cut_video  
video_path = "path/to/your/video.mp4"
output_directory = "path/to/output/directory"
keyword = "your_keyword" 
video_text = "video_text.txt"

timestamps = search_keyword(keyword, video_text)

for i, timestamp in enumerate(timestamps):
    output_path = os.path.join(output_directory, f"video_clip_{i}.mp4")
    start_timestamp = timestamp
    end_timestamp = timestamp + timedelta(seconds=5)  
    cut_video(video_path, start_timestamp, end_timestamp, output_path)
