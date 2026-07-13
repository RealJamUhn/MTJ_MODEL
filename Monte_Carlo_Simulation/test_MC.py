import numpy as np
import matplotlib.pyplot as plt
import time

def analyze_randomness_optimized(file_path):
    print(f"'{file_path}' 파일을 읽는 중입니다...")
    start_time = time.time()
    
    # ==========================================
    # [1단계] 초고속 데이터 불러오기 (최적화 핵심)
    # ==========================================
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read().strip()
            
        print("데이터를 고속 배열로 변환 중...")
        # 1. 거대한 문자열을 ASCII 바이트 배열로 한 번에 변환
        byte_data = np.frombuffer(data.encode('ascii', errors='ignore'), dtype=np.uint8)
        
        # 2. ASCII 코드 기준 숫자 '0'(48) ~ '9'(57)만 걸러낸 뒤 정수로 변환
        numbers = byte_data[(byte_data >= 48) & (byte_data <= 57)] - 48
        
    except FileNotFoundError:
        print("오류: 파일을 찾을 수 없습니다. 파일 이름과 위치를 확인해주세요.")
        return

    total_digits = len(numbers)
    print(f"✅ 데이터 로드 완료! (총 {total_digits:,}개 / 소요 시간: {time.time() - start_time:.2f}초)")

    # ==========================================
    # [2단계] 빈도수 분석 및 몬테카를로 시뮬레이션
    # ==========================================
    # 0~9 빈도수 비율 계산
    counts = np.bincount(numbers, minlength=10)
    percentages = (counts / total_digits) * 100

    # 몬테카를로 파이(Pi) 추정을 위해 데이터 4개씩 묶기
    chunk_size = 4
    max_len = (total_digits // chunk_size) * chunk_size
    reshaped_numbers = numbers[:max_len].reshape(-1, chunk_size)
    
    # 빠른 내적 연산을 통해 소수점(0.xxxx) 변환
    decimals = np.dot(reshaped_numbers, [0.1, 0.01, 0.001, 0.0001])
    
    # 좌표 나누기 (x, y)
    half_point = len(decimals) // 2
    x_coords = decimals[:half_point]
    y_coords = decimals[half_point:half_point*2]
    
    # 원 안의 점 판별 (x^2 + y^2 <= 1)
    distances_squared = x_coords**2 + y_coords**2
    inside_circle = distances_squared <= 1.0
    inside_count = np.sum(inside_circle)
    total_points = len(x_coords)
    
    estimated_pi = (inside_count / total_points) * 4
    print(f"\n[결과 요약]")
    print(f"추정된 원주율(Pi): {estimated_pi:.6f} (실제: 3.141592...)")

    # ==========================================
    # [3단계] 시각화
    # ==========================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # 그래프 1: 빈도수 막대 그래프
    ax1.bar(range(10), percentages, color='skyblue', edgecolor='black')
    ax1.axhline(y=10.0, color='red', linestyle='--', label='10% (Perfect Uniformity)')
    ax1.set_title('Digit Distribution (0-9)')
    ax1.set_xlabel('Digit')
    ax1.set_ylabel('Percentage (%)')
    ax1.set_xticks(range(10))
    for i, p in enumerate(percentages):
        ax1.text(i, p + 0.1, f"{p:.1f}%", ha='center', fontsize=9)
    ax1.legend()

    # 그래프 2: 몬테카를로 산점도 (그리기 속도를 위해 1만개 점만 샘플링 표시)
    plot_limit = min(total_points, 10000)
    x_plot = x_coords[:plot_limit]
    y_plot = y_coords[:plot_limit]
    inside_plot = inside_circle[:plot_limit]

    ax2.scatter(x_plot[inside_plot], y_plot[inside_plot], c='blue', s=1, alpha=0.5, label='Inside Circle')
    ax2.scatter(x_plot[~inside_plot], y_plot[~inside_plot], c='red', s=1, alpha=0.5, label='Outside')
    ax2.add_patch(plt.Circle((0, 0), 1, color='black', fill=False, linewidth=2))
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.set_title(f'Monte Carlo Pi Estimation (Pi $\\approx$ {estimated_pi:.4f})')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

# 실행 부분 (만드신 파일명으로 변경하여 실행하세요)
analyze_randomness_optimized('number_output.txt')