import random
from collections import defaultdict

# Histories
opponent_history = []
player_history = []

# Pattern dictionary to track opponent's move sequences
patterns = defaultdict(lambda: {'R': 0, 'P': 0, 'S': 0})

# Move counter
total_moves = 0
MAX_MOVES = 1000  # Reset after 1000 moves

def predict_next_move(opponent_history, n=3):
    """Predict the opponent's next move based on the most frequent sequence of n previous moves."""
    if len(opponent_history) < n:
        return random.choice(['R', 'P', 'S'])  # Default random choice if not enough history

    # Get the last n moves
    last_moves = tuple(opponent_history[-n:])
    
    # Get the frequencies of what the opponent played after these last_moves
    pattern = patterns.get(last_moves, {'R': 0, 'P': 0, 'S': 0})
    
    # Predict the opponent's next move by choosing the most frequent next move
    predicted_move = max(pattern, key=pattern.get)
    
    return predicted_move

def update_pattern(opponent_history, n=3):
    """Update the pattern dictionary with the opponent's moves."""
    if len(opponent_history) > n:
        last_moves = tuple(opponent_history[-(n+1):-1])  # Get the last n moves (before the most recent one)
        next_move = opponent_history[-1]  # The opponent's most recent move
        patterns[last_moves][next_move] += 1  # Update the pattern dictionary

def calculate_win_percentage(player_history, opponent_history):
    wins = 0
    defeats = 0
    
    # Ideal responses for comparison
    winning_combinations = {'R': 'S', 'S': 'P', 'P': 'R'}  # Player wins if their move beats opponent's move
    
    # Count wins and defeats (ignoring ties)
    for player_move, opponent_move in zip(player_history, opponent_history):
        if winning_combinations.get(player_move) == opponent_move:
            wins += 1  # Player wins
        elif winning_combinations.get(opponent_move) == player_move:
            defeats += 1  # Player loses (defeat)
    
    total_games = wins + defeats  # Only consider wins and defeats for percentage
    if total_games > 0:
        win_percentage = (wins / total_games) * 100
    else:
        win_percentage = 0  # Avoid division by zero if no games have been played
    
    return win_percentage

def reset_pattern():
    """Resets the pattern dictionary and histories after 1000 moves."""
    global patterns, total_moves, opponent_history, player_history
    patterns = defaultdict(lambda: {'R': 0, 'P': 0, 'S': 0})
    total_moves = 0  # Reset move counter
    opponent_history.clear()
    player_history.clear()

def player(prev_opponent_play, opponent_history=[], player_history=[]):
    global total_moves
    
    if prev_opponent_play == "" or prev_opponent_play is None:
        prev_opponent_play = random.choice(['R', 'P', 'S'])  # Randomize first move if opponent has no history

    # Update the history and pattern
    opponent_history.append(prev_opponent_play)
    update_pattern(opponent_history)

    # Predict opponent's next move based on pattern learning
    predicted_opponent_move = predict_next_move(opponent_history)
    
    # Define the ideal response to beat the predicted move
    ideal_response = {'R': 'P', 'P': 'S', 'S': 'R'}  # Counter the predicted move

    # Introduce randomness
    if random.random() > 0.052:  # introduce randomness
        response = ideal_response[predicted_opponent_move]
    else:
        response = random.choice(['R', 'P', 'S'])  # Random response occasionally

    # Append the player's move to their history
    player_history.append(response)

    # Increment total moves
    total_moves += 1

    # Reset the pattern if total moves exceed MAX_MOVES
    if total_moves >= MAX_MOVES:
        reset_pattern()

    # Return the player's move
    return response
