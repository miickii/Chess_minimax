WHITE, BLACK = 1, -1

# COLORS
C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)
C_GREY = (200, 200, 200)
C_GREY_TRANSPARENT = (100, 100, 100, 150)
C_RED = (255, 0, 0)
C_TRANSPARENT_RED = (255, 0, 0, 150)
C_GREEN = (0, 255, 0)
C_TRANSPARENT_GREEN = (0, 255, 0, 150)
C_BLUE = (0, 0, 255)

# GAME STATES
NORMAL, EXPERIMENTAL, NO_RULES = 0, 1, 2

PIECE_IMG_SIZE = (16, 32)

BOARD_POSITIONS = {
    'a8': (0, 0), 'b8': (0, 1), 'c8': (0, 2), 'd8': (0, 3), 'e8': (0, 4), 'f8': (0, 5), 'g8': (0, 6), 'h8': (0, 7),
    'a7': (1, 0), 'b7': (1, 1), 'c7': (1, 2), 'd7': (1, 3), 'e7': (1, 4), 'f7': (1, 5), 'g7': (1, 6), 'h7': (1, 7),
    'a6': (2, 0), 'b6': (2, 1), 'c6': (2, 2), 'd6': (2, 3), 'e6': (2, 4), 'f6': (2, 5), 'g6': (2, 6), 'h6': (2, 7),
    'a5': (3, 0), 'b5': (3, 1), 'c5': (3, 2), 'd5': (3, 3), 'e5': (3, 4), 'f5': (3, 5), 'g5': (3, 6), 'h5': (3, 7),
    'a4': (4, 0), 'b4': (4, 1), 'c4': (4, 2), 'd4': (4, 3), 'e4': (4, 4), 'f4': (4, 5), 'g4': (4, 6), 'h4': (4, 7),
    'a3': (5, 0), 'b3': (5, 1), 'c3': (5, 2), 'd3': (5, 3), 'e3': (5, 4), 'f3': (5, 5), 'g3': (5, 6), 'h3': (5, 7),
    'a2': (6, 0), 'b2': (6, 1), 'c2': (6, 2), 'd2': (6, 3), 'e2': (6, 4), 'f2': (6, 5), 'g2': (6, 6), 'h2': (6, 7),
    'a1': (7, 0), 'b1': (7, 1), 'c1': (7, 2), 'd1': (7, 3), 'e1': (7, 4), 'f1': (7, 5), 'g1': (7, 6), 'h1': (7, 7)
}

FILE_TO_COL = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
RANK_TO_ROW = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}

ROOK = 1
KNIGHT = 2
BISHOP = 3
QUEEN = 4
KING = 5
PAWN = 6
ENPASSANT = 7

B_ROOK = -1
B_KNIGHT = -2
B_BISHOP = -3
B_QUEEN = -4
B_KING = -5
B_PAWN = -6
B_ENPASSANT = -7

W_ROOK = 1
W_KNIGHT = 2
W_BISHOP = 3
W_QUEEN = 4
W_KING = 5
W_PAWN = 6
W_ENPASSANT = 7

# GAMES (each game is an array with subarrays, the subarrays contain the move for white, and the move for black)
GARRY_GAME_1 = [
    ["pe2_e4", "pd7_d6"], ["pd2_d4", "kg8_f6"], ["kb1_c3", "pg7_g6"], ["bc1_e3", "bf8_g7"]
]
MORPHY_GAME_1 = [
    ["pe2_e4", "pe7_e5"], ["kg1_f3", "pd7_d6"], ["pd2_d4", "bc8_g4"], ["pd4_e5", "bg4_f3"], ["qd1_f3", "pd6_e5"], ["bf1_c4", "kg8_f6"],
    ["qf3_b3", "qd8_e7"], ["kb1_c3", "pc7_c6"], ["bc1_g5", "pb7_b5"], ["kc3_b5", "pc6_b5"], ["bc4_b5", "kb8_d7"], ["o-o-o", "ra8_d8"],
    ["rd1_d7", "rd8_d7"], ["rh1_d1", "qe7_e6"], ["bb5_d7", "kf6_d7"], ["qb3_b8", "kd7_b8"], ["rd1_d8", "done"]
]

IVANCHUK_GAME = "1. c4 e5 2. g3 d6 3. Bg2 g6 4. d4 Nd7 5. Nc3 Bg7 6. Nf3 Ngf6 7. O-O O-O 8. Qc2 Re8 9. Rd1 c6 10. b3 Qe7 11. Ba3 e4 12. Ng5 e3 13. f4 Nf8 14. b4 Bf5 15. Qb3 h6 16. Nf3 Ng4 17. b5 g5 18. bxc6 bxc6 19. Ne5 gxf4 20. Nxc6 Qg5 21. Bxd6 Ng6 22. Nd5 Qh5 23. h4 Nxh4 24. gxh4 Qxh4 25. Nde7+ Kh8 26. Nxf5 Qh2+ 27. Kf1 Re6 28. Qb7 Rg6 29. Qxa8+ Kh7 30. Qg8+ Kxg8 31. Nce7+ Kh7 32. Nxg6 fxg6 33. Nxg7 Nf2 34. Bxf4 Qxf4 35. Ne6 Qh2 36. Rdb1 Nh3 37. Rb7+ Kh8 38. Rb8+ Qxb8 39. Bxh3 Qg3 40. a3 Qf2"

