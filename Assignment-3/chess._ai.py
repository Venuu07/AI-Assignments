import chess
from chessboard import display
import time

class State:
    def __init__(self, board=None, player=True):
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board
        self.player = player

    def isTerminal(self):
        return self.board.is_game_over()

    def moveGen(self):
        children = []
        for move in self.board.legal_moves:
            new_board = self.board.copy()
            new_board.push(move)
            children.append(State(new_board, not self.player))
        return children

    def evaluate(self):
        if self.board.is_checkmate():
            return -1000 if self.board.turn else 1000
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0

        # My evaluation function
        score = 0
        
        # 1. Piece count
        piece_values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
        }
        for piece_type in piece_values:
            score += len(self.board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
            score -= len(self.board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

        # 2. Center control
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        for sq in center_squares:
            piece = self.board.piece_at(sq)
            if piece:
                if piece.color == chess.WHITE:
                    score += 0.2
                else:
                    score -= 0.2
        
        # 3. Mobility (number of moves)
        white_moves = self.board.copy()
        white_moves.turn = chess.WHITE
        num_white_moves = len(list(white_moves.legal_moves))

        black_moves = self.board.copy()
        black_moves.turn = chess.BLACK
        num_black_moves = len(list(black_moves.legal_moves))
        
        score += 0.05 * (num_white_moves - num_black_moves)

        return score


def minimax(state, depth, alpha, beta, maximizingPlayer, maxDepth):
    if state.isTerminal() or depth == maxDepth:
        return state.evaluate(), None

    best_move = None

    if maximizingPlayer:
        maxEval = -float('inf')
        for child in state.moveGen():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, False, maxDepth)
            if eval_score > maxEval:
                maxEval = eval_score
                best_move = child.board.peek()
            alpha = max(alpha, eval_score)
            if alpha >= beta:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        for child in state.moveGen():
            eval_score, _ = minimax(child, depth + 1, alpha, beta, True, maxDepth)
            if eval_score < minEval:
                minEval = eval_score
                best_move = child.board.peek()
            beta = min(beta, eval_score)
            if alpha >= beta:
                break
        return minEval, best_move


def play_game():
    current_state = State(player=True)
    maxDepth = 3
    game_board = display.start()

    print("Artificial Intelligence – Assignment 3")
    print("Simple Chess AI")
    print("You are playing as White (enter moves in UCI format, e.g., e2e4)")

    while not current_state.isTerminal():
        display.update(current_state.board.fen(), game_board)
        if display.check_for_quit():
            break

        if current_state.player:  # Human move
            try:
                move_uci = input("Enter your move: ")
                if move_uci.lower() == 'quit':
                    break
                move = chess.Move.from_uci(move_uci)
                if move in current_state.board.legal_moves:
                    new_board = current_state.board.copy()
                    new_board.push(move)
                    current_state = State(new_board, False)
                else:
                    print("Invalid move!")
            except:
                print("Invalid format!")
        else:  # AI move
            print("AI is thinking...")
            start_time = time.time()
            _, best_move = minimax(current_state, 0, -float('inf'), float('inf'), False, maxDepth)
            end_time = time.time()
            print(f"AI thought for {end_time - start_time:.2f} seconds")

            if best_move:
                new_board = current_state.board.copy()
                new_board.push(best_move)
                current_state = State(new_board, True)
                print(f"AI plays: {best_move.uci()}")
            else:
                break

    print("\nGame over!")
    display.update(current_state.board.fen(), game_board)
    print(f"Result: {current_state.board.result()}")
    time.sleep(3)
    display.terminate()


if __name__ == "__main__":
    play_game()