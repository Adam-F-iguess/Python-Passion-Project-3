import pygame



class card(pygame.sprite.Sprite):
    def __init__(self, card_suit, card_image, card_value, x, y):
        super().__init__()
        self.imgspr = card_image
        self.spr = pygame.image.load(self.imgspr).convert_alpha()
        self.image = self.spr
        self.rect = self.image.get_rect(topleft=(x, y))
        self.suit = card_suit
        self.val = card_value

class broke_boy(pygame.sprite.Sprite):
    def __init__(self, bb_name, bb_sprite, x, y):
        super().__init__()
        self.spr = pygame.image.load(bb_sprite).convert_alpha()
        self.image = self.spr
        self.rect = self.image.get_rect(topleft=(x, y))
        self.name = bb_name
        self.money = 1000
        
pygame.init()
screen = pygame.display.set_mode((800, 600))
ace = card('Spade', 'spirtes/aos.jpg', 1, 100, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ace.update() # Call the player's update method

    screen.fill((0, 0, 0)) # Clear the screen
    screen.blit(ace.image, ace.rect) # Draw the player
    pygame.display.flip()