#!/usr/bin/env python3

import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 960, 720
FPS = 60
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chase Shooter Game")

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100  # Player health
        self.color = BLUE
        self.size = 30  # Make the player square larger for better visibility

    def move(self, dx, dy):
        """Move the player based on input direction."""
        self.x += dx * PLAYER_SPEED
        self.y += dy * PLAYER_SPEED
        
        # Keep player on the screen
        self.x = max(0, min(WIDTH - self.size, self.x))
        self.y = max(0, min(HEIGHT - self.size, self.y))

    def draw(self):
        # Draw body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        
        # Draw eyes
        eye_radius = 5
        eye_y = self.y + 5
        # Left eye
        pygame.draw.circle(screen, BLACK, (self.x + 10, eye_y), eye_radius)
        # Right eye
        pygame.draw.circle(screen, BLACK, (self.x + 20, eye_y), eye_radius)

        # Display health and score
        self.display_health()

    def display_health(self):
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {self.health}", True, BLACK)
        screen.blit(health_text, (10, 10))


# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x + 12.5  # Center the bullet
        self.y = y
        self.color = BLACK
        self.size = 5

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self):
        self.y -= BULLET_SPEED  # Move bullet upward


# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = RED
        self.size = 20

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def follow(self, player):
        if self.x < player.x:
            self.x += ENEMY_SPEED
        if self.x > player.x:
            self.x -= ENEMY_SPEED
        if self.y < player.y:
            self.y += ENEMY_SPEED
        if self.y > player.y:
            self.y -= ENEMY_SPEED

def main():
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2, HEIGHT // 2)
    enemies = []
    bullets = []
    score = 0  # Initialize score

    enemy_spawn_delay = 2000  # milliseconds for enemy spawn time
    last_spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        # Fill the screen with a solid color (e.g., white)
        screen.fill(WHITE)  # Change the color if you prefer a different background

        current_time = pygame.time.get_ticks()

        # Spawn a new enemy every 2 seconds
        if current_time - last_spawn_time > enemy_spawn_delay:
            enemies.append(Enemy(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20)))
            last_spawn_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        player.move(dx, dy)

        # Shooting mechanics
        if keys[pygame.K_SPACE]:  # Press space to shoot
            bullets.append(Bullet(player.x, player.y))  # Create a bullet at player's position

        # Move bullets and check for collisions
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if bullet.y < 0:  # Remove bullet if it goes off screen
                bullets.remove(bullet)

            # Check for collision with enemies
            for enemy in enemies[:]:
                if (bullet.x < enemy.x + enemy.size and
                    bullet.x + bullet.size > enemy.x and
                    bullet.y < enemy.y + enemy.size and
                    bullet.y + bullet.size > enemy.y):
                    enemies.remove(enemy)  # Remove enemy if hit
                    bullets.remove(bullet)  # Remove bullet on hit
                    score += 10  # Increase score by 10 for each enemy killed
                    print(f"Score: {score}")  # Debug statement to show score
                    break  # Exit to prevent modifying the list during iteration

        player.draw()

        # Move and draw enemies
        for enemy in enemies[:]:
            enemy.follow(player)  # Enemies follow the player
            enemy.draw()

            # Check for collision with player
            if (player.x < enemy.x + enemy.size and
                player.x + player.size > enemy.x and
                player.y < enemy.y + enemy.size and
                player.y + player.size > enemy.y):
                player.health -= 1  # Reduce player health upon collision
                print(f"Player Health: {player.health}")
                enemies.remove(enemy)  # Remove enemy for a smoother gameplay experience
                if player.health <= 0:
                    print("Game Over!")
                    running = False

        # Display the score on the screen
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 10))  # Display score at the top-right corner

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()