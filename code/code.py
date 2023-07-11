"""
# commande manuelle: éteindre tout
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

print("start...")
# description des boutons
button1 = digitalio.DigitalInOut(board.GP14)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button2 = digitalio.DigitalInOut(board.GP15)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

# description du bandeau de leds
strip = neopixel.NeoPixel(board.GP16, 9)
luminosite = 0.2
rouge=(255*0.2, 0, 0)
vert=(0, 255*0.2, 0)
bleu=(0, 0, 255*0.2)
jaune=(255*0.2,255*0.2,0)
eteint=(0, 0, 0)

# Initialisation scores et game state
score1 = 0
score2 = 0
game_state = "start"
wait_time = random.uniform(5.0, 10.0)
luminosite = 0.2

def update_strip():
    # Mise a jour bandeau led
    global score1, score2, game_state
    strip.fill(eteint)
    for i in range(score1):
        strip[i] = jaune
    for i in range(score2):
        strip[8 - i] = jaune
    if game_state == "start":
        strip[4] = rouge
    elif game_state == "wait":
        strip[4] = bleu
    elif game_state == "play":
        strip[4] = vert
    strip.show()

def wait_for_release():
    while not (button1.value and button2.value):
        strip[4] = jaune
        strip.show()
    update_strip()

def reset_game():
    # Reset game state et scores
    global score1, score2, game_state
    score1 = 0
    score2 = 0
    game_state = "start"
    update_strip()

def flash_winner(winner):
    # Flash les leds du gagnant
    
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
    wait_for_release()

def handle_start_state():

    # en attente que les joueurs soient prêts
    global game_state, start_time, button1, button2
    print(game_state)
    # Animation de la led centrale
    while button1.value or button2.value:
        strip[4] = rouge
        strip.show()
        time.sleep(0.5)
        strip[4] = jaune
        strip.show()
        time.sleep(0.5)
    # départ nouvelle manche    
    game_state = "wait"
    print(game_state)
    update_strip()
    wait_for_release()
    start_time = time.monotonic()



def handle_wait_state():
    # Handle the wait state
    global game_state,score1,score2,start_time
    if not button1.value:
        score1 = max(score1 - 1 , 0) # retire un point
        update_strip()
        wait_for_release()
    elif not button2.value:
        score2 = max(score2 - 1 , 0) # retire un point
        update_strip()
        wait_for_release()
    elif time.monotonic() - start_time >= wait_time:
        game_state = "play"
        update_strip()

def handle_play_state():
    # Handle the play state
    global game_state,score1,score2,start_time
    if not button1.value:
        score1 += 1
        wait_time = random.uniform(5.0,10.0) # change le délai à chaque fois
        update_strip()
        wait_for_release()
        if score1 == 5:
            flash_winner(1)
            reset_game()
        else:
            game_state = "start"
            update_strip()
    elif not button2.value:
        score2 += 1
        wait_time = random.uniform(5.0,10.0) # change le délai à chaque fois
        update_strip()
        wait_for_release()
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


