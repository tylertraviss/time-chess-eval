import chess
import chess.engine
import math
import os
from typing import Optional, Tuple

class TimeConsideringEvaluator:
    def __init__(
        self,
        stockfish_path: str,
        position_weight: float = 0.7,
        time_weight: float = 0.3,
        time_threshold: float = 60.0,  # seconds
        engine_depth: int = 20
    ):
        """
        Initialize the TimeConsideringEvaluator.

        Args:
            stockfish_path: Path to the Stockfish executable
            position_weight: Weight given to position evaluation (0-1)
            time_weight: Weight given to time advantage (0-1)
            time_threshold: Time in seconds to normalize time pressure effect
            engine_depth: Depth for Stockfish analysis
        """
        if not os.path.exists(stockfish_path):
            raise FileNotFoundError(f"Stockfish executable not found at {stockfish_path}")

        self.position_weight = position_weight
        self.time_weight = time_weight
        self.time_threshold = time_threshold
        self.engine_depth = engine_depth
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def __del__(self):
        """Clean up the engine when the object is destroyed."""
        if hasattr(self, 'engine'):
            self.engine.quit()

    def _sigmoid(self, x: float) -> float:
        """Sigmoid scaled to [-1, 1]."""
        return 2 / (1 + math.exp(-x)) - 1

    def _get_position_evaluation(self, board: chess.Board) -> float:
        """Get the position evaluation from Stockfish."""
        info = self.engine.analyse(board, chess.engine.Limit(depth=self.engine_depth))
        score = info["score"].relative.score()
        return max(min(score / 1000, 1), -1)

    def _calculate_time_advantage(self, white_time: float, black_time: float) -> float:
        """Calculate time advantage using sigmoid-normalized time difference."""
        time_diff = white_time - black_time
        normalized = time_diff / self.time_threshold
        return self._sigmoid(normalized)

    def _calculate_pressure_advantage(self, white_time: float, black_time: float) -> float:
        """Calculate time advantage based on inverse time pressure."""
        pressure_white = 1 / (white_time + 1)
        pressure_black = 1 / (black_time + 1)
        return pressure_black - pressure_white

    def evaluate(
        self,
        board: chess.Board,
        white_time: float,
        black_time: float
    ) -> Tuple[float, dict]:
        """
        Evaluate the position considering both engine evaluation and time.

        Args:
            board: The chess board position
            white_time: White's remaining time in seconds
            black_time: Black's remaining time in seconds

        Returns:
            Tuple containing:
            - float: Combined evaluation score (positive favors white)
            - dict: Detailed evaluation breakdown
        """
        position_eval = self._get_position_evaluation(board)
        time_advantage = self._calculate_time_advantage(white_time, black_time)

        combined_eval = (
            self.position_weight * position_eval +
            self.time_weight * time_advantage
        )

        eval_details = {
            "position_evaluation": position_eval,
            "time_advantage": time_advantage,
            "position_weight": self.position_weight,
            "time_weight": self.time_weight,
            "combined_evaluation": combined_eval
        }

        return combined_eval, eval_details

    def calculate_win_probability(
        self,
        board: chess.Board,
        white_time: float,
        black_time: float
    ) -> float:
        """
        Estimate White's win probability (0 to 1) using evaluation and time context.
        """
        position_eval = self._get_position_evaluation(board)
        time_advantage = self._calculate_time_advantage(white_time, black_time)

        blended = (
            self.position_weight * self._sigmoid(position_eval) +
            self.time_weight * time_advantage
        )

        return 1 / (1 + math.exp(-blended * 3))