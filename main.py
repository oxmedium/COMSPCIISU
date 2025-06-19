import pygame
import sys
import time
import random
import nltk

# Download necessary NLTK corpora
nltk.download('gutenberg')
nltk.download('reuters')
nltk.download('punkt')
nltk.download('webtext')

from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize, word_tokenize

# Initialize Pygame
pygame.init()

# Screen setup
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h - 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BetterYou")

# Fonts and colors
FONT = pygame.font.Font(None, 32)
BIG_FONT = pygame.font.Font(None, 48)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)
YELLOW = (255, 228, 146)
RED = (213, 23, 23)

# End Messages
end_messages = ["I mean you did alright I guess, could probably do better though.",
                 "Imagine you moved your fingers just a little faster.",
                 "You know you could do better than that.",
                 "I mean if you're fine with that wpm and accuracy...",
                 "You won't win an argument with THAT wpm.",
                 "You lowkey slow but highkey thats ok.",
                 "I mean you gotta start somewhere right.",
                 "Atleast get 3 digits bro 😭🙏.",
                 "You cannot be satisfied with just 2 digits right.",
                 "If you keep trying you'll get 3 digits one day, just not today.",
                 "You were AFK right?",
                 "Bro thinks typing was invented yesterday get on the grind gang.", 
                 "You know if you actually got 3 digits you'd see nicer messages right(no you won't)",
                 "If you are doing cs as a job you are cooked buddy."]

end_messages2 = ["Wow you got 3 digits, you could probbaly get 4 though.",
                 "You could probably go higher if you really wanted too.",
                 "Always reach for more - some guy on the internet.",
                 "Maybe you won't be cooked working in cs.",
                 ]

# Button rectangles (UI layout)
btn_random = pygame.Rect(WIDTH * 0.12, 115, 120, 50)
btn_real = pygame.Rect(WIDTH * 0.22, 115, 80, 50)
btn_seconds = pygame.Rect(WIDTH * 0.41, 115, 130, 50)
btn_words = pygame.Rect(WIDTH * 0.51, 115, 90, 50)
btn_10sec = pygame.Rect(WIDTH * 0.75, 115, 60, 50)
btn_30sec = pygame.Rect(WIDTH * 0.8, 115, 60, 50)
btn_60sec = pygame.Rect(WIDTH * 0.85, 115, 60, 50)
btn_10word = pygame.Rect(WIDTH * 0.75, 115, 60, 50)
btn_20word = pygame.Rect(WIDTH * 0.8, 115, 60, 50)
btn_30word = pygame.Rect(WIDTH * 0.85, 115, 60, 50)

# Constants for layout
NUM_WORDS_PER_ROW = 10
NUM_ROWS = 3
num_rows = NUM_ROWS
LINE_HEIGHT = 80
TOP_OFFSET = (HEIGHT - num_rows * LINE_HEIGHT) // 2

# Button visibility toggles
show_measure = True
show_seconds = True
show_words = False

# Test configuration
mode = "random"          # either "random" or "real"
measure = "seconds"      # either "seconds" or "words"
seconds = 10             # test duration if time-based
words = 10               # word goal if word-count-based

