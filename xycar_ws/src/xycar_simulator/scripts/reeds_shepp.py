import math

# ================================================
# 🛣️ Reeds-Shepp 스타일 경로 생성 함수 (S자 보간 기반)
# - 차량의 시작점과 목표점을 기반으로 부드러운 경로 생성
# - 실제 Reeds-Shepp 알고리즘이 아닌, sin 함수를 활용한 S자 경로 보간
# ================================================
def reeds_shepp_path(start, goal, turning_radius=30.0):
    x0, y0, yaw0 = start
    x1, y1, yaw1 = goal

    path = []

    # 전체 포인트 수 (전반부: 커브, 후반부: yaw 정렬)
    num_points = 300
    s_curve_ratio = 0.70  # 70%는 커브, 30%는 yaw 정렬용 직선

    # ============================================
    # 📈 S자 형태로 경로를 보간하여 생성
    # - X축은 직선 보간
    # - Y축은 sin 곡선 추가하여 부드러운 곡선형태 구성
    # ============================================

    for i in range(int(num_points * s_curve_ratio)):
        t = i / (num_points * s_curve_ratio - 1)

        # X: 직선 보간
        x = x0 + (x1 - x0) * t

        # Y: sin을 활용한 S자 곡선
        amplitude = 75
        frequency = 2 * math.pi
        y = y0 + (y1 - y0) * t + amplitude * math.sin(frequency * t)

        path.append((x, y, 0))  # yaw는 나중에 계산


    # ============================================
    # 🔁 각 지점 사이의 yaw(방향) 계산
    # - 두 점 사이의 atan2로 방향 구함
    # - 마지막 점은 목표 yaw로 설정
    # ============================================

    x_last, y_last, _ = path[-1]

    align_steps = num_points - len(path)
    for i in range(1, align_steps + 1):
        t = i / align_steps
        x = x_last + (x1 - x_last) * t
        y = y_last + (y1 - y_last) * t
        path.append((x, y, 0))  # yaw 이후에 처리

    # 각도 계산
    smoothed_path = []
    for i in range(len(path) - 1):
        x0, y0, _ = path[i]
        x1, y1, _ = path[i + 1]
        dx = x1 - x0
        dy = y1 - y0
        yaw = math.atan2(dy, dx)
        smoothed_path.append((x0, y0, yaw))

    # 마지막 점: 정확한 goal yaw 반영
    smoothed_path.append((x1, y1, math.radians(yaw1)))

    return smoothed_path
# ============================================
'''
🧭 요약

sin 곡선을 활용한 S자 보간 경로 생성

x는 직선, y는 sin을 더해 커브 생성

yaw는 두 점 사이의 방향으로 계산하여 부드러운 회전 유지

마지막 도착지점은 목표 각도로 맞춰서 정렬
'''