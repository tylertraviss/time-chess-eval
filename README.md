# Time Considering Chess Evaluator

A Python package that provides a chess evaluation bar combining engine evaluation with time pressure. This package uses Stockfish for position evaluation and incorporates time pressure to give a more complete picture of the game state.

## Features

- Stockfish-powered position evaluation
- Time pressure integration
- Customizable evaluation weights
- Easy integration with python-chess
- Detailed evaluation breakdown

## Installation

```bash
pip install time-considering-chess-evaluator
```

Note: This package requires Stockfish to be installed on your system. You can download it from [Stockfish's official website](https://stockfishchess.org/download/).

## Usage

```python
from time_considering_chess_evaluator import TimeConsideringEvaluator
import chess

# Create a board
board = chess.Board()

# Create evaluator
evaluator = TimeConsideringEvaluator(
    stockfish_path="/path/to/stockfish",  # Path to your Stockfish executable
    material_weight=0.7,
    time_weight=0.3
)

# Get evaluation with time pressure
evaluation, details = evaluator.evaluate(
    board=board,
    white_time=300,  # seconds
    black_time=300   # seconds
)

# Print detailed evaluation
print(f"Position evaluation: {details['position_evaluation']}")
print(f"Time advantage: {details['time_advantage']}")
print(f"Combined evaluation: {evaluation}")
```

## License

MIT License 