STALEMATE_GAME_1 = "1.d4 e5 2.Qd2 e4 3.Qf4 f5 4.h3 Bb4+ 5.Nd2 d6 6.Qh2 Be6 7.a4 Qh4 8.Ra3 c5 9.Rg3 f4 10.f3 Bb3 11.d5 Ba5 12.c4 e3"
STALEMATE_GAME_2 = "1. e4 e5 2. Nf3 Nc6 3. Bb5 Nd4 4. Nxd4 exd4 5. O-O c6 6. Bc4 Nf6 7. d3 d5 8. exd5 Nxd5 9. Re1+ Be7 10. Qe2 Be6 11. c3 dxc3 12. Nxc3 O-O 13. Bxd5 cxd5 14. b3 Bf6 15. Bb2 Rc8 16. Rac1 Qa5 17. Na4 d4 18. h3 Qg5 19. Qf3 b5 20. h4 Qd2 21. Red1 Rxc1 22. Bxc1 Qxa2 23. Nc5 Bxh4 24. g3 Be7 25. Nxe6 fxe6 26. Bf4 Qxb3 27. Rc1 e5 28. Qb7 exf4 29. Qxe7 fxg3 30. fxg3 Qxd3 31. Qe6+ Kh8 32. Rc8 Qxg3+ 33. Kh1 Qf3+ 34. Kh2 h6 35. Rxf8+ Qxf8 36. Qe4 Qd8 37. Qd3 b4 38. Kg2 a5 39. Kf2 a4 40. Ke2 a3 41. Qb3 d3+ 42. Kd2 Qd4 43. Kd1 Qc3 44. Qg8+ Kxg8"

RANDOM_GAMES = [
    "1. e4 d5 2. exd5 Nf6 3. Nf3 Nxd5 4. d4 Bf5 5. Bd3 Bg6 6. c4 Nb6 7. Nc3 e6 8. O-O Nc6 9. Bxg6 hxg6 10. b3 Bb4 11. Bb2 a6 12. a3 Bd6 13. d5 Bxh2+ 14. Nxh2 Qh4 15. Re1 Qxh2+ 16. Kf1 O-O-O 17. Qg4 Ne5 18. Qe4 Qh1+ 19. Ke2 Qh5+ 20. f3 exd5 21. Nxd5 Nxd5 22. cxd5 Rhe8 23. Kf2 f5 24. Qd4 Nc6 25. dxc6 Rxe1 26. cxb7+ Kxb7 27. Qxd8 Rxa1 28. Bxa1 g5 29. Qd5+ c6 30. Qd7+ Kb6 31. Bd4+ c5 32. Qd6+ Kb7 33. Qd5+ Kb8 34. Be5+ Kc8 35. Qxc5+ Kd8 36. Qf8+ Kd7 37. Qxg7+ Kc6 38. Qc7+ Kb5 39. a4+ Kb4 40. Qc4+ Ka3 41. Bd6+ Kb2 42. Qb4 f4 43. Qa3+ Kc2 44. Qa2+ Kc3 45. Be5+ Kb4 46. Qc2 Qh4+ 47. Ke2 Qh2 48. Bd6+ Ka5 49. Qc5#",
    "1.d4 Nf6 2.Nf3 e6 3.g3 d5 4.Bg2 Be7 5.c4 O-O 6.O-O dxc4 7.Qc2 Bd7 8.Ne5 c6 9.Qxc4 Be8 10.Nd2 Nbd7 11.Ndf3 c5 12.Rd1 Rc8 13.Qb3 b6 14.Nxd7 Nxd7 15.d5 exd5 16.Rxd5 Qc7 17.Bf4 Qc6 18.Rad1 Qe6 19.Qc2 f6 20.Nd4 cxd4 21.Qxc8 Qxe2 22.R5xd4 Bc5 23.R4d2 Qe7 24.Rxd7 Bxd7 25.Qxd7 Qe2 26.Qd2 Qb5 27.b4 Bxb4 28.Qd5+ Qxd5 29.Bxd5+ Kh8 30.Bb3 Re8 31.Be3 g6 32.Rd7 Re7 33.Rd8+ Kg7 34.Rg8#",
    "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6 6.Bg5 e6 7.f4 Be7 8.Qf3 Qc7 9.O-O-O Nbd7 10.Bd3 b5 11.Rhe1 Bb7 12.Qg3 b4 13.Nd5 exd5 14.e5 dxe5 15.fxe5 Nh5 16.e6 Nxg3 17.exf7+ Kxf7 18.Rxe7+ Kg8 19.hxg3 Qxg3 20.Ne6 Qe5 21.Rf1 Nf8 22.Bf5 Bc8 23.Re8 Bb7 24.Bg6 Qf6 25.Bxf6 gxf6 26.Rxf6 Rxe8 27.Bf7#"
]

