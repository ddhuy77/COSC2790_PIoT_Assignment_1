from sense_hat import SenseHat
import time
import random
from electronicDie import electronicDie

e1=electronicDie
sense = SenseHat()
def game():
    prompt_1 = input("Are you ready to play the dice game? (y/n): ")
    while prompt_1=="y" or prompt_1=="Y":
        while True:
            prompt_2 = input("Type 'Go' to decide which player to roll the dice first: ")
            if prompt_2=="Go" or prompt_2=="go":
                turn = random.randint(1,2)
                if turn==1:
                    print("Player 1 will roll first")
                else:
                    print("Player 2 will roll first")
                break
        score_1=0
        score_2=0
        if turn==1:
            while score_1 < 30 and score_2 < 30:
                print("Player 1, please shake the Pi")
                score_1+=e1.dieRoller()
                if score_1 > 0:
                    print("Player 1 has scored %d" % score_1)
                time.sleep(1)
                print("Player 2, please shake the Pi")
                score_2+=e1.dieRoller()
                if score_2 > 0:
                    print("Player 2 has scored %d" % score_2)
                time.sleep(1)
        if turn==2:
            while score_1 < 30 and score_2 < 30:
                print("Player 2, please shake the Pi")
                score_2+=e1.dieRoller()
                if score_2 > 0:
                    print("Player 2 has scored %d" % score_2)
                time.sleep(1)
                print("Player 1, please shake the Pi")
                score_1+=e1.dieRoller()
                if score_1 > 0:
                    print("Player 1 has scored %d" % score_1)
                time.sleep(1)

        if score_1 >= 30 and score_1 > score_2:
            print("The winner is Player 1 with %d points" % score_1)
        elif score_2 >= 30 and score_2 > score_1:
            print("The winner is Player 2 with %d points" % score_2)
        prompt_1 = input("Play again? (y/n)")
    sense.clear()
game()