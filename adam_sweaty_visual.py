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




ace_spades = card('spade', 'sprites\\aos.jpg', 'ace', 200, 100)
two_spades = card('spade', 'sprites\\2s.jpg', '2', 210, 100)
three_spades = card('spade', 'sprites\\3s.jpg', '3', 220, 100)
four_spades = card('spade', 'sprites\\4s.jpg', '4', 230, 100)
five_spades = card('spade', 'sprites\\5s.jpg', '5', 240, 100)
six_spades = card('spade', 'sprites\\6s.jpg', '6', 250, 100)
seven_spades = card('spade', 'sprites\\7s.jpg', '7', 260, 100)
eight_spades = card('spade', 'sprites\\8s.jpg', '8', 270, 100)
nine_spades = card('spade', 'sprites\\9s.jpg', '9', 280, 100)
ten_spades = card('spade', 'sprites\\10s.jpg', '10', 290, 100)
jack_spades = card('spade', 'sprites\\js.jpg', 'jack', 300, 100)
queen_spades = card('spade', 'sprites\\qs.jpg', 'queen', 310, 100)
king_spades = card('spade', 'sprites\\ks.jpg', 'king', 320, 100)

ace_hearts = card('heart', 'sprites\\aoh.jpg', 'ace', 200, 120)
two_hearts = card('heart', 'sprites\\2h.jpg', '2', 210, 120)
three_hearts = card('heart', 'sprites\\3h.jpg', '3', 220, 120)
four_hearts = card('heart', 'sprites\\4h.jpg', '4', 230, 120)
five_hearts = card('heart', 'sprites\\5h.jpg', '5', 240, 120)
six_hearts = card('heart', 'sprites\\6h.jpg', '6', 250, 120)
seven_hearts = card('heart', 'sprites\\7h.jpg', '7', 260, 120)
eight_hearts = card('heart', 'sprites\\8h.jpg', '8', 270, 120)
nine_hearts = card('heart', 'sprites\\9h.jpg', '9', 280, 120)
ten_hearts = card('heart', 'sprites\\10h.jpg', '10', 290, 120)
jack_hearts = card('heart', 'sprites\\jh.jpg', 'jack', 300, 120)
queen_hearts = card('heart', 'sprites\\qh.jpg', 'queen', 310, 120)
king_hearts = card('heart', 'sprites\\kh.jpg', 'king', 320, 120)

ace_diamonds = card('diamond', 'sprites\\aod.jpg', 'ace', 200, 140)
two_diamonds = card('diamond', 'sprites\\2d.jpg', '2', 210, 140)
three_diamonds = card('diamond', 'sprites\\3d.jpg', '3', 220, 140)
four_diamonds = card('diamond', 'sprites\\4d.jpg', '4', 230, 140)
five_diamonds = card('diamond', 'sprites\\5d.jpg', '5', 240, 140)
six_diamonds = card('diamond', 'sprites\\6d.jpg', '6', 250, 140)
seven_diamonds = card('diamond', 'sprites\\7d.jpg', '7', 260, 140)
eight_diamonds = card('diamond', 'sprites\\8d.jpg', '8', 270, 140)
nine_diamonds = card('diamond', 'sprites\\9d.jpg', '9', 280, 140)
ten_diamonds = card('diamond', 'sprites\\10d.jpg', '10', 290, 140)
jack_diamonds = card('diamond', 'sprites\\jd.jpg', 'jack', 300, 140)
queen_diamonds = card('diamond', 'sprites\\qd.jpg', 'queen', 310, 140)
king_diamonds = card('diamond', 'sprites\\kd.jpg', 'king', 320, 140)

ace_clubs = card('club', 'sprites\\aoc.jpg', 'ace', 200, 160)
two_clubs = card('club', 'sprites\\2c.jpg', '2', 210, 160)
three_clubs = card('club', 'sprites\\3c.jpg', '3', 220, 160)
four_clubs = card('club', 'sprites\\4c.jpg', '4', 230, 160)
five_clubs = card('club', 'sprites\\5c.jpg', '5', 240, 160)
six_clubs = card('club', 'sprites\\6c.jpg', '6', 250, 160)
seven_clubs = card('club', 'sprites\\7c.jpg', '7', 260, 160)
eight_clubs = card('club', 'sprites\\8c.jpg', '8', 270, 160)
nine_clubs = card('club', 'sprites\\9c.jpg', '9', 280, 160)
ten_clubs = card('club', 'sprites\\10c.jpg', '10', 290, 160)
jack_clubs = card('club', 'sprites\\jc.jpg', 'jack', 300, 160)
queen_clubs = card('club', 'sprites\\qc.jpg', 'queen', 310, 160)
king_clubs = card('club', 'sprites\\kc.jpg', 'king', 320, 160)

jokerb = card('black', 'sprites\\jokerb.jpg', 'joker', 200, 180)
jokerr = card('red', 'sprites\\jokerr.jpg', 'joker', 210, 180)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ace_spades.update() # Call the player's update method

    screen.fill((0, 0, 0)) # Clear the screen
    screen.blit(ace_spades.image, ace_spades.rect) # Draw the player
    pygame.display.flip()