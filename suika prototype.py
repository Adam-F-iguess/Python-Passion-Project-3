import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Suika Game Prototype")

# Jar dimensions
JAR_LEFT = 100
JAR_TOP = 150
JAR_WIDTH = 400
JAR_HEIGHT = 600
JAR_RIGHT = JAR_LEFT + JAR_WIDTH
JAR_BOTTOM = JAR_TOP + JAR_HEIGHT

# Fruit definitions: (radius, color, weight)
FRUITS = [
    (20, (255, 0, 0), 1),    # Cherry
    (28, (255, 128, 0), 2),  # Strawberry
    (36, (255, 255, 0), 3),  # Lemon
    (44, (0, 255, 0), 5),    # Apple
    (52, (0, 255, 255), 8),  # Melon
    (60, (255, 0, 255), 13), # Watermelon
]

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

class Fruit:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.radius, self.color, self.weight = FRUITS[kind]
        self.hitbox_radius = self.radius + 4  # 4 pixels larger hitbox
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.merged = False
        self.landed = False

    def update(self, fruits):
        self.vy += 0.5  # gravity
        self.x += self.vx
        self.y += self.vy

        # Floor collision (jar bottom)
        if self.y + self.radius > JAR_BOTTOM:
            self.y = JAR_BOTTOM - self.radius
            self.vy = 0
            self.landed = True
            self.vx *= 0.99  # More slippery!
        else:
            # Check if supported by another fruit
            if is_supported(self, fruits):
                self.vy = 0
                self.landed = True
                self.vx *= 0.99  # Only slip if not blocked horizontally
            else:
                self.landed = False
                self.vx = 0  # No sliding in the air

        # Wall collision (jar sides)
        if self.x - self.radius < JAR_LEFT:
            self.x = JAR_LEFT + self.radius
            self.vx = -self.vx * 0.7 if self.y + self.radius >= JAR_BOTTOM else 0
        if self.x + self.radius > JAR_RIGHT:
            self.x = JAR_RIGHT - self.radius
            self.vx = -self.vx * 0.7 if self.y + self.radius >= JAR_BOTTOM else 0
            
    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
 
        
def collide(f1, f2):
    dist = math.hypot(f1.x - f2.x, f1.y - f2.y)
    return dist < f1.hitbox_radius + f2.hitbox_radius


def resolve_collision(f1, f2):
    dx = f2.x - f1.x
    dy = f2.y - f1.y
    dist = math.hypot(dx, dy)
    overlap = f1.hitbox_radius + f2.hitbox_radius - dist
    if overlap > 0 and dist != 0:
        nx = dx / dist
        ny = dy / dist

        # Weight-based push: heavier fruits move less
        total_weight = f1.weight + f2.weight
        move1 = (f2.weight / total_weight) * overlap
        move2 = (f1.weight / total_weight) * overlap

        # Only push horizontally if vertical push would go into the ground or if blocked
        can_move_vertically = True
        if ((f1.y + f1.radius > JAR_BOTTOM - 1 and ny > 0) or
            (f2.y + f2.radius > JAR_BOTTOM - 1 and ny < 0) or
            (f1.x - f1.radius < JAR_LEFT and nx < 0) or
            (f2.x + f2.radius > JAR_RIGHT and nx > 0)):
            can_move_vertically = False

        if not can_move_vertically:
            f1.x -= nx * move1
            f2.x += nx * move2
        else:
            f1.x -= nx * move1
            f1.y -= ny * move1
            f2.x += nx * move2
            f2.y += ny * move2

        # Only apply horizontal velocity (slippery) if both are on the ground
        if (abs(f1.y + f1.radius - JAR_BOTTOM) < 1 and abs(f2.y + f2.radius - JAR_BOTTOM) < 1):
            impact = (f1.vy - f2.vy) * 0.3
            f1.vx += nx * abs(impact)
            f2.vx -= nx * abs(impact)

        # Clamp positions inside the jar
        for f in (f1, f2):
            if f.x - f.radius < JAR_LEFT:
                f.x = JAR_LEFT + f.radius
                f.vx = -f.vx * 0.7
            if f.x + f.radius > JAR_RIGHT:
                f.x = JAR_RIGHT - f.radius
                f.vx = -f.vx * 0.7
            if f.y + f.radius > JAR_BOTTOM:
                f.y = JAR_BOTTOM - f.radius
                f.vy = 0
                f.landed = True


