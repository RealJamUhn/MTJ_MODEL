def convert_bible_to_numbers(file_path):
    """
    텍스트 파일을 읽어 각 문자의 유니코드 값을 0~9 사이의 숫자로 변환합니다.
    """
    number_array = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()
        
        for char in text_data:
            unicode_val = ord(char)
            scaled_val = unicode_val % 10
            number_array.append(scaled_val)
            
    return number_array

def save_numbers_to_file(numbers, output_file_path):
    """
    숫자 배열을 텍스트 파일로 저장합니다.
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        # 리스트 안의 정수들을 문자열로 변환한 뒤, 공백 없이 하나로 이어 붙입니다.
        string_data = "".join(map(str, numbers))
        file.write(string_data)
        
# --- 실행 및 저장 예시 ---
input_file_name = 'bible.txt'        # 원본 성경 텍스트 파일명
output_file_name = 'number_output.txt' # 새로 저장될 숫자 텍스트 파일명

try:
    # 1. 숫자 변환 실행
    print("데이터 변환을 시작합니다...")
    bible_numbers = convert_bible_to_numbers(input_file_name)
    
    print(f"총 추출된 숫자 개수: {len(bible_numbers):,}개")
    
    # 2. 파일로 저장 실행
    print(f"'{output_file_name}' 파일에 결과를 저장하는 중...")
    save_numbers_to_file(bible_numbers, output_file_name)
    
    print("모든 작업이 성공적으로 완료되었습니다!")
    
except FileNotFoundError:
    print(f"오류: '{input_file_name}' 파일을 찾을 수 없습니다. 원본 파일이 같은 폴더에 있는지 확인해 주세요.")