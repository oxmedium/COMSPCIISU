import pygame
import sys
import time
import random

#Intialization
pygame.init()
#Screen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h - 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Speed Test")

#Fonts
FONT = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
GRAY = (50,50,50)
LIGHT_GRAY = (100,100,100)
YELLOW = (255,228,146)
RED = (213,23,23)

# Buttons setup
btn_random = pygame.Rect(250, 115, 130, 50)
btn_real = pygame.Rect(400, 115, 100, 50)
btn_seconds = pygame.Rect(775, 115, 130, 50)
btn_words = pygame.Rect(975, 115, 90, 50)
btn_10sec = pygame.Rect(1350,115, 60, 50)
btn_30sec = pygame.Rect(1450,115, 60, 50)
btn_60sec = pygame.Rect(1550,115, 60, 50)
btn_10word = pygame.Rect(1350,115, 60, 50)
btn_20word = pygame.Rect(1450,115, 60, 50)
btn_30word = pygame.Rect(1550,115, 60, 50)

#Button Visibility
show_measure = True
show_seconds = True
show_words = False

# Current mode
mode = "random"
measure = "seconds"
seconds = 10
words = 10
def draw_button(rect, text, active=False):
    color = LIGHT_GRAY
    pygame.draw.rect(screen, color, rect)
    label = FONT.render(text, True, YELLOW if active else WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

#Shapes
rect_width, rect_height = 1500, 75
rect = pygame.Rect(WIDTH // 2 - rect_width // 2, 100, rect_width, rect_height)

#Word list
word_list = ["charge", "aftermath", "combative", "skinny", "quack", "ruin", "necessary", "knock", "four", "graet", "bag", "trot", "gleaming", "succeed", "twig", "wrist", "wave", "equal", "groan", "coast", "stay", "lumber", "brick", "canvas", "venemous", "pleasant", "sedate", "cook", "hug", "willing", "faithful", "zesty", "mixed","attack", "post", "laptop", "tiger", "wax", "rabid", "exotic", "delightful", "beginner", "birds", "difficult", "magic", "smoggy", "even", "base", "promise", "wilderness", "shrill", "awake", "brash", "experience", "reflective", "bath", "daughter", "limit", "phone", "shower", "worried", "jail", "hour", "boy", "direction", "trap", "womanly", "ground", "elfin", "spiteful", "strange", "flawless", "stinky", "advertisement", "kind", "oceanic", "girl", "value", "descriptive", "abroad", "reading", "care", "brass", "wine", "drawer", "bury", "grade", "lumpy", "languid", "tick", "vagabond", "dominating", "frog", "destiny", "balance", "language", "nail", "volley", "feeling", "storm"]

#Pre start
user_input = ""
typing_started = False
start_time = 0


#Game Loop
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if btn_random.collidepoint(mouse_pos):
                mode = "random"
                show_measure = True
                if measure == "seconds":
                    show_seconds = True
                    show_words = False
                else:
                    show_seconds = False
                    show_words = True
            elif btn_real.collidepoint(mouse_pos):
                mode = "real"
                show_measure = False
            elif show_measure and btn_seconds.collidepoint(mouse_pos):
                measure = "seconds"
                show_seconds = True
                show_words = False
            elif show_measure and btn_words.collidepoint(mouse_pos):
                measure = "words"
                show_seconds = False
                show_words = True
            elif show_measure and show_seconds and btn_10sec.collidepoint(mouse_pos):
                seconds = 10
            elif show_measure and show_seconds and btn_30sec.collidepoint(mouse_pos):
                seconds = 30
            elif show_measure and show_seconds and btn_60sec.collidepoint(mouse_pos):
                seconds = 60
            elif show_measure and show_words and btn_10word.collidepoint(mouse_pos):
                words = 10
            elif show_measure and show_words and btn_20word.collidepoint(mouse_pos):
                words = 20
            elif show_measure and show_words and btn_30word.collidepoint(mouse_pos):
                words = 30
                
    pygame.draw.rect(screen, LIGHT_GRAY, rect)
    # Draw buttons
    draw_button(btn_random, "Random", active=(mode=="random"))
    draw_button(btn_real, "Real", active=(mode=="real"))
    if show_measure:
        draw_button(btn_seconds, "Seconds", active=(measure=="seconds"))
        draw_button(btn_words, "Words", active=(measure=="words"))
    if measure == "seconds" and show_measure:
        draw_button(btn_10sec, "10", active=(seconds==10))
        draw_button(btn_30sec, "30", active=(seconds==30))
        draw_button(btn_60sec, "60", active=(seconds==60))
    elif measure == "words" and show_measure:
        draw_button(btn_10word, "10", active=(words==10))
        draw_button(btn_20word, "20", active=(words==20))
        draw_button(btn_30word, "30", active=(words==30))

    if mode == "random":
        if measure == "words":
            current_text = "".join(random.choices(word_list,k = words))
        else:
            current_text

    pygame.display.flip()

pygame.quit()
sys.exit()
