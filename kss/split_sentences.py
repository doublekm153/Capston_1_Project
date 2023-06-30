import os
import kss

input_folder_path = "D:\\video-summarization-master\\videos\\time_text"
output_folder_path = "D:\\video-summarization-master\\videos\\ssk_text"

# 입력 폴더 내 모든 파일 확인
for filename in os.listdir(input_folder_path):
    # .txt 파일인 경우만 처리
    if filename.endswith(".txt"):
        input_file_path = os.path.join(input_folder_path, filename)
        output_file_path = os.path.join(output_folder_path, filename)

        # 워드별 구분된 입력 파일을 문장별 구분된 출력 파일로 변환
        with open(input_file_path, "r", encoding="utf-8") as input_file, open(output_file_path, "w", encoding="utf-8") as output_file:
            content = input_file.read()
            sentences = kss.split_sentences(content)
            
            for sentence in sentences:
                output_file.write(sentence + '\n')


