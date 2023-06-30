import kss
import os

input_file_path = "D:\\video-summarization-master\\videos\\time_text\\your_input_file.txt"
output_file_path = "D:\\video-summarization-master\\videos\\ssk_text\\output_sentence_timestamps.txt"

with open(input_file_path, "r", encoding="utf-8") as input_file, open(output_file_path, "w", encoding="utf-8") as output_file:
    lines = input_file.readlines()

    s = ""
    for line in lines:
        line = line.strip().split(" ", 1)
        time, text = line[0], line[1]
        s += f"{text}({time}) "

    sentence_list = []
    for sent in kss.split_sentences(s):
        words = sent.split()
        sentence_list.append((words[0][-9:-1], words[-1][-9:-1], " ".join([word[:-10] for word in words])))

    for start_time, end_time, sentence in sentence_list:
        output_file.write(f"{start_time}~{end_time} {sentence}\n")


