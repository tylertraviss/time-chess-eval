import chess
import chess.engine
from typing import Optional, Tuple
import os

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
            time_threshold: Time in seconds below which time pressure starts to matter
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

    def _get_position_evaluation(self, board: chess.Board) -> float:
        """Get the position evaluation from Stockfish."""
        info = self.engine.analyse(board, chess.engine.Limit(depth=self.engine_depth))
        score = info["score"].relative.score()
        
        # Convert score to a value between -1 and 1
        # Assuming typical Stockfish scores are in centipawns
        return max(min(score / 1000, 1), -1)

    def _calculate_time_advantage(self, white_time: float, black_time: float) -> float:
        """Calculate the time advantage for white."""
        time_diff = white_time - black_time
        
        # Normalize time difference to a value between -1 and 1
        # Time advantage only matters when time is below threshold
        if abs(time_diff) < self.time_threshold:
            return 0
        
        # Scale the time difference
        return max(min(time_diff / (self.time_threshold * 2), 1), -1)

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
        
        # Combine position and time advantages
        combined_eval = (
            self.position_weight * position_eval +
            self.time_weight * time_advantage
        )
        
        # Create detailed evaluation breakdown
        eval_details = {
            "position_evaluation": position_eval,
            "time_advantage": time_advantage,
            "position_weight": self.position_weight,
            "time_weight": self.time_weight,
            "combined_evaluation": combined_eval
        }
        
        return combined_eval, eval_details 