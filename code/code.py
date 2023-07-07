"""
----- WORK IN PROGRESS ----  ça marche mais y'a encore des trucs à faire.
# éteindre tout
import time
import random
import board
import neopixel
import digitalio
pixels = neopixel.NeoPixel(board.GP16, 9)
eteint=(0, 0, 0)
pixels.fill(eteint)
"""

import time
import random
import board
import digitalio
import neopixel

# Set up the button inputs
button1 = digitalio.DigitalInOut(board.GP14)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button2 = digitalio.DigitalInOut(board.GP15)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

# Set up the neopixel strip
strip = neopixel.NeoPixel(board.GP16, 9)

# Initialize scores and game state
score1 = 0
score2 = 0
game_state = "start"
wait_time = random.uniform(5.0, 10.0)
luminosite = 0.2

rouge=(255*0.2, 0, 0)
bleu=(0, 255*0.2, 0)
vert=(0, 0, 255*0.2)
jaune=(255*0.2,255*0.2,0)
eteint=(0, 0, 0)

def update_strip():
    # Update the LED strip to show the current scores and game state
    strip.fill((0, 0, 0))
    for i in range(score1):
        strip[i] = jaune
    for i in range(score2):
        strip[8 - i] = jaune
    if game_state == "start":
        strip[4] = rouge
    elif game_state == "wait":
        strip[4] = vert
    elif game_state == "play":
        strip[4] = bleu
    strip.show()

def reset_game():
    # Reset the game state and scores
    global score1, score2, game_state
    score1 = 0
    score2 = 0
    game_state = "start"
    update_strip()

def flash_winner(winner):
    # Flash the winner's LEDs until both players press their buttons to start a new game
    while button1.value or button2.value:
        if winner == 1:
            for j in range(4):
                strip[j] = jaune
        else:
            for j in range(4):
                strip[8 - j] = jaune
        strip.show()
        time.sleep(0.5)
        if winner == 1:
            for j in range(4):
                strip[j] = eteint
        else:
            for j in range(4):
                strip[8 - j] = eteint
        strip.show()
        time.sleep(0.5)

def handle_start_state():
    # Handle the start state
    global game_state, start_time
    if not button1.value and not button2.value:
        # Animate the center LED while waiting for both players to release their buttons
        while not button1.value or not button2.value:
            strip[4] = rouge
            strip.show()
            time.sleep(0.5)
            strip[4] = vert
            strip.show()
            time.sleep(0.5)
        game_state = "wait"
        start_time = time.monotonic()
        update_strip()

def handle_wait_state():
    # Handle the wait state
    global game_state,score1,score2,start_time
    if not button1.value:
        score1 -= max(score1 - 1 , 0) # subtract one point from player one's score if they press their button during the wait state
        update_strip()
    elif not button2.value:
        score2 -= max(score2 - 1 , 0) # subtract one point from player two's score if they press their button during the wait state
        update_strip()
    elif time.monotonic() - start_time >= wait_time:
        game_state = "play"
        update_strip()

def handle_play_state():
    # Handle the play state
    global game_state,score1,score2,start_time
    if not button1.value:
        score1 += 1
        wait_time = random.uniform(5.0,10.0) # change wait_time every time a point is scored.
        update_strip()
        time.sleep(2)
        if score1 == 5:
            flash_winner(1)
            reset_game()
        else:
            game_state = "start"
            update_strip()
    elif not button2.value:
        score2 += 1
        wait_time = random.uniform(5.0,10.0) # change wait_time every time a point is scored.
        update_strip()
        time.sleep(2)
        if score2 == 5:
            flash_winner(2)
            reset_game()
        else:
            game_state = "start"
            update_strip()

while True:
    if game_state == "start":
        handle_start_state()
    elif game_state == "wait":
        handle_wait_state()
    elif game_state == "play":
        handle_play_state()

