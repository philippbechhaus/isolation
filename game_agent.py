import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    """First evaluation heuristic from the point of view of the given player.

    AB_Custom is similar to AB_Custom_3, but additionally forecasts moves down
    the tree by a depth of 2, summarizing the available moves on each level and
    penalizing their score against the available moves of the opponent player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    for move in game.get_legal_moves(player):
        new_board = game.forecast_move(move)
        own_moves += len(new_board.get_legal_moves(player))
        for move2 in new_board.get_legal_moves(player):
            new_board2 = new_board.forecast_move(move2)
            own_moves += len(new_board2.get_legal_moves(player))

    for move in game.get_legal_moves(game.get_opponent(player)):
        new_board = game.forecast_move(move)
        own_moves += len(new_board.get_legal_moves(game.get_opponent(player)))
        for move2 in new_board.get_legal_moves(game.get_opponent(player)):
            new_board2 = new_board.forecast_move(move2)
            opp_moves += len(new_board2.get_legal_moves(new_board2.get_opponent(player)))

    return float(own_moves - opp_moves * 1.5)


def custom_score_2(game, player):
    """Second evaluation heuristic from the point of view of the given player.

    AB_Custom_2 adds the Manhattan Distance between the two players as an
    additional caveat and penalizes moves in proximity to the opponent.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    penalized_move_diff = float(own_moves - 1.5 * opp_moves)
    own_pos = game.get_player_location(player)
    opp_pos = game.get_player_location(game.get_opponent(player))
    manhattan_distance = float(abs(own_pos[0]-opp_pos[0]) + \
    abs(own_pos[1]-opp_pos[1]))

    return float((penalized_move_diff/manhattan_distance**(-1)))


def custom_score_3(game, player):
    """Third evaluation heuristic from the point of view of the given player.

    The most obvious heuristic: Counts the available moves for each active_player.
    For a conservative approach, we penalize the number of available moves to
    the active player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - opp_moves * 1.5)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Searches for the best move from the available legal moves and
        returns a result before the time limit expires.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Depth-limited minimax search algorithm.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        """
        # timeout challenge. editable in class or instance creation
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # once maximum depth is reached, return location and associated score
        if depth == 0:
            return self.score(game, self)

        # default values
        best_move = (-1, -1)
        value = float('-inf')

        # retrieve list of all legal moves
        moves = game.get_legal_moves()

        # loop through list
        for move in moves:
            # prepare new board for recursion
            new_board = game.forecast_move(move)
            # start alternating recursion until depth is reached
            score = self.min_value(new_board, depth - 1)
            # update default values
            if score > value:
                best_move = move
                value = score
        return best_move

    def min_value(self, game, depth):
        """
        ********************
            Helper Class
        ********************
        - Parameters equal minimax(args)
        - Returns min score of move
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        moves = game.get_legal_moves()
        value = float('inf')

        for move in moves:
            new_board = game.forecast_move(move)
            score = self.max_value(new_board, depth - 1)
            if score < value:
                best_move = move
                value = score

        return value

    def max_value(self, game, depth):
        """
        ********************
            Helper Class
        ********************
        - Parameters equal minimax(args)
        - Returns max score of move
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        moves = game.get_legal_moves()
        value = float('-inf')

        for move in moves:
            new_board = game.forecast_move(move)
            score = self.min_value(new_board, depth - 1)
            if score > value:
                best_move = move
                value = score

        return value

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning.
    """

    def get_move(self, game, time_left):
        """Searches for the best move from the available legal moves and
        returns a result before the time limit expires.

        Slightly modified from the get_move() method from the MinimaxPlayer
        class to support iterative deepening (ID) search instead of fixed-depth
        search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        # define depth range here. Make sure to align with timeout challenge
        for d in range(1,500):
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            try:
                best_move = self.alphabeta(game, d)

            except SearchTimeout:
                break

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Depth-limited minimax search with alpha-beta pruning.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        # timeout challenge. editable in class or instance creation
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # once maximum depth is reached, return corresponding score
        if depth == 0:
            return self.score(game, self)

        # default values
        best_move = (-1, -1)

        # value that is associated with best move
        value = float('-inf')

        # default value of best already explored options along path to the root
        # for maximizer
        alpha = float('-inf')

        # default value of best already explored options along path to the root
        # for minimizer
        beta = float('inf')

        # retrieve list of all legal moves
        moves = game.get_legal_moves()

        # loop through list
        for move in moves:
            # prepare new board for recursion
            new_board = game.forecast_move(move)
            # start alternating recursion until depth is reached
            score = self.min_ab_value(new_board, depth - 1, value, beta)
            # update default values
            if score > value:
                best_move = move
                value = score
        return best_move

    def min_ab_value(self, game, depth, alpha, beta):
        """
        ********************
            Helper Class
        ********************
        - Parameters equal minimax(args)
        - Returns min score of move
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        value = float('inf')
        moves = game.get_legal_moves()

        for move in moves:
            new_board = game.forecast_move(move)
            score = self.max_ab_value(new_board, depth - 1, alpha, beta)
            if score < value:
                best_move = move
                value = score
                if value <= alpha:
                    return value
                else:
                    beta = min(value, beta)

        return value

    def max_ab_value(self, game, depth, alpha, beta):
        """
        ********************
            Helper Class
        ********************
        - Parameters equal minimax(args)
        - Returns max score of move
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        value = float('-inf')
        moves = game.get_legal_moves()

        for move in moves:
            new_board = game.forecast_move(move)
            score = self.min_ab_value(new_board, depth - 1, alpha, beta)
            if score > value:
                best_move = move
                value = score
                if value >= beta:
                    return value
                else:
                    alpha = max(value, alpha)

        return value
