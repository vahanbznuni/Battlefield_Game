import string
import Battlefield_Objects as obj
import Battlefield_Strings as strings
import random

NL ="\n"
strings.intro_str()
player2 = obj.Computer()
player1 = obj.Player()
print(NL + strings.ready_str + NL)
player1.battlefield.display()
input(strings.continue_str)

def check_winnter():
    if player1.check_fleet_sunk():
        winner = player2
    elif player2.check_fleet_sunk():
        winner = player1
    else:
        winner = None
    return winner

while not check_winnter():    
    print(NL*2 + strings.target_str)
    input(strings.continue_str)
    player1.target(player2)
    check_winnter()
    if check_winnter():
        print(strings.winner_str.format(check_winnter()))
    else:
        print(NL*2 + strings.incoming_str)
        input(strings.continue_str)
        player2.target(player1)
        if check_winnter():
            print(strings.winner_str.format(check_winnter()))
        else:
            input(strings.continue_str)  
    
print(strings.final_str)