def merge(f1, f2):
    if f1.kind < len(FRUITS) - 1:
        return Fruit(f1.kind + 1, (f1.x + f2.x) / 2, (f1.y + f2.y) / 2)
    return None


def is_supported(fruit, fruits):
    if abs(fruit.y + fruit.radius - JAR_BOTTOM) < 1:
        return True
    for other in fruits:
        if other is fruit:
            continue
        dx = abs(fruit.x - other.x)
        dy = (fruit.y + fruit.hitbox_radius) - (other.y - other.hitbox_radius)
        if dx < fruit.hitbox_radius + other.hitbox_radius - 2 and 0 <= dy < 2:
            return True
    return False


fruits = []
# When spawning a new fruit, drop it above the jar
current_fruit = Fruit(0, JAR_LEFT + JAR_WIDTH // 2, JAR_TOP - 40)
next_kind = random.randint(0, 2)
game_over = False
score = 0
drop_cooldown = 3000  # milliseconds (6 seconds)
last_drop_time = pygame.time.get_ticks() - drop_cooldown  # allow immediate first drop

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_fruit.x -= 20
                if current_fruit.x - current_fruit.radius < JAR_LEFT:
                    current_fruit.x = JAR_LEFT + current_fruit.radius
            if event.key == pygame.K_RIGHT:
                current_fruit.x += 20
                if current_fruit.x + current_fruit.radius > JAR_RIGHT:
                    current_fruit.x = JAR_RIGHT - current_fruit.radius
            if event.key == pygame.K_SPACE:
                now = pygame.time.get_ticks()
                if now - last_drop_time >= drop_cooldown:
                    fruits.append(current_fruit)
                    # Add a small random vx to the new fruit
                    vx = random.uniform(-2, 2)
                    current_fruit = Fruit(next_kind, JAR_LEFT + JAR_WIDTH // 2, JAR_TOP - 40)
                    current_fruit.vx = vx
                    next_kind = random.randint(0, 2)
                    last_drop_time = now

    # Update fruits
    for fruit in fruits:
        fruit.update(fruits)

    # --- PRIORITY LOOP: mergers -> walls -> collisions ---
    max_priority_passes = 10
    priority_pass = 0
    while priority_pass < max_priority_passes:
        # 1. Try to merge
        merged = False
        merged_indices = set()
        new_fruits = []
        fruits_copy = fruits[:]  # Work on a copy to avoid index issues
        for i in range(len(fruits_copy)):
            if i >= len(fruits):  # If fruits list changed, break
                break
            for j in range(i + 1, len(fruits_copy)):
                if j >= len(fruits):  # If fruits list changed, break
                    break
                if i in merged_indices or j in merged_indices:
                    continue
                if fruits[i].kind == fruits[j].kind and collide(fruits[i], fruits[j]):
                    new_fruit = merge(fruits[i], fruits[j])
                    if new_fruit:
                        new_fruits.append(new_fruit)
                        merged_indices.add(i)
                        merged_indices.add(j)
                        score += 10 * (new_fruit.kind + 1)
                        merged = True
                        break  # Only merge one pair per pass
            if merged:
                break
        if merged:
            # Remove merged fruits by index (highest first to avoid shifting)
            for idx in sorted(merged_indices, reverse=True):
                del fruits[idx]
            fruits.extend(new_fruits)
            priority_pass += 1
            continue  # Go back to mergers

        # 2. Try to resolve wall collisions
        wall_bounced = False
        for fruit in fruits:
            if fruit.x - fruit.radius < JAR_LEFT:
                fruit.x = JAR_LEFT + fruit.radius
                wall_bounced = True
            if fruit.x + fruit.radius > JAR_RIGHT:
                fruit.x = JAR_RIGHT - fruit.radius
                wall_bounced = True
        if wall_bounced:
            priority_pass += 1
            continue  # After wall bounce, check mergers again

        # 3. Try to resolve fruit-to-fruit collisions
        collision_happened = False
        fruits_copy = fruits[:]
        for i in range(len(fruits_copy)):
            for j in range(i + 1, len(fruits_copy)):
                if i >= len(fruits) or j >= len(fruits):
                    break
                before = (fruits[i].x, fruits[i].y, fruits[j].x, fruits[j].y)
                resolve_collision(fruits[i], fruits[j])
                after = (fruits[i].x, fruits[i].y, fruits[j].x, fruits[j].y)
                if before != after:
                    collision_happened = True
        if collision_happened:
            priority_pass += 1
            continue  # After collision, check mergers again

        break  # If nothing happened, exit the loop

    # --- GAME OVER CHECK ---
    for fruit in fruits:
        if fruit.landed and fruit.y - fruit.radius < JAR_TOP + 10:
            game_over = True

    # Draw everything
    screen.fill((30, 30, 30))

    # Draw jar (rectangle and top)
    pygame.draw.rect(screen, (60, 60, 60), (JAR_LEFT, JAR_TOP, JAR_WIDTH, JAR_HEIGHT), 0)
    pygame.draw.rect(screen, (200, 200, 200), (JAR_LEFT, JAR_TOP, JAR_WIDTH, JAR_HEIGHT), 5)
    pygame.draw.rect(screen, (255, 100, 100), (JAR_LEFT, JAR_TOP, JAR_WIDTH, 10))  # visual top

    # Draw fruits
    for fruit in fruits:
        fruit.draw(screen)
    current_fruit.draw(screen)

    # Draw cooldown indicator (to the right of jar, near top)
    now = pygame.time.get_ticks()
    cooldown_ratio = min(1, (now - last_drop_time) / drop_cooldown)
    indicator_radius = 30
    indicator_center = (JAR_RIGHT + 60, JAR_TOP + 40)
    pygame.draw.circle(screen, (100, 100, 100), indicator_center, indicator_radius, 3)
    if cooldown_ratio < 1:
        # Draw cooldown fill (arc)
        end_angle = -math.pi / 2 + 2 * math.pi * cooldown_ratio
        pygame.draw.arc(
            screen,
            (0, 200, 255),
            (indicator_center[0] - indicator_radius, indicator_center[1] - indicator_radius, indicator_radius * 2, indicator_radius * 2),
            -math.pi / 2,
            end_angle,
            8
        )
    else:
        # Ready: draw full circle
        pygame.draw.circle(screen, (0, 255, 0), indicator_center, indicator_radius - 6, 0)

    # Draw "Next" fruit preview under cooldown
    next_label = font.render("Next", True, (255, 255, 255))
    screen.blit(next_label, (indicator_center[0] - next_label.get_width() // 2, indicator_center[1] + indicator_radius + 50))
    next_fruit_y = indicator_center[1] + indicator_radius + 90  # Increased offset
    pygame.draw.circle(
        screen,
        FRUITS[next_kind][1],
        (indicator_center[0], next_fruit_y),
        FRUITS[next_kind][0]
    )

    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

# Game Over screen
screen.fill((30, 30, 30))
msg = big_font.render("Game Over!", True, (255, 80, 80))
score_msg = font.render(f"Final Score: {score}", True, (255, 255, 0))
screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height()))
screen.blit(score_msg, (WIDTH // 2 - score_msg.get_width() // 2, HEIGHT // 2 + 10))
pygame.display.flip()
pygame.time.wait(2500)
pygame.quit()