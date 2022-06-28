
def minimax_v1(self, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or self.board.board_state == self.board.ended_state:
        return self.score - self.enemy_score

    # Retrieving all the pieces on the board and then finding all legal moves
    if maximizingPlayer:
        pieces_on_board = self.board.get_pieces_on_board()
        self.board.set_legal_moves(self.color, pieces_on_board)
        legal_moves = self.board.legal_moves.copy()
        best_score = -9999

        for piece_move in legal_moves:
            score_copy = self.score
            enemy_score_copy = self.enemy_score
            threathening_copy = self.threathening_amt
            enemy_threathening_amt = self.enemy_threathening_amt
            self.board.move_piece(piece_move[0], piece_move[1], searching=True)
            score = self.minimax_v1(depth-1, alpha, beta, False)
            self.board.switch_turn()
            self.board.switch_turn()
            self.board.pop(searching=True)
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
        pieces_on_board = self.board.get_pieces_on_board()
        self.board.set_legal_moves(self.enemy_color, pieces_on_board)
        legal_moves = self.board.legal_moves.copy()
        best_score = 9999

        for piece_move in legal_moves:
            score_copy = self.score
            enemy_score_copy = self.enemy_score
            threathening_copy = self.threathening_amt
            enemy_threathening_amt = self.enemy_threathening_amt
            self.board.move_piece(piece_move[0], piece_move[1], searching=True)
            score = self.minimax_v1(depth-1, alpha, beta, True)
            self.board.switch_turn()
            self.board.switch_turn()
            self.board.pop(searching=True)
            self.threathening_amt = threathening_copy
            self.enemy_threathening_amt = enemy_threathening_amt
            self.score = score_copy
            self.enemy_score = enemy_score_copy
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                return best_score
        return best_score

# Time: 46587159
def minimax(self, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or self.board.board_state == self.board.ended_state:
        return self.score - self.enemy_score

    # Retrieving all the pieces on the board and then finding all legal moves
    pieces_on_board = self.board.get_pieces_on_board()
    self.board.set_legal_moves(pieces_on_board)
    legal_moves = self.board.legal_moves.copy()
    if maximizingPlayer:
        best_score = -9999
        for i, piece_move in enumerate(legal_moves):
            board_copy = self.board.copy()
            score_copy = self.score
            enemy_score_copy = self.enemy_score
            threathening_copy = self.threathening_amt
            enemy_threathening_amt = self.enemy_threathening_amt
            self.board.move_piece(piece_move[0], piece_move[1], searching=True)
            score = self.minimax(depth-1, alpha, beta, False)
            self.board.revert_from_copy(board_copy)
            #self.board.pop(searching=True)
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
        for i, piece_move in enumerate(legal_moves):
            board_copy = self.board.copy()
            score_copy = self.score
            enemy_score_copy = self.enemy_score
            threathening_copy = self.threathening_amt
            enemy_threathening_amt = self.enemy_threathening_amt
            self.board.move_piece(piece_move[0], piece_move[1], searching=True)
            score = self.minimax(depth-1, alpha, beta, True)
            self.board.revert_from_copy(board_copy)
            #self.board.pop(searching=True)
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