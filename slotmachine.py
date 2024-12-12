from flask import Flask, render_template, jsonify, request
import random
import os

app = Flask(__name__)

# Constants
ROWS = 3
COLS = 3
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
RTP =0.9

symbol_count = {"A": 2, "B": 4, "C": 6, "D": 8, "X":10}
symbol_value = {"A": 5, "B": 4, "C": 3, "D": 2, "X":0}

# Slot machine spin logic
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

# Check winnings logic
def check_winnings(columns, lines, values, bet):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

# Serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Spin route
@app.route('/spin', methods=['POST'])
def spin():
    data = request.json
    lines = data.get('lines')
    bet = data.get('bet')
    
    # Validate input
    if not (1 <= lines <= MAX_LINES):
        return jsonify({"error": "Invalid number of lines"}), 400
    if not (MIN_BET <= bet <= MAX_BET):
        return jsonify({"error": "Invalid bet amount"}), 400

    # Calculate total bet
    total_bet = bet * lines

    # Call the function with correct arguments
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)

    # Calculate winnings
    winnings, winning_lines = check_winnings(slots, lines, symbol_value, bet)

    # Return the results
    return jsonify({
        "slots": slots,
        "winnings": winnings,
        "winning_lines": winning_lines,
        "total_bet": total_bet
    })

if __name__ == '__main__':
    app.run(debug=True)








