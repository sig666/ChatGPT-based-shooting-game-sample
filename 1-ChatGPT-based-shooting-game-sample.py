import pygame
import sys
import random

# 画面サイズ
WIDTH = 800
HEIGHT = 600

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# ゲームのFPS
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('縦スクロールシューティングゲーム')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.bullets = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = -40
            self.rect.x = random.randint(0, WIDTH - 40)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()

player = Player(WIDTH // 2, HEIGHT - 60)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for i in range(10):
    enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(-200, -40))
    enemies.add(enemy)
    all_sprites.add(enemy)

score = 0
lives = 3

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(bullets) < player.bullets:
                bullet = Bullet(player.rect.x + 22, player.rect.y)
                all_sprites.add(bullet)
                bullets.add(bullet)

    all_sprites.update()

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(-200, -40))
        all_sprites.add(enemy)
        enemies.add(enemy)

    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        lives -= 1
        if lives == 0:
            pygame.quit()
            sys.exit()
        else:
            player.rect.x = WIDTH // 2
            player.rect.y = HEIGHT - 60
            for _ in range(10):
                enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(-200, -40))
                enemies.add(enemy)
                all_sprites.add(enemy)

    screen.fill(BLACK)

    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score}", 36, WIDTH // 2, 10)
    draw_text(screen, f"Lives: {lives}", 36, WIDTH - 100, 10)

    pygame.display.flip()
    clock.tick(FPS)