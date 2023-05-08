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
GREEN = (0, 255, 0)

# ゲームのFPS
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('縦スクロールシューティングゲーム')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

player_image = pygame.image.load('/Users/user1/1.jpg').convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 50))
enemy_image = pygame.image.load('/Users/user1/2.jpg').convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (40, 40))
power_up_image = pygame.image.load('/Users/user1/3.jpg').convert_alpha()
power_up_image = pygame.transform.scale(power_up_image, (30, 30))
big_enemy_image = pygame.image.load('/Users/user1/4.jpg').convert_alpha()
big_enemy_image = pygame.transform.scale(big_enemy_image, (80, 80))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
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
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = random.randint(1, 5)
        self.speed_x = random.choice([-1, 1])

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        if self.rect.y > HEIGHT:
            self.rect.y = -40
            self.rect.x = random.randint(0, WIDTH - 40)
            self.speed_x = random.choice([-1, 1])

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = power_up_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

class BigEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = big_enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width:
            self.speed = -self.speed

class Text(pygame.sprite.Sprite):
    def __init__(self, text, x, y, duration):
        super().__init__()
        self.image = font.render(text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.duration = duration
        self.time_created = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.time_created >= self.duration:
            self.kill()

player = Player(WIDTH // 2, HEIGHT - 60)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
big_enemies = pygame.sprite.Group()
texts = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for i in range(10):
    enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(-200, -40))
    enemies.add(enemy)
    all_sprites.add(enemy)

score = 0
lives = 3
bullet_size = (5, 10)

pygame.time.set_timer(pygame.USEREVENT, 10000)
pygame.time.set_timer(pygame.USEREVENT + 1, 15000)

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
                bullet = Bullet(player.rect.x + 22, player.rect.y, bullet_size)
                all_sprites.add(bullet)
                bullets.add(bullet)
        if event.type == pygame.USEREVENT:
            power_up = PowerUp(random.randint(0, WIDTH - 30), -30)
            all_sprites.add(power_up)
            power_ups.add(power_up)
        if event.type == pygame.USEREVENT + 1:
            big_enemy = BigEnemy(random.randint(0, WIDTH - 80), random.randint(0, HEIGHT // 4))
            all_sprites.add(big_enemy)
            big_enemies.add(big_enemy)

    all_sprites.update()

    # Enemy collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(-200, -40))
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Big enemy collisions
    hits = pygame.sprite.groupcollide(big_enemies, bullets, True, True)
    for hit in hits:
        score += 100
        text = Text("Destroyed: Score + 100", hit.rect.x, hit.rect.y, 1000)
        all_sprites.add(text)
        texts.add(text)

    # Power up collisions
    hits = pygame.sprite.spritecollide(player, power_ups, True)
    if hits:
        player.bullets += 1
        bullet_size = (bullet_size[0] * 1.5, bullet_size[1] * 1.5)

    # Enemy and player collisions
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
