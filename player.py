import pygame
import random
from constants import WHITE, BLACK, KNIGHT, BISHOP, ROOK, QUEEN

class Player():
    def __init__(self, color, board, ai=False, ai_level=1):
        self.color = color
        self.ai = ai
        self.ai_level = ai_level
        self.board = board
        self.pieces = self.board.white_pieces_on_board if self.color == WHITE else self.board.black_pieces_on_board
        self.enemy_pieces = self.board.white_pieces_on_board if self.color == BLACK else self.board.black_pieces_on_board
        self.score = 0
        self.enemy_score = 0
        self.chosen_piece = None
        self.chosen_move = None
        self.moves_calculated = 0
        self.threathening_amt = 0
        self.enemy_threathening_amt = 0
    
    def make_move(self):
        if self.board.board_state == self.board.promotion_state:
            # The chosen piece is a pawn and it has reached the 8th rank
            promoted_piece = self.chosen_piece.promote_pawn(QUEEN)
            self.board.pieces_on_board.remove(self.chosen_piece) # Remove pawn from pieces
            self.board.black_pieces_on_board.append(promoted_piece)

            self.board.move_piece(promoted_piece, promoted_piece.get_pos())
        else:
            if self.ai_level == 1:
                self.random_move()
            elif self.ai_level == 2:
                self.ai_2()
            elif self.ai_level == 3:
                self.ai_3()
                #self.minimax_test()

            self.board.move_piece(self.chosen_piece, self.chosen_move)
            self.board.set_legal_moves(self.board.pieces_on_board)
    
    # Makes random moves
    def random_move(self):
        random_piece = None

        while True:
            random_piece_index = random.randint(0, len(self.pieces)-1)
            random_piece = self.pieces[random_piece_index]

            # If the piece has available moves, break, if not try again
            if len(random_piece.available_moves) >= 1:
                break
        
        random_move_index = random.randint(0, len(random_piece.available_moves)-1)
        random_square = random_piece.available_moves[random_move_index]

        self.chosen_piece = random_piece
        self.chosen_move = random_square
    
    # Always captures a piece if possible and chooses the piece with highest value if there are move than 1 possible captures
    def ai_2(self):
        best_piece = None
        best_move = None
        move_value = 0

        # Check if player can capture a piece and choose the best one to capture
        for piece in self.pieces:
            for move in piece.available_moves:
                piece_at_move = self.board.get_piece(move)
                if piece_at_move != None and piece_at_move.value > move_value:
                    best_piece = piece
                    best_move = move
                    move_value = piece_at_move.value
        
        if best_piece != None:
            self.chosen_piece = best_piece
            self.chosen_move = best_move
        else:
            self.random_move()
    
    def minimax_test(self):
        alpha = -9999
        best_score = -9999
        best_piece = None
        best_move = None
        second_best_pieces = []
        second_best_moves = []

        beta = 9999
        worst_score = 9999
        worst_piece = None
        worst_move = None
        next_player = self.board.next_player

        for move in self.board.legal_moves:
            board_copy = self.board.copy()
            self.moves_calculated += 1
            print("Moves calculated: ", self.moves_calculated)
            board = self.board.move_piece_2(move[0], move[1])
            score = self.minimax(board, 2, alpha, beta, False)
            self.board.revert_from_copy(board_copy)

            if score > best_score:
                best_score = score
                best_piece = piece
                best_move = move

                second_best_moves = []
                second_best_moves.append(best_move)
                second_best_pieces = []
                second_best_pieces.append(best_piece)
            elif score == best_score:
                second_best_moves.append(move)
                second_best_pieces.append(piece)

            if score < worst_score:
                worst_score = score
                worst_piece = piece
                worst_move = move
    
        random_index = random.randint(0, len(second_best_moves)-1)
        self.chosen_piece = second_best_pieces[random_index]
        self.chosen_move = second_best_moves[random_index]
        self.board.player_turn = self.color
        self.board.next_player = next_player
    
    # Uses minimax
    def ai_3(self):
        alpha = -9999
        best_score = -9999
        best_piece = None
        best_move = None
        second_best_pieces = []
        second_best_moves = []

        beta = 9999
        worst_score = 9999
        worst_piece = None
        worst_move = None
        next_player = self.board.next_player

        all_possible_moves = []
        pieces_on_board = self.board.get_pieces_on_board()
        self.board.set_legal_moves(pieces_on_board)
        legal_moves = self.board.legal_moves.copy()
        print(self.color, len(legal_moves))
        for piece_move in legal_moves:
            piece, move = piece_move

            board_copy = self.board.copy(with_captured=True)
            score_copy = self.score
            enemy_score_copy = self.enemy_score
            threathening_copy = self.threathening_amt
            enemy_threathening_amt = self.enemy_threathening_amt
            self.board.move_piece(piece, move, searching=True)
            score = self.minimax(1, alpha, beta, False)
            self.board.revert_from_copy(board_copy, with_captured=True)
            self.threathening_amt = threathening_copy
            self.enemy_threathening_amt = enemy_threathening_amt
            self.score = score_copy
            self.enemy_score = enemy_score_copy

            if score > best_score:
                best_score = score
                best_piece = piece
                best_move = move

                second_best_moves = []
                second_best_moves.append(best_move)
                second_best_pieces = []
                second_best_pieces.append(best_piece)
            elif score == best_score:
                second_best_moves.append(move)
                second_best_pieces.append(piece)

            if score < worst_score:
                worst_score = score
                worst_piece = piece
                worst_move = move
        
        random_index = random.randint(0, len(second_best_moves)-1)
        self.chosen_piece = second_best_pieces[random_index]
        self.chosen_move = second_best_moves[random_index]
        self.board.player_turn = self.color
        self.board.next_player = next_player
    
    def minimax(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.board.board_state == self.board.ended_state:
            return self.score - self.enemy_score

        # Retrieving all the pieces on the board and then finding all legal moves
        pieces_on_board = self.board.get_pieces_on_board()
        self.board.set_legal_moves(pieces_on_board)
        legal_moves = self.board.legal_moves.copy()
        if maximizingPlayer:
            best_score = -9999
            for piece_move in legal_moves:
                board_copy = self.board.copy()
                score_copy = self.score
                enemy_score_copy = self.enemy_score
                threathening_copy = self.threathening_amt
                enemy_threathening_amt = self.enemy_threathening_amt
                self.board.move_piece(piece_move[0], piece_move[1], searching=True)

                score = self.minimax(depth-1, alpha, beta, False)
                self.board.revert_from_copy(board_copy)
                self.threathening_amt = threathening_copy
                self.enemy_threathening_amt = enemy_threathening_amt
                self.score = score_copy
                self.enemy_score = enemy_score_copy
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    return best_score
            return best_score
        else:
            best_score = 9999
            for piece_move in legal_moves:
                board_copy = self.board.copy()
                score_copy = self.score
                enemy_score_copy = self.enemy_score
                threathening_copy = self.threathening_amt
                enemy_threathening_amt = self.enemy_threathening_amt
                self.board.move_piece(piece_move[0], piece_move[1], searching=True)

                score = self.minimax(depth-1, alpha, beta, True)
                self.board.revert_from_copy(board_copy)
                self.threathening_amt = threathening_copy
                self.enemy_threathening_amt = enemy_threathening_amt
                self.score = score_copy
                self.enemy_score = enemy_score_copy
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    return best_score
            return best_score

    '''for piece in self.pieces:
        for move in piece.available_moves:
            self.moves_calculated += 1
            print("Moves calculated: ", self.moves_calculated)
            board_copy = self.board.copy()
            score_copy = self.score
            enemy_score_copy = self.enemy_score

            self.board.move_piece(piece, move)
            score = self.minimax((piece, move), 2, alpha, beta, False)

            self.board.revert_from_copy(board_copy)
            self.score = score_copy
            self.enemy_score = enemy_score_copy

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.board.board_state == self.board.ended_state:
            return self.score - self.enemy_score

        if maximizingPlayer:
            best_score = -9999
            for move in self.board.legal_moves:
                board_copy = self.board.copy()
                board = self.board.move_piece_2(move[0], move[1])
                score = self.minimax(board, depth-1, alpha, beta, False)
                self.board.revert_from_copy(board_copy)
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    return best_score
            return best_score
        else:
            best_score = 9999
            for move in self.board.legal_moves:
                board_copy = self.board.copy()
                self.board.move_piece_2(move[0], move[1])
                score = self.minimax(board, depth-1, alpha, beta, True)
                self.board.revert_from_copy(board_copy)
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    return best_score
            return best_score'''

