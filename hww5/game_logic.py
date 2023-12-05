import random

def calculate_winnings(bet_amount, selected_slot, winning_slot):
    if selected_slot == winning_slot:
        return 2 * bet_amount
    else:
        return -bet_amount

def generate_winning_slot():
    return random.randint(1, 30)