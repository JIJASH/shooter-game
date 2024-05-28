import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

# Classes
class Game:
    def __init__(self):
        self.levels = [Level1(), Level2(), Level3()]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.player = Player()
        self.scoreboard = Scoreboard()
        self.running = True
        self.game_over = False
        self.won = False
        self.show_instructions = True
        self.font = pygame.font.SysFont(None, 36)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and self.show_instructions:
                    self.show_instructions = False
                if event.type == pygame.MOUSEBUTTONDOWN and (self.game_over or self.won):
                    mouse_pos = pygame.mouse.get_pos()
                    if self.play_again_button.collidepoint(mouse_pos):
                        self.reset_game()
                    if self.exit_button.collidepoint(mouse_pos):
                        self.running = False

            if not self.show_instructions:
                if not self.game_over and not self.won:
                    self.player.handle_keys()
                    self.current_level.update(self.player, self.scoreboard)
                    if self.scoreboard.is_game_over():
                        self.game_over = True
                    elif self.scoreboard.score >= 500:
                        self.won = True
                    elif self.scoreboard.score >= 300 and self.current_level_index == 1:
                        self.current_level_index += 1
                        self.current_level = self.levels[self.current_level_index]
                        self.player.reset()
                    elif self.scoreboard.score >= 100 and self.current_level_index == 0:
                        self.current_level_index += 1
                        self.current_level = self.levels[self.current_level_index]
                        self.player.reset()

            self.draw()
            clock.tick(60)

    def draw(self):
        screen.fill(WHITE)
        if self.show_instructions:
            self.display_instructions()
        elif self.won:
            self.display_won()
        elif self.game_over:
            self.display_game_over()
        else:
            self.current_level.draw(screen)
            self.player.draw(screen)
            self.scoreboard.draw(screen)
            self.display_level()
        pygame.display.flip()

    def display_instructions(self):
        instructions = [
            "Welcome to the Shooter!",
            "Instructions:",
            "Use arrow keys to move the player.",
            "Press SPACE to shoot bullets.",
            "Avoid enemies and obstacles.",
            "Score points by shooting enemies.",
            "Reach 100 points to get to Level 2.",
            "Reach 300 points to get to Level 3.",
            "Reach 500 points to win the game!",
            "Press any key to start..."
        ]
        y_offset = 100
        for line in instructions:
            text = self.font.render(line, True, BLACK)
            screen.blit(text, (50, y_offset))
            y_offset += 40

    def display_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, BLACK)
        score_text = self.font.render(f"Score: {self.scoreboard.score}", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        self.display_buttons()

    def display_won(self):
        won_text = self.font.render("YOU WON!", True, BLACK)
        score_text = self.font.render(f"Score: {self.scoreboard.score}", True, BLACK)
        screen.blit(won_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        self.display_buttons()

    def display_buttons(self):
        self.play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        self.exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)

        pygame.draw.rect(screen, GRAY, self.play_again_button)
        pygame.draw.rect(screen, GRAY, self.exit_button)

        play_again_text = self.font.render("Play Again", True, BLACK)
        exit_text = self.font.render("Exit", True, BLACK)

        screen.blit(play_again_text, (self.play_again_button.x + 50, self.play_again_button.y + 10))
        screen.blit(exit_text, (self.exit_button.x + 80, self.exit_button.y + 10))

    def display_level(self):
        level_text = self.font.render(f"Level: {self.current_level_index + 1}", True, BLACK)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))

    def reset_game(self):
        self.__init__()
        self.show_instructions = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = self.create_rocket()
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 60
        self.speed = 5
        self.bullets = pygame.sprite.Group()

    def create_rocket(self):
        image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(image, BLUE, [(25, 0), (50, 50), (0, 50)])
        return image

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.add(bullet)

    def update(self):
        self.bullets.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 60


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = self.create_bomb()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(1, 3)

    def create_bomb(self):
        image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(image, RED, (25, 25), 25)
        pygame.draw.rect(image, BLACK, (20, 0, 10, 20))
        return image

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Level:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def update(self, player, scoreboard):
        self.enemies.update()
        player.update()
        self.check_collisions(player, scoreboard)
        self.spawn_enemies()

    def check_collisions(self, player, scoreboard):
        if pygame.sprite.spritecollideany(player, self.enemies):
            player.reset()
            scoreboard.decrease_life()

        if pygame.sprite.spritecollideany(player, self.obstacles):
            player.reset()
            scoreboard.decrease_life()

        for bullet in player.bullets:
            enemy_hit = pygame.sprite.spritecollideany(bullet, self.enemies)
            if enemy_hit:
                bullet.kill()
                enemy_hit.kill()
                scoreboard.increase_score()

    def spawn_enemies(self):
        if len(self.enemies) < 5:  # Ensure a minimum number of enemies on the screen
            enemy = Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(-100, -40))
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def draw(self, screen):
        self.enemies.draw(screen)
        self.obstacles.draw(screen)
        self.all_sprites.draw(screen)

    def is_completed(self, player):
        return False  # Levels no longer complete based on enemies killed, but score


class Level1(Level):
    def __init__(self):
        super().__init__()
        for i in range(5):
            enemy = Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(-100, -40))
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        for i in range(3):
            obstacle = Obstacle(random.randint(0, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 30))
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)


class Level2(Level):
    def __init__(self):
        super().__init__()
        for i in range(7):
            enemy = Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(-100, -40))
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        for i in range(5):
            obstacle = Obstacle(random.randint(0, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 30))
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)


class Level3(Level):
    def __init__(self):
        super().__init__()
        for i in range(10):
            enemy = Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(-100, -40))
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        for i in range(7):
            obstacle = Obstacle(random.randint(0, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 30))
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.font = pygame.font.SysFont(None, 36)

    def increase_score(self):
        self.score += 10

    def decrease_life(self):
        self.lives -= 1

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

    def is_game_over(self):
        return self.lives <= 0


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
