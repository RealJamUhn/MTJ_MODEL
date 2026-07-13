import numpy as np
import matplotlib.pyplot as plt

def analyze_randomness(file_path):
    print(f"'{file_path}' 파일을 분석 중입니다...")
    
    # 1. 데이터 불러오기
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read().strip()
            # 문자열을 정수 리스트로 변환 (Numpy 배열로 처리하여 속도 향상)
            numbers = np.array([int(char) for char in data if char.isdigit()])
    except FileNotFoundError:
        print("오류: 파일을 찾을 수 없습니다.")
        return

    total_digits = len(numbers)
    print(f"총 분석 숫자 개수: {total_digits:,}개")

    # ==========================================
    # [1단계] 0~9 빈도수 분석 및 퍼센트 계산
    # ==========================================
    counts = np.bincount(numbers, minlength=10)
    percentages = (counts / total_digits) * 100

    print("\n[숫자별 출현 비율]")
    for i in range(10):
        print(f"숫자 {i}: {percentages[i]:.2f}%")

    # ==========================================
    # [2단계] 몬테카를로 시뮬레이션 (좌표 생성 및 원주율 추정)
    # ==========================================
    # 난수성을 높이기 위해 숫자 4개를 묶어 0.xxxx 형태의 소수로 만듭니다.
    # 예: [3, 8, 1, 0] -> 0.3810
    
    # 데이터를 4개씩 묶기 위해 4의 배수로 길이를 자릅니다.
    chunk_size = 4
    max_len = (total_digits // chunk_size) * chunk_size
    reshaped_numbers = numbers[:max_len].reshape(-1, chunk_size)
    
    # 각 행을 [0.1, 0.01, 0.001, 0.0001]과 내적하여 소수로 변환
    decimals = np.dot(reshaped_numbers, [0.1, 0.01, 0.001, 0.0001])
    
    # 만들어진 소수들을 x좌표와 y좌표 쌍으로 나눕니다.
    half_point = len(decimals) // 2
    x_coords = decimals[:half_point]
    y_coords = decimals[half_point:half_point*2]
    
    # 원점과의 거리 계산 (x^2 + y^2)
    distances_squared = x_coords**2 + y_coords**2
    
    # 거리가 1 이하인 점(원 안의 점) 판별
    inside_circle = distances_squared <= 1.0
    inside_count = np.sum(inside_circle)
    total_points = len(x_coords)
    
    # 몬테카를로 원주율 계산
    estimated_pi = (inside_count / total_points) * 4
    print(f"\n[몬테카를로 시뮬레이션 결과]")
    print(f"생성된 좌표 개수: {total_points:,}개")
    print(f"추정된 원주율(Pi): {estimated_pi:.6f} (실제 Pi: {np.pi:.6f})")

    # ==========================================
    # [3단계] 시각화 (그래프 그리기)
    # ==========================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # 그래프 1: 0~9 빈도수 막대 그래프
    ax1.bar(range(10), percentages, color='skyblue', edgecolor='black')
    ax1.axhline(y=10.0, color='red', linestyle='--', label='10% (Perfect Uniformity)')
    ax1.set_title('Distribution of Digits (0-9)')
    ax1.set_xlabel('Digit')
    ax1.set_ylabel('Percentage (%)')
    ax1.set_xticks(range(10))
    ax1.legend()
    
    # 막대 위에 퍼센트 텍스트 추가
    for i, p in enumerate(percentages):
        ax1.text(i, p + 0.2, f"{p:.1f}%", ha='center', fontsize=9)

    # 그래프 2: 몬테카를로 산점도 (데이터가 너무 많으면 렌더링이 느려지므로 최대 1만 개만 표시)
    plot_limit = min(total_points, 10000)
    x_plot = x_coords[:plot_limit]
    y_plot = y_coords[:plot_limit]
    inside_plot = inside_circle[:plot_limit]

    # 원 안의 점은 파란색, 밖의 점은 빨간색으로 표시
    ax2.scatter(x_plot[inside_plot], y_plot[inside_plot], c='blue', s=1, alpha=0.5, label='Inside Quarter Circle')
    ax2.scatter(x_plot[~inside_plot], y_plot[~inside_plot], c='red', s=1, alpha=0.5, label='Outside')
    
    # 기준이 되는 부채꼴 선 그리기
    circle_arc = plt.Circle((0, 0), 1, color='black', fill=False, linewidth=2)
    ax2.add_patch(circle_arc)
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.set_title(f'Monte Carlo Pi Estimation\nEstimated Pi: {estimated_pi:.4f}')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

# --- 실행 부분 ---
# 이전 단계에서 만든 파일 이름을 입력합니다.
analyze_randomness('number_output.txt')