def draw_button(rect, text, active=False):
    """
    Draws a rectangular button with the given text and visual state.
    
    Args:
        rect (pygame.Rect): Button area.
        text (str): Button label.
        active (bool): Whether the button is currently selected.
    """
    color = LIGHT_GRAY
    pygame.draw.rect(screen, color, rect)
    label = FONT.render(text, True, YELLOW if active else WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

# Typing box rectangle
rect_width, rect_height = WIDTH * 0.80, HEIGHT * 0.08
rect = pygame.Rect(WIDTH // 2 - rect_width // 2, 100, rect_width, rect_height)

# Default word list (used in random mode)
word_list = ["charge", "each", "the", "skinny", "quack", "ruin", "me", "knock", "four", "great", "bag",
             "trot", "gleaming", "succeed", "twig", "wrist", "wave", "equal", "groan", "coast", "stay", "lumber",
             "brick", "canvas", "car", "pleasant", "sedate", "cook", "hug", "willing", "faithful", "zesty",
             "mixed", "attack", "post", "laptop", "tiger", "wax", "rabid", "exotic", "him", "beginner", "birds",
             "difficult", "magic", "smoggy", "even", "base", "promise", "her", "shrill", "awake", "brash",
             "hard", "easy", "bath", "daughter", "limit", "phone", "shower", "worried", "jail", "hour",
             "boy", "direction", "trap", "womanly", "ground", "elfin", "spiteful", "strange", "flawless", "stinky",
             "hello", "kind", "oceanic", "girl", "value", "world", "abroad", "reading", "care", "brass",
             "wine", "drawer", "bury", "grade", "lumpy", "in", "tick", "son", "dominating", "frog", "destiny",
             "balance", "language", "nail", "volley", "feeling", "storm", "there", "cool", "python", "conquer", "deceit",
             "blade", "sword", "phone", "table", "unicorn", "stars", "paper", "polish", "vacuum", "notebook", "painting",
             "pencil", "red", "orange", "yellow", "dream", "green", "blue", "purple", "indigo", "direct", "mental", "refuse", 
             "falter", "knight", "quick", "stone", "foul", "soap", "game", "swift", "ball", "nurse", "panda", "snow",
             "pepper", "cacao", "bean", "strawberry", "blueberry", "coconut", "dragon", "fruit", "sugar", "apple", "ember",
             "lily", "mango", "moon", "venus", "pumpkin", "watermelon", "bamboo", "carrot", "tomato", "rose", "pearl", 
             "peach", "rotund", "devil", "lard", "little", "one", "day", "bounce", "cherry", "blossom", "treat", "point", 
             "ninja", "steam", "turtle", "penguin", "fox", "crush", "candy", "light", "mysterious", "guess"]

# Game state variables
show_cursor = False
user_input = ""
typing_started = False
start_time = 0
test_duration = seconds
test_ended = False
words_typed = 0
final_wpm = 0
final_typed_words = []
current_word_global_index = 0
current_row_index = 0
current_word_index = 0
elapsed_time = 0
typed_words = [""] * (num_rows * NUM_WORDS_PER_ROW)
real_mode_rows_backup = []
scroll_offset = 0

def generate_words(n):
    """
    Generates a list of `n` random words from the word list.
    
    Args:
        n (int): Number of words.
    Returns:
        list of str: Randomly selected words.
    """
    return random.choices(word_list, k=n)

# Generate initial rows
rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]

# Colors for each character (used to show correctness)
char_colors = [
    [[LIGHT_GRAY] * len(word) for word in row]
    for row in rows
]

def update_colors_for_word(row_idx, word_idx, user_input_word):
    """
    Updates the color of characters for a specific word based on user input.
    
    Args:
        row_idx (int): Row index of the word.
        word_idx (int): Word index in the row.
        user_input_word (str): The current typed word.
    """
    if row_idx < 0 or row_idx >= len(rows):
        return
    if word_idx < 0 or word_idx >= len(rows[row_idx]):
        return

    correct_word = rows[row_idx][word_idx]
    colors = []

    for k in range(max(len(correct_word), len(user_input_word))):
        if k < len(user_input_word):
            if k < len(correct_word) and user_input_word[k] == correct_word[k]:
                colors.append(WHITE)
            else:
                colors.append(RED)
        else:
            colors.append(LIGHT_GRAY)
    
    if 0 <= row_idx < len(char_colors) and 0 <= word_idx < len(char_colors[row_idx]):
        char_colors[row_idx][word_idx] = colors

def init_char_colors(rows):
    """
    Initializes the character colors for each word in each row.
    
    Args:
        rows (list of list of str): The words to type.
    Returns:
        list: Nested list of color arrays for each character.
    """
    char_colors = []
    for row in rows:
        row_colors = []
        for word in row:
            row_colors.append([LIGHT_GRAY] * len(word))
        char_colors.append(row_colors)
    return char_colors

def draw_rows():
    """
    Draws all the rows of words to the screen, including character coloring
    and the blinking input cursor.
    """
    global scroll_offset
    for i in range(num_rows):
        row_idx = i + scroll_offset
        if row_idx >= len(rows):
            break
        row = rows[row_idx]
        y = TOP_OFFSET + i * LINE_HEIGHT
        x = WIDTH // 2
        rendered_items = []
        cursor_pos = None
        running_length = 0

        for j, word in enumerate(row):
            word_surfaces = []
            if row_idx < len(char_colors) and j < len(char_colors[row_idx]):
                colors = char_colors[row_idx][j]
                for k, char in enumerate(word):
                    color = colors[k] if k < len(colors) else LIGHT_GRAY
                    surface = BIG_FONT.render(char, True, color)
                    word_surfaces.append((surface, color))
                if row_idx == current_row_index + scroll_offset and j == current_word_index:
                    cursor_pos = running_length + len(user_input)
            else:
                for char in word:
                    surface = BIG_FONT.render(char, True, LIGHT_GRAY)
                    word_surfaces.append((surface, LIGHT_GRAY))

            space_surface = BIG_FONT.render(" ", True, LIGHT_GRAY)
            word_surfaces.append((space_surface, LIGHT_GRAY))
            rendered_items.extend(word_surfaces)
            running_length += len(word_surfaces)

        total_width = sum(surf.get_width() for surf, _ in rendered_items)
        start_x = x - total_width // 2
        cursor_x = start_x

        for idx, (surface, color) in enumerate(rendered_items):
            screen.blit(surface, (start_x, y))
            if row_idx == current_row_index + scroll_offset and idx == cursor_pos:
                cursor_x = start_x
            start_x += surface.get_width()

        if row_idx == current_row_index + scroll_offset and cursor_pos is not None and show_cursor:
            cursor_surface = BIG_FONT.render("|", True, YELLOW)
            screen.blit(cursor_surface, (cursor_x, y))

def update_layout():
    """
    Recalculates vertical centering for the word rows when number of rows changes.
    """
    global TOP_OFFSET
    TOP_OFFSET = (HEIGHT - num_rows * LINE_HEIGHT) // 2

update_layout()

def reset_test(keep_rows=True):
    """
    Resets the typing test state, including input, row data, and timers.
    
    Args:
        keep_rows (bool): If True, retain previous row content.
    """
    global user_input, typing_started, test_ended, current_word_index, words_typed, show_cursor
    global typed_words, char_colors, final_wpm, final_typed_words, elapsed_time
    global current_word_global_index, current_row_index, rows, num_rows, scroll_offset, start_time

    show_cursor = False
    user_input = ""
    typing_started = False
    test_ended = False
    current_word_index = 0
    words_typed = 0
    final_wpm = 0
    final_typed_words = []
    current_word_global_index = 0
    current_row_index = 0
    elapsed_time = 0
    scroll_offset = 0
    start_time = 0 

    # Set number of rows based on mode
    if measure == "words":
        num_rows = max(1, words // NUM_WORDS_PER_ROW)
    elif measure == "seconds":
        num_rows = NUM_ROWS
        if mode == "real" and real_mode_rows_backup and keep_rows:
            rows = [row[:] for row in real_mode_rows_backup]
            num_rows = len(rows)
        else:
            rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
    else:
        rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]

    typed_words = [""] * (num_rows * NUM_WORDS_PER_ROW)
    char_colors = init_char_colors(rows)
    update_layout()

def get_sentences(min_words=30, max_words=50, words_per_row=NUM_WORDS_PER_ROW):
    """
    Extracts a list of real sentences from NLTK's 'austen-emma.txt' corpus
    and tokenizes them into word groups for display.
    
    Args:
        min_words (int): Minimum total words to retrieve.
        max_words (int): Max limit to avoid very long texts.
        words_per_row (int): Number of words in each row.
    
    Returns:
        list[list[str]]: Words chunked into rows.
    """
    text = gutenberg.raw('austen-emma.txt')
    sentences = sent_tokenize(text)

    combined_words = []
    i = 0

    while i < len(sentences) and len(combined_words) < min_words:
        raw_words = word_tokenize(sentences[i])
        sentence_words = []
        for w in raw_words:
            # Attach punctuation to the previous word
            if w in [".", ",", "!", "?", ":", ";", "'", "\"", "’"] and sentence_words:
                sentence_words[-1] += w
            else:
                sentence_words.append(w)
        combined_words.extend(sentence_words)
        i += 1

    if len(combined_words) > max_words:
        combined_words = combined_words[:max_words]

    return chunk_words(combined_words, size=words_per_row)

def chunk_words(words, size=10):
    """
    Breaks a list of words into smaller lists (rows) of given size.
    
    Args:
        words (list): The flat word list.
        size (int): Words per chunk/row.
    
    Returns:
        list of list of str: Word rows.
    """
    return [words[i:i+size] for i in range(0, len(words), size)]

def calculate_wpm(typed_words, start_time):
    """
    Calculates the words per minute from typed input.
    
    Args:
        typed_words (list): List of typed words.
        start_time (float): Timestamp when typing began.
    
    Returns:
        int: WPM rounded to nearest integer.
    """
    total_chars = sum(len(word) for word in typed_words)
    elapsed_minutes = (time.time() - start_time) / 60
    if elapsed_minutes == 0:
        return 0
    wpm = (total_chars / 4) / elapsed_minutes
    return round(wpm)

def calculate_acc(typed_words, target_words):
    """
    Calculates typing accuracy as a percentage of correct characters.
    
    Args:
        typed_words (list): User-typed words.
        target_words (list): Expected correct words.
    
    Returns:
        int: Accuracy percentage.
    """
    correct_chars = 0
    total_chars = 0

    for i in range(len(typed_words)):
        typed = typed_words[i] if i < len(typed_words) else ""
        target = target_words[i] if i < len(target_words) else ""

        for j in range(max(len(typed), len(target))):
            if j < len(typed) and j < len(target):
                if typed[j] == target[j]:
                    correct_chars += 1
            total_chars += 1

    if total_chars == 0:
        return 0
    return round((correct_chars / total_chars) * 100)

# ========== MAIN GAME LOOP ==========

running = True
while running:
    screen.fill(GRAY)  # Clear screen each frame

    # -------- EVENT HANDLING --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Handle when test has ended
            if test_ended:
                if event.key == pygame.K_TAB:
                    reset_test()
                    continue
                elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                    # Generate new words
                    if measure == "words":
                        num_rows = max(1, words // NUM_WORDS_PER_ROW)
                        update_layout()
                        rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
                    else:
                        num_rows = NUM_ROWS
                        update_layout()
                        rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
                    reset_test()
                    continue
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    continue
                else:
                    continue  # Ignore other keys if test is over

            else:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Start test on first key press
            if not typing_started and event.unicode.isprintable():
                typing_started = True
                start_time = time.time()

            # --- BACKSPACE key ---
            if event.key == pygame.K_BACKSPACE:
                if user_input:
                    user_input = user_input[:-1]
                    typed_words[current_word_global_index] = user_input
                elif current_word_global_index > 0:
                    current_word_global_index -= 1
                    words_typed = max(0, words_typed - 1)
                    current_word_index = current_word_global_index % NUM_WORDS_PER_ROW
                    current_row_index = current_word_global_index // NUM_WORDS_PER_ROW
                    user_input = typed_words[current_word_global_index]
                update_colors_for_word(current_row_index, current_word_index, user_input)

            # --- SPACE key: Word completed ---
            elif event.key == pygame.K_SPACE:
                typed_words[current_word_global_index] = user_input.strip()
                words_typed += 1

                current_word_global_index += 1
                current_row_index = current_word_global_index // NUM_WORDS_PER_ROW
                current_word_index = current_word_global_index % NUM_WORDS_PER_ROW
                user_input = ""

                # In 'random + seconds' mode, scroll after 2nd row
                if measure == "seconds" and mode == "random" and current_row_index >= 2:
                    rows.pop(0)
                    rows.append(generate_words(NUM_WORDS_PER_ROW))
                    typed_words = typed_words[NUM_WORDS_PER_ROW:] + [""] * NUM_WORDS_PER_ROW
                    char_colors.pop(0)
                    char_colors.append([[LIGHT_GRAY] * len(word) for word in rows[-1]])
                    current_row_index = 1
                    current_word_global_index = NUM_WORDS_PER_ROW + current_word_index

                typed_words += [""] * NUM_WORDS_PER_ROW
                update_colors_for_word(current_row_index, current_word_index, user_input)

                # End test if in words mode and reached target
                if measure == "words" and words_typed >= words:
                    test_ended = True
                    typing_started = False
                    final_typed_words = typed_words[:current_word_global_index]
                    final_wpm = calculate_wpm(final_typed_words, start_time)
                    if final_wpm < 100:
                        final_message = random.choice(end_messages)
                    else:
                        final_message = random.choice(end_messages2)

            # --- TAB key: Retry test ---
            elif event.key == pygame.K_TAB:
                reset_test(keep_rows=(measure != "seconds" or mode != "random"))
                char_colors = init_char_colors(rows)

            # --- CTRL key: New word set ---
            elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                if mode == "real":
                    all_sentences = get_sentences(min_words=100, max_words=150, words_per_row=NUM_WORDS_PER_ROW)
                    if all_sentences:
                        rows = all_sentences
                        real_mode_rows_backup = [row[:] for row in all_sentences]
                        num_rows = len(all_sentences)
                    else:
                        rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(NUM_ROWS)]
                        num_rows = NUM_ROWS
                elif measure == "words":
                    num_rows = max(1, words // NUM_WORDS_PER_ROW)
                    rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
                else:
                    rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(NUM_ROWS)]
                reset_test(keep_rows=False)
                char_colors = init_char_colors(rows)

            # --- Printable characters: Typing ---
            elif event.unicode.isprintable():
                user_input += event.unicode
                show_cursor = True
                typed_words[current_word_global_index] = user_input
                update_colors_for_word(current_row_index, current_word_index, user_input)

                # If user finishes all words in real mode or word mode, end test
                if mode == "real":
                    total_words = sum(len(row) for row in rows)
                    if current_word_global_index == total_words - 1:
                        target_word = rows[current_row_index][current_word_index]
                        if user_input == target_word:
                            test_ended = True
                            typing_started = False
                            final_typed_words = typed_words[:current_word_global_index + 1]
                            final_wpm = calculate_wpm(final_typed_words, start_time)
                            if final_wpm < 100:
                                final_message = random.choice(end_messages)
                            else:
                                final_message = random.choice(end_messages2)
                elif measure == "words":
                    if words_typed == words - 1:
                        target_word = rows[current_row_index][current_word_index]
                        if user_input == target_word:
                            test_ended = True
                            typing_started = False
                            final_typed_words = typed_words[:current_word_global_index + 1]
                            final_wpm = calculate_wpm(final_typed_words, start_time)
                            if final_wpm < 100:
                                final_message = random.choice(end_messages)
                            else:
                                final_message = random.choice(end_messages2)

        # -------- BUTTON HANDLING --------
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # Mode toggle: Random or Real
            if btn_random.collidepoint(mouse_pos):
                mode = "random"
                show_measure = True
                show_seconds = measure == "seconds"
                show_words = not show_seconds
                num_rows = NUM_ROWS if measure == "seconds" else max(1, words // NUM_WORDS_PER_ROW)
                update_layout()
                rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
                char_colors = init_char_colors(rows)
                reset_test(keep_rows=True)

            elif btn_real.collidepoint(mouse_pos):
                mode = "real"
                show_measure = False
                all_sentences = get_sentences(min_words=100, max_words=150, words_per_row=NUM_WORDS_PER_ROW)
                if all_sentences:
                    rows = all_sentences
                    real_mode_rows_backup = [row[:] for row in all_sentences]
                    num_rows = len(all_sentences)
                else:
                    rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(NUM_ROWS)]
                    num_rows = NUM_ROWS
                reset_test(keep_rows=True)
                char_colors = init_char_colors(rows)

            # Measure toggle: Seconds or Words
            elif show_measure and btn_seconds.collidepoint(mouse_pos):
                measure = "seconds"
                show_seconds = True
                show_words = False
                num_rows = NUM_ROWS
                update_layout()
                rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
                reset_test()

            elif show_measure and btn_words.collidepoint(mouse_pos):
                measure = "words"
                show_seconds = False
                show_words = True
                num_rows = max(1, words // NUM_WORDS_PER_ROW)
                update_layout()
                rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
                reset_test()

            # Time selection buttons
            elif show_measure and show_seconds and btn_10sec.collidepoint(mouse_pos):
                reset_test()
                seconds = 10
            elif show_measure and show_seconds and btn_30sec.collidepoint(mouse_pos):
                reset_test()
                seconds = 30
            elif show_measure and show_seconds and btn_60sec.collidepoint(mouse_pos):
                reset_test()
                seconds = 60

            # Word count buttons
            elif show_measure and show_words and btn_10word.collidepoint(mouse_pos):
                words = 10
                num_rows = max(1, words // NUM_WORDS_PER_ROW)
                update_layout()
                rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
                reset_test(keep_rows=False)

            elif show_measure and show_words and btn_20word.collidepoint(mouse_pos):
                words = 20
                num_rows = max(1, words // NUM_WORDS_PER_ROW)
                update_layout()
                rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
                reset_test(keep_rows=False)

            elif show_measure and show_words and btn_30word.collidepoint(mouse_pos):
                words = 30
                num_rows = max(1, words // NUM_WORDS_PER_ROW)
                update_layout()
                rows = [generate_words(NUM_WORDS_PER_ROW) for _ in range(num_rows)]
                reset_test(keep_rows=False)

    # -------- TIMER CHECK (for seconds mode) --------
    if typing_started and not test_ended and measure == "seconds" and mode == "random":
        elapsed_time = time.time() - start_time
        if elapsed_time >= seconds:
            test_ended = True
            typing_started = False
            final_typed_words = typed_words[:current_word_global_index + 1]
            final_wpm = calculate_wpm(final_typed_words, start_time)
            if final_wpm < 100:
                final_message = random.choice(end_messages)
            else:
                final_message = random.choice(end_messages2)

    # -------- DRAWING UI --------
    pygame.draw.rect(screen, LIGHT_GRAY, rect)
    draw_button(btn_random, "Random", active=(mode == "random"))
    draw_button(btn_real, "Real", active=(mode == "real"))

    if show_measure:
        draw_button(btn_seconds, "Seconds", active=(measure == "seconds"))
        draw_button(btn_words, "Words", active=(measure == "words"))

    if measure == "seconds" and show_measure:
        draw_button(btn_10sec, "10", active=(seconds == 10))
        draw_button(btn_30sec, "30", active=(seconds == 30))
        draw_button(btn_60sec, "60", active=(seconds == 60))
    elif measure == "words" and show_measure:
        draw_button(btn_10word, "10", active=(words == 10))
        draw_button(btn_20word, "20", active=(words == 20))
        draw_button(btn_30word, "30", active=(words == 30))

    # Render the words
    draw_rows()

    # Show timer or word progress
    if measure == "seconds" and mode == "random":
        if typing_started and not test_ended:
            timer_text = f"{round(seconds - elapsed_time)}s"
        elif test_ended:
            timer_text = "0s"
        else:
            timer_text = f"{seconds}s"
        timer_surface = FONT.render(timer_text, True, LIGHT_GRAY)
        screen.blit(timer_surface, (WIDTH * 0.95, HEIGHT * 0.93))

    elif measure == "words" and mode == "random":
        words_text = f"{words_typed}/{words}"
        words_surface = FONT.render(words_text, True, LIGHT_GRAY)
        screen.blit(words_surface, (WIDTH * 0.95, int(HEIGHT * 0.93)))

    # Retry / New Word Set hint
    hint_surface = FONT.render("Press [Tab] to Retry  |  [CTRL] for New Words", True, LIGHT_GRAY)
    screen.blit(hint_surface, (WIDTH // 2 - hint_surface.get_width() // 2, HEIGHT * 0.93))

    # -------- FINAL RESULT SCREEN --------
    if test_ended:
        screen.fill(GRAY)
        result_text = BIG_FONT.render(final_message, True, LIGHT_GRAY)
        
        wpm_text = BIG_FONT.render(f"WPM: {final_wpm}", True, LIGHT_GRAY)
        target_text = [word for row in rows for word in row]
        accuracy_text = BIG_FONT.render(f"Acc: {calculate_acc(final_typed_words, target_text)}%", True, LIGHT_GRAY)

        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        result_rect = result_text.get_rect(center=(center_x, center_y - 80))
        wpm_rect = wpm_text.get_rect(center=(center_x, center_y - 20))
        acc_rect = accuracy_text.get_rect(center=(center_x, center_y + 40))

        screen.blit(result_text, result_rect)
        screen.blit(wpm_text, wpm_rect)
        screen.blit(accuracy_text, acc_rect)

        hint_surface = FONT.render("Press [Tab] to Retry  |  [CTRL] for New Words", True, LIGHT_GRAY)
        hint_rect = hint_surface.get_rect(center=(center_x, HEIGHT * 0.93))
        screen.blit(hint_surface, hint_rect)
    pygame.display.flip()  # Update display

# Exit Pygame
pygame.quit()
sys.exit()