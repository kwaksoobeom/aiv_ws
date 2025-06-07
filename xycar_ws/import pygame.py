import pygame
import math
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
RED = (220, 80, 80)
BLACK = (0, 0, 0)

# 차량 스폰 초기값
def get_random_pose():
    x = random.randint(100, 300)
    y = random.randint(100, 500)
    angle = random.uniform(0, 360)
    return [x, y, angle]

car_pos = get_random_pose()
target_pos = (700, 100)

# 버튼
font = pygame.font.SysFont("Arial", 24)
planning_button = pygame.Rect(250, 550, 120, 40)
tracking_button = pygame.Rect(400, 550, 120, 40)

# 차량 이동 변수
path = []
moving = False
index = 0

# 차량 이미지
car_image = pygame.Surface((50, 30), pygame.SRCALPHA)
pygame.draw.rect(car_image, (0, 200, 0), (0, 0, 50, 30))

def draw_rotated_car(x, y, angle):
    rotated = pygame.transform.rotate(car_image, -angle)
    rect = rotated.get_rect(center=(x, y))
    screen.blit(rotated, rect)

# 메인 루프
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if planning_button.collidepoint(event.pos):
                path = [(car_pos[0] + i * 6, car_pos[1] - i * 2) for i in range(100)]
                index = 0
            elif tracking_button.collidepoint(event.pos):
                moving = True

    # 주차 영역
    pygame.draw.rect(screen, RED, (target_pos[0] - 25, target_pos[1] - 15, 50, 30), 2)

    # 경로 시각화
    if path:
        pygame.draw.lines(screen, BLUE, False, path, 3)

    # 차량 이동
    if moving and index < len(path):
        car_pos[0], car_pos[1] = path[index]
        car_pos[2] = math.degrees(math.atan2(
            path[index][1] - car_pos[1],
            path[index][0] - car_pos[0]
        ))
        index += 1

    # 차량 그리기
    draw_rotated_car(car_pos[0], car_pos[1], car_pos[2])

    # 버튼 그리기
    pygame.draw.rect(screen, BLUE, planning_button)
    pygame.draw.rect(screen, RED, tracking_button)
    screen.blit(font.render("Planning", True, WHITE), (planning_button.x + 10, planning_button.y + 5))
    screen.blit(font.render("Tracking", True, WHITE), (tracking_button.x + 10, tracking_button.y + 5))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
