import pygame
import random
import sys


pygame.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
ROAD_COLOR = (30, 30, 30)
LINE_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Car Racing Game")

clock = pygame.time.Clock()
FPS = 60

# Load images
player_car_img = pygame.image.load(r"C:\Users\vaysh\OneDrive\Desktop\gaming\car_racing\player_car.png").convert_alpha()
player_car_img = pygame.transform.scale(player_car_img, (50, 100))

obstacle_car_images = [
    pygame.image.load(r"C:\Users\vaysh\OneDrive\Desktop\gaming\car_racing\enemy_car1.png").convert_alpha(),
    pygame.image.load(r"C:\Users\vaysh\OneDrive\Desktop\gaming\car_racing\enemy_car2.png").convert_alpha(),
    pygame.image.load(r"C:\Users\vaysh\OneDrive\Desktop\gaming\car_racing\enemy_car3.png").convert_alpha(),
]
obstacle_car_images = [pygame.transform.scale(img, (50, 100)) for img in obstacle_car_images]

ROAD_WIDTH = 300
ROAD_LEFT = (SCREEN_WIDTH - ROAD_WIDTH) // 2
LINE_WIDTH = 10
LINE_HEIGHT = 40
LINE_GAP = 20

player_x = SCREEN_WIDTH // 2 - 25
player_y = SCREEN_HEIGHT - 120
player_speed = 7

class Obstacle:
    def __init__(self, speed):
        self.image = random.choice(obstacle_car_images)
        lane_positions = [
            ROAD_LEFT + 20,
            ROAD_LEFT + ROAD_WIDTH // 3 + 10,
            ROAD_LEFT + 2 * (ROAD_WIDTH // 3) + 10,
        ]
        self.x = random.choice(lane_positions)
        self.y = -100
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y > SCREEN_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 100)

class RoadLines:
    def __init__(self):
        self.lines = []
        for i in range(10):
            y = i * (LINE_HEIGHT + LINE_GAP)
            self.lines.append(pygame.Rect(SCREEN_WIDTH // 2 - LINE_WIDTH // 2, y, LINE_WIDTH, LINE_HEIGHT))

    def update(self, speed):
        for line in self.lines:
            line.y += speed
            if line.y > SCREEN_HEIGHT:
                line.y = -LINE_HEIGHT - LINE_GAP

    def draw(self, screen):
        for line in self.lines:
            pygame.draw.rect(screen, LINE_COLOR, line)

def draw_road():
    screen.fill(GRAY)
    pygame.draw.rect(screen, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

def main():
    score = 0
    font = pygame.font.SysFont(None, 36)
    obstacles = []
    obstacle_timer = 0
    obstacle_delay = 1500
    road_lines = RoadLines()
    obstacle_speed = 4

    global player_x
    running = True

    while running:
        dt = clock.tick(FPS)
        obstacle_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        
        if player_x < ROAD_LEFT + 10:
            player_x = ROAD_LEFT + 10
        elif player_x > ROAD_LEFT + ROAD_WIDTH - 50 - 10:
            player_x = ROAD_LEFT + ROAD_WIDTH - 50 - 10

       
        if obstacle_timer > obstacle_delay:
            obstacles.append(Obstacle(obstacle_speed))
            obstacle_timer = 0
            if obstacle_delay > 700:
                obstacle_delay -= 20
            obstacle_speed += 0.05

       
        for obstacle in obstacles[:]:
            obstacle.update()
            if obstacle.off_screen():
                obstacles.remove(obstacle)
                score += 1

        road_lines.update(obstacle_speed)

        
        player_rect = pygame.Rect(player_x, player_y, 50, 100)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.get_rect()):
                running = False

        
        draw_road()
        road_lines.draw(screen)
        screen.blit(player_car_img, (player_x, player_y))
        for obstacle in obstacles:
            obstacle.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over", True, WHITE)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
