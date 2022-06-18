import sys

# Print total number of arguments
print('Total arguments:', len(sys.argv))
print('The argument values are:', str(sys.argv))

def hypothetic_move(self, piece, checking_piece, new_square):
        avoids_check = False
        curr_square = piece.get_pos()
        curr_row, curr_col = curr_square

        new_row, new_col = new_square

        self.grid[curr_row][curr_col] = None 
        piece_at_new_square = self.grid[new_row][new_col]

        # COPIES
        original_piece_at_new_square = piece_at_new_square
        original_reference_pawn = None

        # CHECK IF I HAVE DONE THIS PART CORRECTLY MICKI!!!
        if piece_at_new_square and piece_at_new_square.type == ENPASSANT:
            if piece.type != PAWN:
                piece_at_new_square = None
            else:
                reference_pawn = piece_at_new_square.reference_pawn
                piece_at_new_square = reference_pawn
                original_reference_pawn = reference_pawn
                self.grid[reference_pawn.row][reference_pawn.col] = None

        if piece_at_new_square and piece_at_new_square == checking_piece:
            # If piece at new square is the checking piece, then this hypothetic move will get player out of check
            avoids_check = True

        # Move piece in grid array to the new position
        self.grid[new_row][new_col] = piece

        # Moves the piece on board
        piece.move(new_square)

        # Make a copy of the original available moves of the checking piece
        threathening_copy = checking_piece.threathening
        available_moves_copy = checking_piece.available_moves
        # IS THIS THE RIGHT WAY TO COPY????
        # ALSO CHECK IF YOU HAVE COPIED THE OBJECTS ABOVE CORRECTLY MICKI!!!

        checking_piece.available_moves = []
        checking_piece.threathening = []
        checking_piece.update_available_moves()

        if checking_piece.is_threathening(self.checked_king.get_pos()):
            avoids_check = False
        else:
            avoids_check = True

        # REVERTING CHANGES
        self.grid[curr_row][curr_col] = piece
        self.grid[new_row][new_col] = original_piece_at_new_square
        if original_reference_pawn:
            self.grid[original_reference_pawn.row][original_reference_pawn.col] = original_reference_pawn
        # Moves the piece on board
        # BE SURE YOU ARE NOT MESSING WITH EN PASSANT MICKI!!!
        piece.move(curr_square)

        return avoids_check