ENPASSANT_CHECKMATE = "1. e4 c5 2. Nf3 Nc6 3. d4 cxd4 4. Nxd4 Nxd4 5. Qxd4 Qc7 6. Nc3 e5 7. Qd1 Nf6 8. Bd3 b6 9. O-O Bb7 10. Bg5 Be7 11. Bxf6 Bxf6 12. Nd5 Bxd5 13. exd5 Qc5 14. c4 O-O 15. Qh5 g6 16. Qf3 Qd6 17. h4 h5 18. g3 Rfe8 19. Kg2 Re7 20. Rae1 Rae8 21. Rh1 Qb4 22. b3 a5 23. g4 a4 24. gxh5 axb3 25. axb3 Qxb3 26. hxg6 e4 27. Qh5 Qxd3 28. Qh7+ Kf8 29. h5 Qf3+ 30. Kg1 Bd4 31. Rf1 Qg4+ 32. Kh2 Be5+ 33. f4 exf3#"

THREE_DEPTH_GAME = "[(<pawn.Pawn object at 0x106cd8730>, (4, 0)), (<pawn.Pawn object at 0x106cd85e0>, (3, 2)), (<pawn.Pawn object at 0x106cda4d0>, (5, 7)), (<knight.Knight object at 0x106cd8b20>, (2, 5)), (<pawn.Pawn object at 0x106cda410>, (5, 3)), (<pawn.Pawn object at 0x106cd9c60>, (2, 7)), (<pawn.Pawn object at 0x106cda380>, (5, 2)), (<pawn.Pawn object at 0x106cd9db0>, (3, 6)), (<pawn.Pawn object at 0x106cda470>, (4, 5)), (<queen.Queen object at 0x106cd9600>, (3, 0)), (<pawn.Pawn object at 0x106cda470>, (3, 6)), (<knight.Knight object at 0x106cd8b20>, (3, 7)), (<pawn.Pawn object at 0x106cda350>, (4, 1)), (<pawn.Pawn object at 0x106cd85e0>, (4, 1)), (<pawn.Pawn object at 0x106cda470>, (2, 6)), (<pawn.Pawn object at 0x106cd85e0>, (5, 2)), (<pawn.Pawn object at 0x106cda470>, (1, 5)), (<king.King object at 0x106cda050>, (1, 5)), (<queen.Queen object at 0x106cda290>, (5, 1)), (<king.King object at 0x106cda050>, (1, 6)), (<queen.Queen object at 0x106cda290>, (5, 2)), (<queen.Queen object at 0x106cd9600>, (5, 2)), (<knight.Knight object at 0x106cd9b10>, (5, 2)), (<pawn.Pawn object at 0x106cd9750>, (2, 3)), (<bishop.Bishop object at 0x106cd87f0>, (5, 4)), (<knight.Knight object at 0x106cd9690>, (1, 3)), (<pawn.Pawn object at 0x106cda4a0>, (4, 6)), (<pawn.Pawn object at 0x106cd9c90>, (3, 4)), (<pawn.Pawn object at 0x106cda4a0>, (3, 7)), (<rook.Rook object at 0x106cd9ff0>, (0, 1)), (<knight.Knight object at 0x106cd9b10>, (4, 4)), (<pawn.Pawn object at 0x106cd8670>, (2, 1)), (<rook.Rook object at 0x106cda020>, (6, 7)), (<rook.Rook object at 0x106cd8790>, (0, 6)), (<rook.Rook object at 0x106cd9c00>, (6, 0)), (<rook.Rook object at 0x106cd8790>, (0, 7)), (<knight.Knight object at 0x106cd9d20>, (5, 5)), (<king.King object at 0x106cda050>, (0, 6)), (<rook.Rook object at 0x106cd9c00>, (6, 3)), (<king.King object at 0x106cda050>, (1, 5)), (<rook.Rook object at 0x106cda020>, (6, 5)), (<king.King object at 0x106cda050>, (1, 6)), (<rook.Rook object at 0x106cd9c00>, (6, 0)), (<pawn.Pawn object at 0x106cd8670>, (3, 1)), (<pawn.Pawn object at 0x106cd8730>, (3, 1)), (<rook.Rook object at 0x106cd9ff0>, (0, 0)), (<rook.Rook object at 0x106cd9c00>, (1, 0)), (<bishop.Bishop object at 0x106cd9e40>, (2, 0)), (<rook.Rook object at 0x106cd9c00>, (1, 3)), (<king.King object at 0x106cda050>, (0, 6)), (<knight.Knight object at 0x106cd9b10>, (2, 5))]"