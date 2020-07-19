from sense_hat import SenseHat
import time
import random
from electronicDie import electronicDie
import csv

e1=electronicDie
sense = SenseHat()
class diceGame:
    def game():
        winner=""
        winner_score=0
        winner_time=0
        prompt_1 = input("Are you ready to play the dice game? (y/n): ")
        while prompt_1=="y" or prompt_1=="Y":
            while True:
                print("The first to reach 30 points after each turn of rolling the die will be the winner")
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
            time_1=0
            time_2=0
            if turn==1:
                while score_1 < 30 and score_2 < 30:
                    print("Player 1, please shake the Pi")
                    score_1+=e1.dieRoller()
                    if score_1 > 0:
                        print("Player 1 has scored %d" % score_1)
                        time_1+=1
                    time.sleep(1)
                    print("Player 2, please shake the Pi")
                    score_2+=e1.dieRoller()
                    if score_2 > 0:
                        print("Player 2 has scored %d" % score_2)
                        time_2+=1
                    time.sleep(1)
            if turn==2:
                while score_1 < 30 and score_2 < 30:
                    print("Player 2, please shake the Pi")
                    score_2+=e1.dieRoller()
                    if score_2 > 0:
                        print("Player 2 has scored %d" % score_2)
                        time_2+=1
                    time.sleep(1)
                    print("Player 1, please shake the Pi")
                    score_1+=e1.dieRoller()
                    if score_1 > 0:
                        print("Player 1 has scored %d" % score_1)
                        time_1+=1
                    time.sleep(1)

            if score_1 >= 30 and score_1 > score_2:
                print("The winner is Player 1 with %d points" % score_1)
                winner="Player 1"
                winner_score=score_1
                winner_time=time_1
            elif score_2 >= 30 and score_2 > score_1:
                print("The winner is Player 2 with %d points" % score_2)
                winner="Player 2"
                winner_score=score_2
                winner_time=time_2
            prompt_1 = input("Play again? (y/n)")
        sense.clear()
        row_list = [["Time (Number of Try)", "Winner", "Score"],
                    [winner_time, winner, winner_score]]
        with open('winner.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

d = diceGame
d.game()