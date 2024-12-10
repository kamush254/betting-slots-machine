
import random

# Constants defining game settings
MAX_LINES = 3  # Maximum number of betting lines
MAX_BET = 100  # Maximum allowable bet per line
MIN_BET = 1    # Minimum allowable bet per line

ROWS = 3  # Number of rows in the slot machine
COLS = 3  # Number of columns in the slot machine

# Dictionary defining the number of occurrences for each symbol
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

# Dictionary defining the value of each symbol for calculating winnings
symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

def check_winnings(columns, lines, values, bet):
    """
    Calculates the winnings based on the slot machine outcome.
    Args:
        columns: 2D list representing the slot machine columns.
        lines: Number of lines the user bet on.
        values: Dictionary of symbol values.
        bet: Amount bet on each line.
    Returns:
        Tuple of total winnings and the lines that won.
    """
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]  # Symbol from the first column on the current line
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break  # If symbols do not match, stop checking this line
        else:
            # All symbols in the line matched, calculate winnings
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)  # Line numbers are 1-indexed
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    """
    Generates a random slot machine spin.
    Args:
        rows: Number of rows in the slot machine.
        cols: Number of columns in the slot machine.
        symbols: Dictionary of symbols and their counts.
    Returns:
        2D list representing the slot machine columns after a spin.
    """
    all_symbols = []
    # Populate a list with all symbols based on their counts
    for symbol, symbol_count in symbols.items():
        all_symbols.extend([symbol] * symbol_count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)  # Ensure no duplicate symbols in a column
            column.append(value)
        columns.append(column)

    return columns

def print_slot_machine(columns):
    """
    Prints the slot machine layout in a readable format.
    Args:
        columns: 2D list representing the slot machine columns.
    """
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end="|")
            else:
                print(column[row], end="")
        print()  # Move to the next line after printing a row

def deposit():
    """
    Prompts the user to deposit money into their balance.
    Returns:
        Amount deposited as an integer.
    """
    while True:
        amount = input("What would you like to deposit? $ ")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount

def get_number_of_lines():
    """
    Prompts the user to select the number of lines to bet on.
    Returns:
        Number of lines as an integer.
    """
    while True:
        lines = input(f"Enter number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines

def get_bet():
    """
    Prompts the user to enter the bet amount per line.
    Returns:
        Bet amount as an integer.
    """
    while True:
        amount = input("What would you like to bet on each line? $ ")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a number.")
    return amount

def spins(balance):
    """
    Handles a single spin of the slot machine.
    Args:
        balance: Current balance of the user.
    Returns:
        Net change in balance after the spin.
    """
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"You don't have enough balance to bet. Your balance is: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is: ${total_bet}")
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, symbol_value, bet)
    print(f"You won ${winnings}.")
    print(f"You won on lines: ", *winning_lines)
    return winnings - total_bet

def main():
    """
    Main function to run the slot machine game.
    """
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit): ")
        if answer.lower() == "q":
            break
        balance += spins(balance)

    print(f"You left with ${balance}")

# Run the game
main()
