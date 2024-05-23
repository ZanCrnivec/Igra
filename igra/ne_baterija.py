import pygame
import sys
import random
import math

pygame.init()

display = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Nočna straža")
pygame.display.set_icon(pygame.image.load("drevo1.png"))
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def main(self, display):
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), self.radius+5)
        pygame.draw.circle(display, (255, 255, 255), (self.x, self.y), self.radius)


class Tree:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    def draw(self, display, scroll):
        display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

class Stick:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (100, 50))
    def draw(self, display, scroll):
        display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

class Campfire:
    def __init__(self, x, y, image1, image2):
        self.x = x
        self.y = y
        self.image1 = pygame.transform.scale(image1, (600, 400))
        self.image2 = pygame.transform.scale(image2, (600, 400))
        self.current_image = self.image1
        self.image_timer = 0

    def draw(self, display, scroll):
        self.image_timer += 1
        if self.image_timer >= 30: 
            self.image_timer = 0
            if self.current_image == self.image1:
                self.current_image = self.image2
            else:
                self.current_image = self.image1

        display.blit(self.current_image, (self.x - scroll[0], self.y - scroll[1]))

class StaminaBar():
    def __init__(self, x, y, width, height, max_stamina):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stamina = max_stamina
        self.max_stamina = max_stamina  
    def draw(self, display):    
        ratio = self.stamina / self.max_stamina
        pygame.draw.rect(display, "white", (self.x + 4, self.y + 4, (self.width * ratio) - 8, self.height - 8))

class Tema:
    def __init__(self, width, height, image):
        self.width = width
        self.height = height
        self.original_image = pygame.transform.scale(image, (self.width, self.height))
        self.image = self.original_image

    def draw(self, display, alpha, player_x, player_y, angle):
        temp_surface = pygame.transform.rotate(self.original_image, angle)
        temp_surface.set_alpha(alpha)
        rotated_rect = temp_surface.get_rect(center=(player_x, player_y))
        display.blit(temp_surface, rotated_rect.topleft)

def check_proximity(px, py, sx, sy, threshold=100):
    distance = ((px - sx) ** 2 + (py - sy) ** 2) ** 0.5
    return distance < threshold

def check_proximity2(px, py, sx, sy, threshold=500):
    distance2 = ((px - sx) ** 2 + (py - sy) ** 2) ** 0.5
    return distance2 < threshold

def blizu_ognja(px, py, cx, cy):
    distance2 = ((px - (cx+285)) ** 2 + (py - (cy+180)) ** 2) ** 0.55
    return distance2

def draw_text(text, font, text_color, x, y, value=0):
    img = font.render(text + str(value), True, text_color)
    display.blit(img, (x, y))

stamina_bar = StaminaBar(325, 600, 400, 30, 100)
tree_list = [Tree(random.randint(-2000, 2000), random.randint(-2000, 2000), pygame.transform.scale(pygame.image.load(random.choice(["drevo1.png", "drevo2.png"])), (700, 400))) for _ in range(70)]
tree_list.sort(key=lambda tree: tree.y)

stick_list = []
stick_amount = 0
stick_inv = 0

def spawn_stick():
    stick = Stick(random.randint(-2000, 2000), random.randint(-2000, 2000), pygame.image.load("palca.png"))
    stick_list.append(stick)
    stick_list.sort(key=lambda stick: stick.y)

text_font = pygame.font.SysFont("Comic Sans MS", 30)
player = Player(500, 400, 20)
campfire = Campfire(500, 400, pygame.image.load("ogenj1.png"), pygame.image.load("ogenj2.png"))

display_scroll = [0, 0]
timer = 25
tema_image = pygame.image.load("tema5.png")

tema = Tema(1500, 1500, tema_image)
score = 0
svetloba = 255

while True:
    display.fill((25, 165, 85))
    
    if stick_amount < 31 and random.randint(1, 2) == 1:
        spawn_stick()
        stick_amount += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LSHIFT] and stamina_bar.stamina > 0:
        speed = 6
        stamina_bar.stamina -= 0.4
    else:
        speed = 2
        if stamina_bar.stamina < stamina_bar.max_stamina:
            if any([keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]]):
                stamina_bar.stamina += 0.1
            else:
                stamina_bar.stamina += 0.7
    
    if keys[pygame.K_a]:
        display_scroll[0] -= speed
    if keys[pygame.K_d]:
        display_scroll[0] += speed
    if keys[pygame.K_w]:
        display_scroll[1] -= speed
    if keys[pygame.K_s]:
        display_scroll[1] += speed


    for tree in tree_list:
        tree.draw(display, display_scroll)

    for stick in stick_list:
        stick.draw(display, display_scroll)

    remaining_sticks = []
    for stick in stick_list:
        if check_proximity(500, 400, stick.x - display_scroll[0], stick.y - display_scroll[1]):
            stick_amount -= 1
            stick_inv += 1
        else:
            remaining_sticks.append(stick)
    stick_list = remaining_sticks

    for tree in tree_list:
        if check_proximity2(campfire.x - display_scroll[0], campfire.y - display_scroll[1], tree.x - display_scroll[0], tree.y - display_scroll[1]):
            while check_proximity2(campfire.x - display_scroll[0], campfire.y - display_scroll[1], tree.x - display_scroll[0], tree.y - display_scroll[1]):
                tree.x = random.randint(-2000, 2000)
                tree.y = random.randint(-2000, 2000)

    timer -= 0.02
    score += 0.02

    if check_proximity(500, 400, (campfire.x + 285) - display_scroll[0], (campfire.y + 180) - display_scroll[1]):
        timer += stick_inv * 5
        score += stick_inv * 5
        
        stick_inv = 0

    if timer < 0:
        pygame.quit()

    player.main(display)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_x - (500), mouse_y - (400)
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

    distance_to_fire = blizu_ognja(500, 400, campfire.x - display_scroll[0], campfire.y - display_scroll[1])
    alpha = int(max(255-(timer * 255 / 15), min(255, distance_to_fire * 255 / 1000)))

    tema.draw(display, alpha, 500, 400, angle-90)
    display.blit(pygame.transform.scale(pygame.image.load("luč.png"), (timer*10, timer*10)), (800-display_scroll[0]-timer*5, 600-display_scroll[1]-timer*5))
    campfire.draw(display, display_scroll)

    draw_text("Palce: ", text_font, (255, 255, 255), 330, 550, stick_inv)
    draw_text("Čas: ", text_font, (255, 255, 255), 620, 550, int(timer // 1))
    draw_text("Score: ", text_font, (255, 255, 255), 460, 0, int(score // 1))
    stamina_bar.draw(display)

    clock.tick(60)
    pygame.display.update()
