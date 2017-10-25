"""
This is the only file you should change in your submission!
"""
from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function, INFINITY, NEG_INFINITY
import time


# TODO Uncomment and fill in your information here. Think of a creative name that's relatively unique.
# We may compete your agent against your classmates' agents as an experiment (not for marks).
# Are you interested in participating if this competition? Set COMPETE=TRUE if yes.

STUDENT_ID = 20486960
AGENT_NAME = 'PlayingForFun'
COMPETE = False


# To prefer earlier wins and later losses, I changed the utility
# of a losing position to be a multiple of the number of blank spaces
# on the board. A loss later in the game will result in a smaller penalty 
# than one that occurs earlier

def focused_evaluate(board):
    if board.is_game_over():
        score = (42 - board.num_tokens_on_board()) * -10000
        if board.is_tie():
          score = 0
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)
    return score

    

    #raise NotImplementedError


# Create a "player" function that uses the focused_evaluate function
# You can test this player by choosing 'quick' in the main program.
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)



#Used for help understanding the algorithm: https://www.cs.swarthmore.edu/~meeden/cs63/f07/minimax.html

# This method calculates the  values of MAX for the alpha beta pruning algorithm. 
# it is a helper function for the alpha_beta_search program
def alpha_beta_max_value(board, depth, alpha, beta, eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    if is_terminal_fn(depth, board):
        return eval_fn(board)
    for move, new_board in get_next_moves_fn(board):
        score  = -1*alpha_beta_min_value(new_board, depth - 1, alpha, beta, eval_fn,
                               get_next_moves_fn, is_terminal_fn)
        # update alpha if we find a better solution
        if score > alpha:
            alpha = score
        # if alpha is greater than beta, quit and return beta
        if alpha >= beta:
            return alpha
    return alpha

# This method calculates the  values of MIN for the alpha beta pruning algorithm. 
# it is a helper function for the alpha_beta_search program
def alpha_beta_min_value(board, depth, alpha, beta,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    
    if is_terminal_fn(depth, board):
        return eval_fn(board)
    for move, new_board in get_next_moves_fn(board):
        score  = -1*alpha_beta_max_value(new_board, depth - 1, alpha, beta, eval_fn,
                               get_next_moves_fn, is_terminal_fn)
        # update beta if we have found a score lower than beta
        if score < beta:
            beta = score
        # if beta is less than alpha, quit and return beta
        if beta <= alpha:
            return beta
    return beta





# You can use minimax() in basicplayer.py as an example.
# NOTE: You should use get_next_moves_fn when generating
# next board configurations, and is_terminal_fn when
# checking game termination.
# The default functions for get_next_moves_fn and is_terminal_fn set here will work for connect_four.

# This method is the entry point for the alpha beta search algorithm. For the rest of the Implementation, 
# Please see alpha_beta_min_value and alpha_beta_max_value
def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    """
 
    Do alpha beta search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to

    """
    alpha = NEG_INFINITY
    beta = INFINITY
    best_val = None
    for move, new_board in get_next_moves_fn(board):
        score = -1*alpha_beta_min_value(new_board, depth - 1,  alpha, beta, eval_fn,
                                            get_next_moves_fn, is_terminal_fn)
        if best_val is None or score > alpha:
            alpha = score
            best_val = (alpha, move, new_board)
    return best_val[1]



# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=8, eval_fn=better_evaluate)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=60)



# This is my evaluation function to beat basic_player and focused_evaluate. 
# This method finds the number of chains that each player has on the board
# and adds the current players chains to their score, and subtracts the 
# opponents chains from the score. When the player is going second, 
# this method also prefers to have pieces in the middle of the board if 
# it is player two. 
def better_evaluate(board):
    if board.is_game_over():
        score = (42 - board.num_tokens_on_board()) * -10000
        if board.is_tie():
          score = 0
    else:
        score = 0
        if board.num_tokens_on_board() % 2 == 1:
          score = board.longest_chain(board.get_current_player_id()) * 10
          # Prefer having your pieces in the center of the board.
          for row in range(6):
              for col in range(7):
                  if board.get_cell(row, col) == board.get_current_player_id():
                      score -= abs(3-col)**2
                  elif board.get_cell(row, col) == board.get_other_player_id():
                      score += abs(3-col)**2
        # get my chains and the other players chains
        my_chains = board.chain_cells(board.get_current_player_id())
        other_chains = board.chain_cells(board.get_other_player_id())
        # update my score based on the length of my chains
        for chain in my_chains:
            if len(chain)== 3:
              score += len(chain)**3
            if len(chain)== 2:
              score += len(chain)**2
         # update my score based on the length of my opponents chains
        for chain in other_chains:
            if len(chain) == 3:
              score -= len(chain)**9
            if len(chain) == 2:
              score -= len(chain)**3
    return score

#Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

#memoize focused evaluate
focused_evaluate = memoize(focused_evaluate)

# A player that uses alpha-beta and better_evaluate:
## NOTE: I changed this to be minimax to evaluate my player because my alpha beta search loses
## when i play against basic player, but I can win with minimax
def my_player(board):
    return run_search_function(board, search_fn=minimax, eval_fn=better_evaluate, timeout=5)

# my_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)
