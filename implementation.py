"""
This is the only file you should change in your submission!
"""
from basicplayer import basic_evaluate, minimax, get_all_next_moves, is_terminal
from util import memoize, run_search_function, INFINITY, NEG_INFINITY
import time


# TODO Uncomment and fill in your information here. Think of a creative name that's relatively unique.
# We may compete your agent against your classmates' agents as an experiment (not for marks).
# Are you interested in participating if this competition? Set COMPETE=TRUE if yes.

# STUDENT_ID = 12345678
# AGENT_NAME =
# COMPETE = False

# TODO Change this evaluation function so that it tries to win as soon as possible
# or lose as late as possible, when it decides that one side is certain to win.
# You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    if board.is_game_over():
        score = -1000
        if board.is_tie():
          score = 0
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        
    else:
        my_chains = board.chain_cells(board.get_current_player_id())
        other_chains = board.chain_cells(board.get_other_player_id())
        score = 0
        for chain in my_chains:
            if len(chain) > 1:
                score += len(chain)
        for chain in other_chains:
             if len(chain) > 1:
                score -= len(chain)
    return score

    

    #raise NotImplementedError


# Create a "player" function that uses the focused_evaluate function
# You can test this player by choosing 'quick' in the main program.
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

# TODO Write an alpha-beta-search procedure that acts like the minimax-search
# procedure, but uses alpha-beta pruning to avoid searching bad ideas
# that can't improve the result. The tester will check your pruning by
# counting the number of static evaluations you make.


def alpha_beta_max_value(board, depth, alpha, beta, eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    if is_terminal_fn(depth, board):
        return eval_fn(board)
    val = NEG_INFINITY
    for move, new_board in get_next_moves_fn(board):
        val = -1*max(val, alpha_beta_min_value(new_board, depth-1, alpha, beta,eval_fn, get_next_moves_fn, is_terminal_fn))
        if val >= beta:
            return val
        alpha = max(val, alpha)
    return val

def alpha_beta_min_value(board, depth, alpha, beta,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    val = INFINITY
    for move, new_board in get_next_moves_fn(board):
        val = min(val, alpha_beta_max_value(new_board, depth - 1, alpha, beta, eval_fn, get_next_moves_fn, is_terminal_fn))
        if val <= alpha:
            return val
        beta = min(beta, val)
    return val



# You can use minimax() in basicplayer.py as an example.
# NOTE: You should use get_next_moves_fn when generating
# next board configurations, and is_terminal_fn when
# checking game termination.
# The default functions for get_next_moves_fn and is_terminal_fn set here will work for connect_four.
def alpha_beta_search(board, depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    """
     board is the current tree node.

     depth is the search depth.  If you specify depth as a very large number then your search will end at the leaves of trees.
     
     def eval_fn(board):
       a function that returns a score for a given board from the
       perspective of the state's current player.
    
     def get_next_moves(board):
       a function that takes a current node (board) and generates
       all next (move, newboard) tuples.
    
     def is_terminal_fn(depth, board):
       is a function that checks whether to statically evaluate
       a board/node (hence terminating a search branch).
    """
    alpha = NEG_INFINITY
    beta = INFINITY
    best_val = None
    for move, new_board in get_next_moves_fn(board):
        val = -1*alpha_beta_min_value(new_board, depth - 1,  alpha, beta, eval_fn,
                                            get_next_moves_fn, is_terminal_fn)
        print new_board 
        print val
        print
        if best_val is None or val > best_val[0]:
            alpha = val
            best_val = (val, move, new_board)
    #return best_val[1]
    return best_val



# Now you should be able to search twice as deep in the same amount of time.
# (Of course, this alpha-beta-player won't work until you've defined alpha_beta_search.)
def alpha_beta_player(board):
    return alpha_beta_search(board, depth=8, eval_fn=better_evaluate)


# This player uses progressive deepening, so it can kick your ass while
# making efficient use of time:
def ab_iterative_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=focused_evaluate, timeout=5)


# TODO Finally, come up with a better evaluation function than focused-evaluate.
# By providing a different function, you should be able to beat
# simple-evaluate (or focused-evaluate) while searching to the same depth.


#help: https://www.gamedev.net/forums/topic/644496-connect-4-evaluation-functionneed-some-guide/, https://github.com/msaveski/connect-four


# returns what type of chain the sequence is
# 0 = horizontal, 1 = vertical, 2 = diagonal
def chain_type(chain):
    link_1 = chain[0]
    link_2 = chain[1]
    if link_1[0] == link_2[0]:
      return 0
    elif link_1[1] == link_2[1]:
      return 1
    else:
      return 2


def better_evaluate(board):
    if board.is_game_over():
            score = -10000
            if board.is_tie():
              score = 0
            if board.is_win() == board.get_current_player_id():
              score = 10000
    else:

        my_chains = board.chain_cells(board.get_current_player_id())
        other_chains = board.chain_cells(board.get_other_player_id())
        score = 0
        for chain in my_chains:
            blocked = False 
            for link in chain:
                if link[0] == 0 or link[1] == 6:
                    blocked = True 
            if not blocked: 
                if len(chain) > 1:
                    cType = chain_type(chain)  
                    if cType == 0 and board.get_cell(chain[len(chain)-1][0],chain[len(chain)-1][1]+1) <> 0:
                        blocked = True
                    if cType == 1 and board.get_cell(chain[len(chain)-1][0]-1,chain[len(chain)-1][1]) <> 0:
                        blocked = True
                    if cType == 0 and board.get_cell(chain[len(chain)-1][0]-1,chain[len(chain)-1][1]+1) <> 0:
                      blocked = True
            if not blocked:
                score += len(chain)**2
        for chain in other_chains:
            blocked = False 
            for link in chain:
                if link[0] == 0 or link[1] == 6:
                    blocked = True
            if not blocked: 
                if len(chain) > 1:
                    cType = chain_type(chain)  
                    if cType == 0 and board.get_cell(chain[len(chain)-1][0],chain[len(chain)-1][1]+1) <> 0:
                        blocked = True
                    if cType == 1 and board.get_cell(chain[len(chain)-1][0]-1,chain[len(chain)-1][1]) <> 0:
                        blocked = True
                    if cType == 0 and board.get_cell(chain[len(chain)-1][0]-1,chain[len(chain)-1][1]+1) <> 0:
                        blocked = True
            if not blocked:
                score -= len(chain)**2
    return score

#Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

#memoize focused evaluate
focused_evaluate = memoize(focused_evaluate)

# A player that uses alpha-beta and better_evaluate:
def my_player(board):
    return run_search_function(board, search_fn=alpha_beta_search, eval_fn=better_evaluate, timeout=5)

# my_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)
