def convert_bible_to_numbers(file_path):
    """
    텍스트 파일을 읽어 각 문자의 유니코드 값을 0~9 사이의 숫자로 변환합니다.
    """
    number_array = []
    
    # 1. 텍스트 읽기
    # 영문 성경이라도 특수기호 처리를 위해 'utf-8' 인코딩을 명시하는 것이 안전합니다.
    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()
        
        # 2 & 3. 유니코드 변환 및 0~9 스케일링
        for char in text_data:
            # (선택 사항) 띄어쓰기나 줄바꿈 같은 공백 문자를 제외하고 싶다면 아래 코드를 활성화하세요.
            # if char.isspace(): 
            #     continue
                
            unicode_val = ord(char)         # 문자를 유니코드(아스키) 정수로 변환
            scaled_val = unicode_val % 10   # 10으로 나눈 나머지 계산 (0~9)
            
            number_array.append(scaled_val)
            
    return number_array

# --- 실행 예시 ---
# 'english_bible.txt' 파일이 같은 폴더에 있다고 가정합니다.
file_name = 'english_bible.txt'

try:
    bible_numbers = convert_bible_to_numbers(file_name)
    
    # 결과 확인 (전체 데이터 개수 및 처음 20개 숫자 출력)
    print(f"총 추출된 숫자 개수: {len(bible_numbers):,}개")
    print(f"처음 20개 숫자 샘플: {bible_numbers[:20]}")
    
except FileNotFoundError:
    print(f"오류: '{file_name}' 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")