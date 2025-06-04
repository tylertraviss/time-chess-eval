import chess
from time_chess_eval import TimeConsideringEvaluator

def main():
    
    board = chess.Board()    
    
    evaluator = TimeConsideringEvaluator(
        stockfish_path="/opt/homebrew/bin/stockfish",
        position_weight=0.7,
        time_weight=0.3
    )
    
    # Test initial position
    print("\nTesting initial position:")
    eval_score, details = evaluator.evaluate(
        board=board,
        white_time=300,  # 5 minutes
        black_time=300   # 5 minutes
    )
    print(f"Combined evaluation: {eval_score:.3f}")
    print(f"Position evaluation: {details['position_evaluation']:.3f}")
    print(f"Time advantage: {details['time_advantage']:.3f}")
    
    # Test a position with white advantage
    print("\nTesting position with white advantage:")
    board.set_fen("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
    eval_score, details = evaluator.evaluate(
        board=board,
        white_time=300,
        black_time=300
    )
    print(f"Combined evaluation: {eval_score:.3f}")
    print(f"Position evaluation: {details['position_evaluation']:.3f}")
    print(f"Time advantage: {details['time_advantage']:.3f}")
    
    # Test time pressure
    print("\nTesting time pressure:")
    eval_score, details = evaluator.evaluate(
        board=board,
        white_time=300,  # 5 minutes
        black_time=60    # 1 minute
    )
    print(f"Combined evaluation: {eval_score:.3f}")
    print(f"Position evaluation: {details['position_evaluation']:.3f}")
    print(f"Time advantage: {details['time_advantage']:.3f}")

if __name__ == "__main__":
    main() 