import pygame
import math
import random

passed_path = []  # 차량이 지나간 경로를 저장하는 리스트

# ================================================
# 🚗 차량 스폰 함수
# - 주어진 위치 기준으로 차량을 랜덤한 출발 위치에 생성하고,
#   목표를 향한 방향 + 약간의 랜덤 각도 오차를 부여
# ================================================
def spawn_car(target_pos):
    # 차량 스폰 가능한 후보 위치들
    spawn_candidates = [(100, 450), (200, 500), (300, 400)]
    
    # 후보 중 하나를 무작위 선택
    car_pos = list(random.choice(spawn_candidates))

    # 선택된 위치에서 목표지점까지의 방향 계산
    dx = target_pos[0] - car_pos[0]
    dy = target_pos[1] - car_pos[1]
    base_angle = math.degrees(math.atan2(dy, dx))

    # 방향에 ±30도 오차를 더해 현실적인 출발 방향으로 설정
    car_angle = base_angle + random.uniform(-30, 30)

    return car_pos, car_angle


# ================================================
# 🖼️ 차량 이미지 회전 후 화면에 그리기
# - 주어진 위치와 각도에 따라 차량 이미지를 회전시켜 렌더링
# ================================================
def draw_rotated_car(screen, car_img, car_pos, car_angle):
    rotated = pygame.transform.rotate(car_img, -car_angle)  # 각도는 반시계방향이므로 음수
    rect = rotated.get_rect(center=(car_pos[0], car_pos[1]))  # 회전 중심 설정
    screen.blit(rotated, rect)  # 화면에 그리기


# ================================================
# 🔍 차량에 가장 가까운 경로 점 찾기
# - 차량 현재 위치와 경로상의 점들 간 거리 계산하여 가장 가까운 점 인덱스 반환
# ================================================
def find_nearest_path_index(car_pos, path):
    min_dist = float('inf')
    min_index = 0
    for i, (x, y, _) in enumerate(path):
        dist = math.hypot(car_pos[0] - x, car_pos[1] - y)
        if dist < min_dist:
            min_dist = dist
            min_index = i
    return min_index


# ================================================
# 🚗 차량을 경로를 따라 이동시키는 함수
# - 현재 각도와 경로 방향을 비교해 회전 보정
# - 일정 각도 차이 이내면 전진, 아니면 회전만 수행
# ================================================
def move_car_along_path(car_pos, car_angle, path, _, passed_path):
    # 현재 차량 위치에서 가장 가까운 경로 인덱스 찾기
    path_index = find_nearest_path_index(car_pos, path)

    # 경로 마지막에 도달하면 정지
    if path_index >= len(path) - 1:
        return car_pos, car_angle, path_index

    # 타겟 경로 점 정보
    target_x, target_y, target_yaw = path[path_index]

    # 위치 차이 계산
    dx = target_x - car_pos[0]
    dy = target_y - car_pos[1]
    distance = math.hypot(dx, dy)

    # 현재 각도 (도 → 라디안)
    car_angle_rad = math.radians(car_angle)

    # 목표 yaw와 현재 각도 차이 계산 ([-π, π] 범위 유지)
    diff_angle = target_yaw - car_angle_rad
    diff_angle = (diff_angle + math.pi) % (2 * math.pi) - math.pi

    # 회전 보정값 적용
    turn_speed = 0.15  # 회전 민감도
    car_angle_rad += turn_speed * diff_angle
    car_angle = math.degrees(car_angle_rad)

    # 일정 각도 차이 이내일 때만 전진
    angle_threshold = math.radians(30)  # 최대 허용 각도 차이
    speed = 1.5  # 전진 속도

    if abs(diff_angle) < angle_threshold:
        # 전진
        move_x = speed * math.cos(car_angle_rad)
        move_y = speed * math.sin(car_angle_rad)
        car_pos[0] += move_x
        car_pos[1] += move_y

        passed_path.append((car_pos[0], car_pos[1])) # 차량 실제 이동 경로 추가
    else:
        # 각도만 보정하고 위치는 그대로
        pass

    return car_pos, car_angle, path_index, passed_path

#======================================

'''
🔍 요약 정리

spawn_car: 차량을 랜덤 위치에 스폰하며, 목표지점 방향 + 약간의 각도 오차 부여

draw_rotated_car: 차량 이미지를 현재 위치/방향에 맞게 회전 렌더링

find_nearest_path_index: 현재 차량 위치 기준 가장 가까운 경로 점 탐색

move_car_along_path: 경로를 따라 자연스럽게 회전+전진

'''