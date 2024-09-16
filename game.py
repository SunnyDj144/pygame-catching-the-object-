import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Falling Object")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load background image
background = pygame.image.load("py.jpeg")
background = pygame.transform.scale(background, (width, height))

# Load player (basket) image
player_image = pygame.image.load("p1.jpeg ")
player_image = pygame.transform.scale(player_image, (100, 50))

# Load sound effects
catch_sound = pygame.mixer.Sound("cc.mp3")
miss_sound = pygame.mixer.Sound("missing.mp3")

# Define the player (basket) and falling object attributes
player_width = 100
player_height = 50
player_x = (width - player_width) // 2
player_y = height - player_height - 10
player_speed = 10

object_width = 40
object_height = 40
object_x = random.randint(0, width - object_width)
object_y = -object_height
object_speed = 5

# Variables for game logic
score = 0
missed = 0
font = pygame.font.SysFont(None, 36)
game_over = False

# Main game loop
running = True
clock = pygame.time.Clock()

def draw_window():
    window.blit(background, (0, 0))  # Draw background

    # Draw player (basket image)
    window.blit(player_image, (player_x, player_y))
    
    # Draw falling object (red rectangle)
    pygame.draw.rect(window, RED, (object_x, object_y, object_width, object_height))
    
    # Display score and missed objects
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    missed_text = font.render(f"Missed: {missed}", True, (0, 0, 0))
    window.blit(score_text, (10, 10))
    window.blit(missed_text, (10, 40))

    pygame.display.update()

def reset_object():
    global object_x, object_y
    object_x = random.randint(0, width - object_width)
    object_y = -object_height

while running:
    clock.tick(30)  # 30 frames per second

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Get key press
        keys = pygame.key.get_pressed()

        # Move player left or right
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += player_speed

        # Move the falling object
        object_y += object_speed

        # Check if object is caught by the player
        if player_y < object_y + object_height and player_x < object_x + object_width and player_x + player_width > object_x:
            score += 1
            catch_sound.play()  # Play sound effect
            reset_object()

        # Reset the object if it falls off the screen and count as missed
        if object_y > height:
            missed += 1
            miss_sound.play()  # Play miss sound effect
            reset_object()

        # Increase object speed as score increases
        if score > 0 and score % 5 == 0:
            object_speed += 0.1

        # End the game if the player misses 3 objects
        if missed >= 3:
            game_over = True

        # Update the game window
        draw_window()

    else:
        # Display Game Over screen
        window.fill(WHITE)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
        window.blit(game_over_text, (width // 2 - 100, height // 2 - 50))
        window.blit(final_score_text, (width // 2 - 120, height // 2))
        pygame.display.update()

pygame.quit()