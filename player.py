import pygame
import random
from constants import WHITE, BLACK, KNIGHT, BISHOP, ROOK, QUEEN, ENPASSANT, PAWN, KING

class Player():
    def __init__(self, color, board, ai=False, ai_level=1, depth=1):
        self.color = color
        self.enemy_color = BLACK if color == WHITE else WHITE
        self.ai = ai
        self.ai_level = ai_level
        self.depth = depth
        self.positions_calculated = 0

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

        self.success = True

    def make_move(self):
        if self.board.board_state == self.board.promotion_state:
            # The chosen piece is a pawn and it has reached the 8th rank
            promoted_piece = self.chosen_piece.promote_pawn(QUEEN)
            self.board.pieces_on_board.append(promoted_piece)
            self.board.pieces_on_board.remove(self.chosen_piece) # Remove pawn from pieces
            self.board.black_pieces_on_board.append(promoted_piece)

            self.board.move_piece(promoted_piece, promoted_piece.get_pos())
        else:
            if self.ai_level == 1:
                self.random_move()
            elif self.ai_level == 2:
                self.ai_2()
            elif self.ai_level == 3:
                self.chosen_piece, self.chosen_move = self.best_move_minimax()
            elif self.ai_level == 4:
                self.chosen_piece, self.chosen_move = self.best_move()


            self.board.move_piece(self.chosen_piece, self.chosen_move, ai_move=True)
            self.board.prepare_next_player()
    
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
    
    # Uses minimax
    # Current where we create a new grid in memory everytime a move is checked TIME PR. MOVE: 11.6
    # Note: The alg works now but will give a lot of dumb predictions because, for instance if white is last move in search,
    # a queen or any other piece can capture without black being able to capture back because of depth of search. Therefore white always have an advantage in this way, as a queen taking a pawn that could be taken in the next move would be evaluated as -1.
    # This is kind of unimportant since that when it's whites turn and goes through possible moves, the line that was previously evaluated as -1 for black would be completely different,
    # Because now white can look one more move ahead and see that the queen would be captured and result in -8 for white, +1 for black. This line would never be take place, thats why scores in debug don't mean much, unless they are very abnormal.
    
    # v0: When we were copying grid between every move checked
    # Time first move depth 3: e4: 46587159
    # v1: Added board.push(move), pop()
    # SESSION 1 MAC
    # Time first move depth 3: e4: 30469883, d4: 21575864, e4: 30347339, Nf3: 13407581, d3: 26173633, h4: 15341103
    # v2: Removed switch_turn() from move_piece() and pop(), as well as threathening_amt for efficiency
    # SESSION 1 MAC
    # Time first move depth 3: e4: 30119264, d4: 21359617, e4: 30119906, Nf3: 13287239, d3: 25932327, h4: 15324308, e4 WO a-b pruning: 154874391 (124754485 difference)
    # 39281578 current e4 after fixing en passant (bad way)
    # 37174022 current e4
    # v3: Now we are checking if a piece is giving check directly from the update_available_moves() function instead of doing it with update_and_add_available_moves().
    #     update_and_add_available_moves() was slow because it first updated all the possible_moves, and then looped through all of them again while checking if the move puts enemy in check
    # Time first move depth 3: e4: 32298070, 31599344
    # v4: In previous versions we weren't doing alpha beta pruning on the first move, in this version we are keeping track of alpha and beta from the first move
    #     The way of retrieving legal moves is also slightly different. Now instead of using the get_pieces_on_board() function, we do that directly in the legal_moves function
    #     We also don't set the member variable self.legal_moves in board, but instead just return a list with the legal moves. That way we don't have to copy it everytime
    # Time first move depth 3: e4: 24579274, d4: 12306503, e4: 24357332, Nf3: 5415130, d3: 10864682, h4: 3079938

    #@profile # Use kernprof -l -v main.py command to use it
    def best_move_minimax(self):
        alpha = -9999
        best_score = -9999
        self.chosen_piece = None
        self.chosen_move = None
        best_piece = None
        best_move = None
        second_best_pieces = []
        second_best_moves = []

        beta = 9999
        worst_score = 9999
        worst_piece = None
        worst_move = None

        all_possible_moves = []
        player_pieces, enemy_pieces = self.board.get_pieces_on_board(self.color)
        self.board.set_legal_moves(self.color, player_pieces, enemy_pieces)
        legal_moves = self.board.legal_moves.copy() # Copy is slow???
        #print(self.color, len(legal_moves))
        for piece_move in legal_moves:
            piece, move = piece_move

            self.board.move_piece(piece, move, searching=True)
            score = self.minimax_v2(self.depth, alpha, beta, False)
            self.board.pop(searching=True)

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
        
        print(best_score)
        if len(second_best_moves)-1 == 0:
            pass
        piece, move = self.choose_best_move(second_best_pieces, second_best_moves)
        '''self.chosen_piece = best_piece
        self.chosen_move = best_move'''
        self.board.player_turn = self.color
        self.board.next_player = self.enemy_color
        if self.success:
            print("SUCCESS!!")
        else:
            print("FAILED")
        
        print(self.positions_calculated)
        return piece, move
    
     #@profile
    def minimax_v2(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.board.board_state == self.board.ended_state:
            #before_score = self.score - self.enemy_score
            self.positions_calculated += 1
            before_score = self.board.board_score * self.color
            after_score = self.board.evaluate_board(self.color)
            if after_score != before_score:
                self.success = False

            return before_score

        # Retrieving all the pieces on the board and then finding all legal moves
        if maximizingPlayer:
            player_pieces, enemy_pieces = self.board.get_pieces_on_board(self.color)
            self.board.set_legal_moves(self.color, player_pieces, enemy_pieces)
            legal_moves = self.board.legal_moves.copy()
            best_score = -9999

            for piece_move in legal_moves:
                self.board.move_piece(piece_move[0], piece_move[1], searching=True)
                score = self.minimax_v2(depth-1, alpha, beta, False)
                self.board.pop(searching=True)

                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    return best_score
            return best_score
        else:
            player_pieces, enemy_pieces = self.board.get_pieces_on_board(self.enemy_color)
            self.board.set_legal_moves(self.enemy_color, player_pieces, enemy_pieces)
            legal_moves = self.board.legal_moves.copy()
            best_score = 9999

            for piece_move in legal_moves:
                self.board.move_piece(piece_move[0], piece_move[1], searching=True)
                score = self.minimax_v2(depth-1, alpha, beta, True)
                self.board.pop(searching=True)

                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    return best_score

            return best_score

    def choose_best_move(self, pieces, moves):
        best_piece = None
        best_move = None
        
        for i in range(len(moves)):
            piece = pieces[i]
            move = moves[i]
            this_move = False
            '''if piece.type == PAWN:
                self.chosen_piece = piece
                self.chosen_move = move'''
            if (piece.type == KNIGHT or piece.type == BISHOP or piece.type == QUEEN) and piece.first_move:
                this_move = True
            elif piece.type == PAWN and (piece.col == 3 or piece.col == 4) and piece.first_move:
                this_move = True
            elif piece.type == KING and abs(move[1] - piece.col) > 1:
                this_move = True
            
            if this_move:
                best_piece = piece
                best_move = move
        
        if best_piece == None:
            random_index = random.randint(0, len(moves)-1)
            best_piece = pieces[random_index] # best_piece
            best_move = moves[random_index] # best_move
        
        return best_piece, best_move

    #@profile
    def best_move(self):
        global best_pieces, best_moves
        self.positions_calculated = 0
        best_pieces = []
        best_moves = []
        alpha = -9999
        beta = 9999

        #self.minimax_v3(self.depth, alpha, beta, True)
        legal_moves = self.board.get_legal_moves(self.color)
        self.negamax(legal_moves, self.depth, alpha, beta, self.color)
        best_piece, best_move = self.choose_best_move(best_pieces, best_moves)

        print(self.positions_calculated)
        return best_piece, best_move
    
    
    def negamax(self, legal_moves, depth, alpha, beta, color):
        global best_pieces, best_moves
        if depth == 0 or self.board.board_state == self.board.ended_state:
            self.positions_calculated += 1
            score = color * self.board.board_score
            return score#self.board.evaluate_board(color)

        # Retrieving all the pieces on the board and then finding all legal moves
        best_score = -9999
        #legal_moves = self.board.get_legal_moves(color)

        for piece_move in legal_moves:
            self.board.move_piece(piece_move[0], piece_move[1], searching=True)
            next_moves = self.board.get_legal_moves(-color)
            score = -self.negamax(next_moves, depth-1, -beta, -alpha, -color)
            self.board.pop(searching=True)

            if score > best_score:
                best_score = score
                if depth == self.depth:
                    best_pieces = []
                    best_moves = []
                    best_pieces.append(piece_move[0])
                    best_moves.append(piece_move[1])
            elif score == best_score and depth == self.depth:
                best_pieces.append(piece_move[0])
                best_moves.append(piece_move[1])

            if best_score > alpha:
                alpha = best_score
            if beta <= alpha:
                return best_score

        return best_score
    
    #@profile
    def minimax_v3(self, depth, alpha, beta, max_player):
        global best_pieces, best_moves
        if depth == 0 or self.board.board_state == self.board.ended_state:
            self.positions_calculated += 1
            return self.board.board_score * self.color

        # Retrieving all the pieces on the board and then finding all legal moves
        if max_player:
            best_score = -9999
            legal_moves = self.board.get_legal_moves(self.color)
            for piece_move in legal_moves:
                self.board.move_piece(piece_move[0], piece_move[1], searching=True)
                score = self.minimax_v3(depth-1, alpha, beta, False)
                self.board.pop(searching=True)

                if score > best_score:
                    best_score = score
                    if depth == self.depth:
                        best_pieces = []
                        best_moves = []
                        best_pieces.append(piece_move[0])
                        best_moves.append(piece_move[1])
                elif score == best_score and depth == self.depth:
                    best_pieces.append(piece_move[0])
                    best_moves.append(piece_move[1])

                alpha = max(alpha, best_score)
                if beta < alpha:
                    return best_score

            return best_score
        else:
            best_score = 9999
            legal_moves = self.board.get_legal_moves(self.enemy_color)
            for piece_move in legal_moves:
                self.board.move_piece(piece_move[0], piece_move[1], searching=True)
                score = self.minimax_v3(depth-1, alpha, beta, True)
                self.board.pop(searching=True)

                if score < best_score:
                    best_score = score
                    if depth == self.depth:
                        best_pieces = []
                        best_moves = []
                        best_pieces.append(piece_move[0])
                        best_moves.append(piece_move[1])
                elif score == best_score and depth == self.depth:
                    best_pieces.append(piece_move[0])
                    best_moves.append(piece_move[1])

                beta = min(beta, best_score)
                if beta < alpha:
                    return best_score

            return best_score
