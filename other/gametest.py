import pygame
import sys

# 1. Khởi tạo Pygame
pygame.init()

# 2. Thiết lập cửa sổ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Test - Python 3.14")

# 3. Màu sắc và thuộc tính vật thể
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
player_pos = [400, 300]
player_size = 50
speed = 5

# 4. Giới hạn khung hình (FPS)
clock = pygame.time.Clock()

# --- VÒNG LẶP GAME CHÍNH ---
while True:
    # A. Xử lý sự kiện (Events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # B. Xử lý logic di chuyển (Input)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += speed
    if keys[pygame.K_UP]:
        player_pos[1] -= speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += speed

    # C. Vẽ (Drawing)
    screen.fill(WHITE) # Xóa màn hình bằng màu trắng
    
    # Vẽ người chơi (hình vuông màu xanh)
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    # D. Cập nhật hiển thị
    pygame.display.flip()

    # E. Khống chế 60 khung hình/giây
    clock.tick(60)