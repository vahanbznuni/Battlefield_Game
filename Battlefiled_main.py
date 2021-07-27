import string
import Battlefield_Objects as obj
import Battlefield_Strings as strings
import random

winner = None

NL ="\n"
strings.intro_str()
player2 = obj.Computer()
player1 = obj.Player()
print(NL + strings.ready_str + NL)
player1.battlefield.display()
input(strings.continue_str)

def check_winnter():
    if player1.check_fleet_sunk:
        winner = player2
    elif player2.check_fleet_sunk:
        winner = player1
    else:
        winner = None

while not winner:    
    print(NL*2 + strings.target_str)
    input(strings.continue_str)
    print(NL + strings.line_str1 + NL + strings.enemy_battlefield_str + NL)
    player2.battlefield.display()
    input1 = input(NL + strings.target_cords_str)
    target_coords = (input1[0], int(input1[1:]))
    print(NL*2 + strings.target_complete + NL)
    player2.battlefield.target(target_coords)
    check_winnter()
    if winner:
        print(strings.winner_str.format(winner))
    else:
        input(strings.continue_str)
        print(NL*2 + strings.incoming_str + NL)
        print(NL + strings.line_str1 + NL + strings.player_battlefield_str + NL)
        player1.battlefield.display()
        input(strings.continue_str)
        print(NL*2 + strings.incoming_complete+ NL)
        while True:
            try:
                rows = player1.battlefield.rows
                comp_target = (rows[random.randint(0, len(rows)-1)], random.randint(0, 10))
                player1.battlefield.target(comp_target)
                break
            except Exception:
                pass
        check_winnter()
        if winner:
            print(strings.winner_str.format(winner))
        else:
            input(strings.continue_str)  
    
print(strings.final_str)