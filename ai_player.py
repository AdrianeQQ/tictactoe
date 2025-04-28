from player import Player

class AIPlayer(Player):
    def __init__(self, symbol, max_depth=4):
        super().__init__(symbol)
        self.max_depth = max_depth

    def get_move(self, game):
        best_score = -float('inf')
        best_move = None
        board = [row[:] for row in game.board_state]
        req_wins = game.req_wins
        for r in range(game.dimensions):
            for c in range(game.dimensions):
                if board[r][c] is None:
                    board[r][c] = self.symbol
                    score = self.minimax(board, self.max_depth - 1, -float('inf'), float('inf'), False, req_wins)
                    board[r][c] = None
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing, req_wins):
        winner = self.check_winner(board, req_wins)
        if winner is not None:
            if winner == self.symbol:
                return 10
            elif winner == "draw":
                return 0
            else:
                return -10
        if depth == 0:
            return 0

        if maximizing:
            max_eval = -float('inf')
            for r in range(len(board)):
                for c in range(len(board)):
                    if board[r][c] is None:
                        board[r][c] = self.symbol
                        eval = self.minimax(board, depth - 1, alpha, beta, False, req_wins)
                        board[r][c] = None
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            return max_eval
            return max_eval
        else:
            opponent = "O" if self.symbol == "X" else "X"
            min_eval = float('inf')
            for r in range(len(board)):
                for c in range(len(board)):
                    if board[r][c] is None:
                        board[r][c] = opponent
                        eval = self.minimax(board, depth - 1, alpha, beta, True, req_wins)
                        board[r][c] = None
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            return min_eval
            return min_eval

    def check_winner(self, board, req_wins):
        n = len(board)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(n):
            for c in range(n):
                if board[r][c] is not None:
                    current_symbol = board[r][c]
                    for dr, dc in directions:
                        count = 1
                        rr, cc = r + dr, c + dc
                        while 0 <= rr < n and 0 <= cc < n and board[rr][cc] == current_symbol:
                            count += 1
                            if count >= req_wins:
                                return current_symbol
                            rr += dr
                            cc += dc
        for row in board:
            if None in row:
                return None
        return "draw"

    def make_move(self, game, row=None, col=None):
        move = self.get_move(game)
        if move is not None:
            r, c = move
            return game.make_move(r, c, self.symbol)
        return False


   