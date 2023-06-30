def search_keyword_in_text_file(text_file, keyword):
    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    keyword_occurrences = []
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            keyword_occurrences.append(i)
    
    # 발견된 키워드의 첫 번째 줄 번호 반환
    if keyword_occurrences:
        return keyword_occurrences[0]  # 첫 번째 발생 이벤트로 예시
    else:
        return None

text_file = "D:\\video-summarization-master\\videos\\text_2\\example.txt"  # 실제 텍스트 파일로 변경하세요.
keyword = "sample keyword"
found_line_number = search_keyword_in_text_file(text_file, keyword)

if found_line_number is not None:
    print(f"Keyword '{keyword}' found at line {found_line_number+1}.")
else:
    print(f"Keyword '{keyword}' not found.")
