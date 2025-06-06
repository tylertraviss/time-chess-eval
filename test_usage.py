import chess
from time_chess_eval import TimeConsideringEvaluator


# Path to the Stockfish engine binary
STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"

# Create a sample chess position (starting position)
board = chess.Board()

# Example time values in seconds
white_time = 50.0   # White's remaining time
black_time = 50.0  # Black's remaining time

# Initialize the evaluator
evaluator = TimeConsideringEvaluator(
    stockfish_path=STOCKFISH_PATH,
    position_weight=0.7,
    time_weight=0.3,
    time_threshold=60.0,
    engine_depth=15
)

# Compute evaluation score and breakdown
combined_eval, details = evaluator.evaluate(board, white_time, black_time)

# Compute estimated win probability for White
win_prob = evaluator.calculate_win_probability(board, white_time, black_time)

# Display results
print("=== Evaluation Summary ===")
print(f"Combined Evaluation Score: {combined_eval:.3f}")
for key, value in details.items():
    if isinstance(value, float):
        print(f"{key}: {value:.3f}")
    else:
        print(f"{key}: {value}")

print("\n=== Win Probability ===")
print(f"Estimated Win Probability for White: {win_prob:.2%}")