import pygame
import sys
import math
import random
from reeds_shepp import reeds_shepp_path

# car simulator logic 모듈
from parking_sim import spawn_car, draw_rotated_car, move_car_along_path

def run_simulator():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("XYCAR Parking Simulator")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    # Colors
    WHITE = (255, 255, 255)
    BLUE = (100, 149, 237)
    RED = (220, 80, 80)
    GREEN = (0, 200, 0)
    BLACK = (0, 0, 0)
    DARKBLUE = (80, 80, 220)
    BACKGROUND = (230, 245, 255)  # 연한 하늘색 배경

    # Buttons
    spawn_button = pygame.Rect(80, 550, 120, 40)
    planning_button = pygame.Rect(250, 550, 120, 40)
    tracking_button = pygame.Rect(420, 550, 120, 40)

    # Car
    car_img = pygame.image.load("assets/car_image.png")
    car_img = pygame.image.load("assets/car_image.png").convert_alpha()

    # 180도 회전 (앞뒤 반전)
    car_img = pygame.transform.rotate(car_img, 180)

    # 크기 조절
    car_img = pygame.transform.smoothscale(car_img, (60, 30))

    # 비율 유지해서 리사이즈 (너비 기준)
    scale_width = 80
    scale_factor = scale_width / car_img.get_width()
    scale_height = int(car_img.get_height() * scale_factor)

    car_img = pygame.transform.smoothscale(car_img, (scale_width, scale_height))

    car_pos = [150.0, 500.0]
    car_angle = 45.0
    target_pos = [700.0, 100.0]
    target_angle = 270.0

    path = []
    path_index = 0
    moving = False

    running = True
    while running:
        screen.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if spawn_button.collidepoint(event.pos):
                    car_pos[:], car_angle = spawn_car(target_pos)
                    path = []
                    path_index = 0
                    moving = False

                elif planning_button.collidepoint(event.pos):
                    # 차량 출발 상태
                    start = [car_pos[0], car_pos[1], math.radians(car_angle)]

                    # 주차 목표 지점 = 박스 중심
                    goal_yaw = math.radians(270)
                    goal = [target_pos[0], target_pos[1], goal_yaw]

                    path = reeds_shepp_path(start, goal)
                    if path:
                        last_yaw = path[-2][2]  # 마지막에서 두 번째 점의 방향
                        x1, y1, _ = path[-1]
                        path[-1] = (x1, y1, last_yaw)
                    path_index = 0

                elif tracking_button.collidepoint(event.pos):
                    moving = True# ← driving 상태 활성화

        # Draw parking target
        pygame.draw.rect(screen, RED, (target_pos[0] - 40, target_pos[1] - 25, 80, 50), 3)

        # Draw path
        if path:
            target_angle = math.degrees(path[-1][2])  # 목표 방향을 경로의 마지막 방향으로!
            for i in range(len(path) - 1):
                pygame.draw.line(screen, BLUE, path[i][:2], path[i + 1][:2], 2)

        # Move car
        if moving and path and path_index < len(path):
            car_pos, car_angle, path_index = move_car_along_path(car_pos, car_angle, path, path_index)


        # Draw car
        draw_rotated_car(screen, car_img, car_pos, car_angle)

        # Draw buttons
        pygame.draw.rect(screen, DARKBLUE, spawn_button)
        pygame.draw.rect(screen, BLUE, planning_button)
        pygame.draw.rect(screen, RED, tracking_button)
        screen.blit(font.render("Spawn", True, WHITE), (spawn_button.x + 20, spawn_button.y + 5))
        screen.blit(font.render("Planning", True, WHITE), (planning_button.x + 10, planning_button.y + 5))
        screen.blit(font.render("Tracking", True, WHITE), (tracking_button.x + 10, tracking_button.y + 5))

         # 주차 성공 판정 조건
        if moving:
            dx = car_pos[0] - target_pos[0]
            dy = car_pos[1] - target_pos[1]
            distance = math.hypot(dx, dy)

            angle_diff = abs((car_angle - target_angle + 180) % 360 - 180)

            print(f"[DEBUG] distance: {distance:.2f}, angle_diff: {angle_diff:.2f}, moving: {moving}")
    

            if distance < 20.0 and angle_diff < 15.0:
                screen.blit(font.render("🅿️ 주차 완료!", True, BLACK), (WIDTH // 2 - 80, 20))
                moving = False
            

        pygame.display.flip()
        clock.tick(60)



    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    run_simulator()
