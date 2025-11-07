import os
import sys
import time
import random

try:
    import msvcrt
    WINDOWS = True
except ImportError:
    import termios, tty, select
    WINDOWS = False

def get_keypress():
    if WINDOWS:
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8').lower()
    else:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1).lower()
    return None

def hide_cursor():
    print("\033[?25l", end="", flush=True)

def show_cursor():
    print("\033[?25h", end="", flush=True)

def move_cursor_home():
    print("\033[H", end="", flush=True)

WIDTH = 50
HEIGHT = 20
PADDLE_SIZE = 4
BALL_SPEED = 0.08

def bot_move(ball_y, paddle_y, difficulty):
    if difficulty == "einfach":
        if random.random() < 0.4:
            if ball_y > paddle_y + 2: paddle_y += 1
            elif ball_y < paddle_y: paddle_y -= 1
    elif difficulty == "normal":
        if random.random() < 0.7:
            if ball_y > paddle_y + 1: paddle_y += 1
            elif ball_y < paddle_y: paddle_y -= 1
    elif difficulty == "schwer":
        if ball_y > paddle_y + 1: paddle_y += 1
        elif ball_y < paddle_y: paddle_y -= 1
    elif difficulty == "impossible":
        paddle_y = ball_y - PADDLE_SIZE // 2
    paddle_y = max(0, min(HEIGHT - PADDLE_SIZE, paddle_y))
    return paddle_y

def game(difficulty):
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = random.choice([-1, 1]), random.choice([-1, 1])
    player_y = HEIGHT // 2 - PADDLE_SIZE // 2
    bot_y = HEIGHT // 2 - PADDLE_SIZE // 2
    player_score = 0
    bot_score = 0
    hide_cursor()
    try:
        while True:
            move_cursor_home()
            frame = []
            for y in range(HEIGHT):
                line = ""
                for x in range(WIDTH):
                    if x == 1 and player_y <= y < player_y + PADDLE_SIZE:
                        line += "|"
                    elif x == WIDTH - 2 and bot_y <= y < bot_y + PADDLE_SIZE:
                        line += "|"
                    elif int(ball_x) == x and int(ball_y) == y:
                        line += "O"
                    else:
                        line += " "
                frame.append(line)
            frame.append(f"\nPlayer: {player_score}   Bot ({difficulty}): {bot_score}")
            frame.append("Controsl: [W] up, [S] down, [Q] quit")
            print("\n".join(frame))
            key = get_keypress()
            if key == 'w':
                player_y = max(0, player_y - 1)
            elif key == 's':
                player_y = min(HEIGHT - PADDLE_SIZE, player_y + 1)
            elif key == 'q':
                break
            ball_x += ball_dx
            ball_y += ball_dy
            if ball_y <= 0 or ball_y >= HEIGHT - 1:
                ball_dy *= -1
            if ball_x <= 2 and player_y <= ball_y < player_y + PADDLE_SIZE:
                ball_dx *= -1
                ball_x = 3
            elif ball_x >= WIDTH - 3 and bot_y <= ball_y < bot_y + PADDLE_SIZE:
                ball_dx *= -1
                ball_x = WIDTH - 4
            if ball_x < 0:
                bot_score += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = 1
            elif ball_x > WIDTH:
                player_score += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT // 2
                ball_dx = -1
            bot_y = bot_move(ball_y, bot_y, difficulty)
            time.sleep(BALL_SPEED)
    finally:
        show_cursor()
        print("\Game ended!")

if __name__ == "__main__":
    print("Terminal Ping Pong")
    print("Choose a difficulty:")
    print("[1] easy\n[2] normal\n[3] hord\n[4] impossible")
    diff_choice = input(">>> ")
    diff_map = {
        "1": "easy",
        "2": "normal",
        "3": "hard",
        "4": "impossible"
    }
    difficulty = diff_map.get(diff_choice, "normal")
    os.system('cls' if WINDOWS else 'clear')
    game(difficulty)
