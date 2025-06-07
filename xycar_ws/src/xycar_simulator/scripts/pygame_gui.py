import pygame
import sys
import math
import random
from reeds_shepp import reeds_shepp_path  # Reeds-Shepp 경로 생성 함수
from parking_sim import spawn_car, draw_rotated_car, move_car_along_path  # 차량 관련 함수들

def run_simulator():
    # Pygame 초기화
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("XYCAR Parking Simulator")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    # 색상 정의
    WHITE = (255, 255, 255)
    BLUE = (100, 149, 237)
    RED = (220, 80, 80)
    GREEN = (0, 200, 0)
    BLACK = (0, 0, 0)
    DARKBLUE = (80, 80, 220)
    BACKGROUND = (230, 245, 255)  # 하늘색 배경

    # 버튼 설정 (사각형)
    spawn_button = pygame.Rect(80, 550, 120, 40)
    planning_button = pygame.Rect(250, 550, 120, 40)
    tracking_button = pygame.Rect(420, 550, 120, 40)

    # 차량 이미지 불러오기 및 전처리
    car_img = pygame.image.load("src/xycar_simulator/scripts/assets/car_image.png").convert_alpha()
    car_img = pygame.transform.rotate(car_img, 180)  # 차량이 앞을 향하도록 180도 회전
    car_img = pygame.transform.smoothscale(car_img, (60, 30))  # 초기 크기 조절

    # 비율 유지 리사이징
    scale_width = 80
    scale_factor = scale_width / car_img.get_width()
    scale_height = int(car_img.get_height() * scale_factor)
    car_img = pygame.transform.smoothscale(car_img, (scale_width, scale_height))

    #########------------------------------------------###########

    # 초기 차량 위치 및 각도
    car_pos = [150.0, 500.0]
    car_angle = 45.0  # 출발 방향 (도)
    target_pos = [700.0, 100.0]  # 주차 타겟 위치 (중앙)
    target_angle = 270.0  # 목표 각도 (위쪽 방향)

    # 경로 및 상태 변수 초기화
    path = []
    path_index = 0
    moving = False  # 주행 중 여부

    # 이동 경로 저장 리스트
    passed_path = []

    running = True
    while running:
        screen.fill(BACKGROUND)  # 배경 초기화

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 차량 재스폰
                if spawn_button.collidepoint(event.pos):
                    car_pos[:], car_angle = spawn_car(target_pos)
                    path = []
                    path_index = 0
                    moving = False

                    # 이동 경로 저장 리스트 (경로 초기화)
                    passed_path = []

                # 경로 생성
                elif planning_button.collidepoint(event.pos):
                    start = [car_pos[0], car_pos[1], math.radians(car_angle)]

                    # 목표 위치 조정 (박스 앞쪽)
                    goal_yaw_deg = 270
                    goal_yaw = math.radians(goal_yaw_deg)

                    offset = 5  # 박스 arrive loacation control
                    goal_x = target_pos[0] + offset * math.cos(goal_yaw)
                    goal_y = target_pos[1]
                    goal = [goal_x, goal_y, goal_yaw]

                    # Reeds-Shepp 경로 생성
                    path = reeds_shepp_path(start, goal)

                    if path:
                        last_yaw = path[-2][2]
                        x1, y1, _ = path[-1]
                        path[-1] = (x1, y1, last_yaw)  # 마지막 방향 정리
                        path_index = 0
                        # 이동 경로 저장 리스트 (경로 초기화)
                        passed_path = []

                # 경로 따라 이동 시작
                elif tracking_button.collidepoint(event.pos):
                    moving = True

        # 주차 타겟 박스 그리기
        pygame.draw.rect(screen, RED, (target_pos[0] - 40, target_pos[1] - 25, 80, 50), 3)

        # 경로 시각화
        if path:
            target_angle = math.degrees(path[-1][2])  # 목표 방향 업데이트
            for i in range(len(path) - 1):
                pygame.draw.line(screen, BLUE, path[i][:2], path[i + 1][:2], 2)

        # 차량 이동
        if moving and path and path_index < len(path):
            car_pos, car_angle, path_index, passed_path = move_car_along_path(car_pos, car_angle, path, path_index, passed_path)


        # 이동 경로 그리기 (항상 그려지게 위치 이동)
        if len(passed_path) >= 2:
            for i in range(len(passed_path) - 1):
                pygame.draw.line(screen, GREEN, passed_path[i], passed_path[i + 1], 3)
                #print(f"Append point: {car_pos}, path_index={path_index}")


        # 차량 렌더링
        draw_rotated_car(screen, car_img, car_pos, car_angle)

        # 버튼 UI
        pygame.draw.rect(screen, DARKBLUE, spawn_button)
        pygame.draw.rect(screen, BLUE, planning_button)
        pygame.draw.rect(screen, RED, tracking_button)
        screen.blit(font.render("Spawn", True, WHITE), (spawn_button.x + 20, spawn_button.y + 5))
        screen.blit(font.render("Planning", True, WHITE), (planning_button.x + 10, planning_button.y + 5))
        screen.blit(font.render("Tracking", True, WHITE), (tracking_button.x + 10, tracking_button.y + 5))

        # 주차 성공 판정
        if moving:
            dx = car_pos[0] - target_pos[0]
            dy = car_pos[1] - target_pos[1]
            distance = math.hypot(dx, dy)

            angle_diff = abs((car_angle - target_angle + 180) % 360 - 180)

            print(f"[DEBUG] distance: {distance:.2f}, angle_diff: {angle_diff:.2f}, moving: {moving}")

            # 조건 만족 시 성공 메시지 출력
            if distance < 10.0 and angle_diff < 5.0:
                #screen.blit(font.render("주차 완료!", True, BLACK), (WIDTH // 2 - 80, 20))
                moving = False

        pygame.display.flip()
        clock.tick(60)  # 60 FPS 유지

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    run_simulator()
