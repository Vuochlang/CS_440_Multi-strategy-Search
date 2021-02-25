"""MultiStrategy Search in TicTacToe

Warm up thought questions 
(not graded, just to get you going)... consider referring to the slides.

a. read the documentation for count_outcomes(). What should the 
   return value be for the input state 122122011?

-> Return value = (0, 1, 0) which indicates X won.


b. what should count_outcomes() return for an input state of
   102122001?

-> With current input state, there are three options for X to move:
    1. X takes board[6] = 102122101, which X wins - (0, 1, 0)
    2. X takes board[1]:
        _ O takes board[6] = 112122201, which O wins - (0, 0, 1)
        _ or, O takes board[7], then X is left with board[6], thus X will win - (0, 1, 0)
    3. X takes board[7]:
        _ O takes board[6] = 102122211, O will win - (0, 0, 1)
        _ O takes board[1], then X is left with board[6], so X will win - (0, 1, 0)
-> In total, the return value is (0, 3, 2)


Graded questions (answer these):

1. Given an initially empty 3x3 board, how many end games result in
   a win for X?

-> Using the count_outcomes() with the empty board as the initial state,
    the return value is (46080, 131184, 77904). So the total end games that X win is 131184


2. How early can X force a win assuming O plays randomly?

-> Assuming we are at the current state 001002120:
       |   | X
    -----------
       |   | O
    -----------
    X | O |
-> By running the evaluation function with the state, we get
        BB:(0, 1, 0), BR:(0, 4, 0), RB:(2, 5, 6), RR:(12, 45, 16)
-> Thus, if X is one move away from winning and O plays randomly, X will most likely to win the game.


3. How early can X force a win assuming O plays the best strategy?

-> When the X player manages to get any two corners and O is not in the center as shown below,
         |   |
       -----------
        O |   |
       -----------
         X |   | X
-> O's next move will be in between those two X, then X can take the center which result in,
           |   |
        -----------
        O | X |
        -----------
        X | O | X
-> So, no matter which way O is going, X is guarantee a win.


"""

import sys

from typing import List


class TicTacToe():
    Column = 0
    Row = 1
    Diagonal = 2
    StaleMate = 3
    Chrs = {0: ' ', 1: 'X', -1: 'O'}


from collections import namedtuple

#
# NOTE:  ** Be Careful Constructing These ! **
#
#       The 'nextplayer' field must be set appropriately for the board state
#       and no verification is performed to ensure that it is valid.
#       'nextplayer' should be 1 (if the nextplayer is X) and -1 otherwise
#       Although 'nextplayer' *could* be calculated from the board contents,
#       it is explicitly maintained in the state for efficiency.
#
#       Recall that this creates the class TTTNode which behaves like
#       a tuple (the instance variable references are immutable), but
#       unlike a tuple, you can access the instance variables ("slots")
#       with names instead of indicies. Here, each instance will have
#       the three instance variable names: 'nextplayer', 'board' and 'parent'
TTTNode = namedtuple('TTTNode', ['nextplayer', 'board', 'parent'])


class MultiStrategySearch():
    def __init__(self, boardsize=3):
        self.n = boardsize
        self.n2 = boardsize ** 2

    def is_win(self, tttnode):
        """ _Part 1: Implement This Method_
        
        Use your code from TicTacToe to determine if the
        TTTNode instance represents a board in an end-game configuration. 
        Note that "tttnode" is an argument to the method here, it is 
        not an instance variable...

        For a board of size n, a win requires one player to have n tokens
        in a line (vertical, horizontal or diagonal). 

        Arguments:
         tttnode - an instance of TTTNode representing a particular node
                     in the search tree (this give you player information
                     along with the state in the search graph, which can 
                     help you improve the speed of this method). You can 
                     assume that any tttnode passed into this method
                     with encapsulate a board with self.n2 elements

        Returns:
         (TicTacToe.Column, c, player): if player wins in column c
         (TicTacToe.Row, r, player): if player wins in row r
         (TicTacToe.Diagonal, 0, player): if player wins via
           a diagonal in the upper-left corner
         (TicTacToe.Diagonal, 1, player): if player wins via a
           diagonal in the upper-right corner
         (TicTacToe.StaleMate, 0, 0): if the game is a stalemate
         False: if the outcome can't be determined yet
        """

        # only check for last player's win

        # check row = horizontal, to see if a player won in any particular row
        start_index = 0
        for row in range(self.n):  # loop through each <row>
            win = True
            limit = start_index + self.n
            player_id = tttnode.board[start_index]
            for i in range(start_index, limit):  # loop through each column of that <row>
                if player_id == 0:  # if the column is still empty
                    win = False
                    break
                if player_id != tttnode.board[i]:  # if the column is taken by the other player
                    win = False
                    break
            start_index = limit  # update the starting index to check for the next row
            if win:
                return TicTacToe.Row, row, player_id

        # check column = vertical, to see if a player won in any particular column
        for column in range(self.n):  # loop through each <column> of the table
            win = True
            last = column
            player_id = tttnode.board[last]
            if player_id != 0:  # if the <column> is taken
                while last < self.n2:  # loop through each square box in that <column>
                    if player_id == 0:  # if box is empty
                        win = False
                        break
                    if player_id != tttnode.board[last]:  # if box is taken by other player
                        win = False
                        break
                    last += self.n  # update the index to check next square box in that <column>
            else:  # if that first box in the <column> is empty, move to the next column
                win = False
                last += self.n
            if win:
                return TicTacToe.Column, column, player_id

        # diagonal in the upper-left corner
        win = True
        player_id = tttnode.board[0]  # most upper left
        for i in range(self.n):  # loop through each box in each row in a diagonally direction from the left
            if player_id == 0:
                win = False
                break
            start = (self.n * i) + i  # update the box-index for the next box in the next row
            if player_id != tttnode.board[start]:
                win = False
                break
        if win:
            return TicTacToe.Diagonal, 0, player_id

        # diagonal in the upper-right corner
        win = True
        player_id = tttnode.board[self.n - 1]  # most upper right
        for i in range(1, self.n + 1):  # loop through each box in each row in a diagonally direction from the right
            if player_id == 0:
                win = False
                break
            start = (self.n * i) - i  # update the box-index for the next box in the next row
            if player_id != tttnode.board[start]:
                win = False
                break
        if win:
            return TicTacToe.Diagonal, 1, player_id

        # if it didn't return in any above check-point, then it's either the game is not over or is StaleMate
        # first, check if the board is full - StaleMater, otherwise, the continue the game
        full = True
        for i in range(self.n2):
            if tttnode.board[i] == 0:
                full = False
                break
        if full:  # stale mate
            return TicTacToe.StaleMate, 0, 0

        return False  # game is not ended yet

    def show(self, state, stream=sys.stdout):
        """Prints a representation of the board on the specified stream."""

        for i in range(self.n):
            fmtstr = []
            for j in range(self.n - 1):
                fmtstr.append(" %s |" % TicTacToe.Chrs[state.board[i * self.n + j]])
            fmtstr.append(" %s " % TicTacToe.Chrs[state.board[(i + 1) * self.n - 1]])
            line = "".join(fmtstr)
            print(line, file=stream)
            if i < self.n - 1:
                print('-' * len(line), file=stream)

    def successors(self, tttnode):
        """Yield the successor nodes of the given parent node.
        
        Note that this successor function takes a TTTNode instance
        and yields TTTNode instances. These nodes don't track path/edge
        costs since we don't care about that in our search. But, they do
        maintain a reference to their parent so we can navigate the search
        tree.
        """
        for i in range(self.n ** 2):
            if tttnode.board[i] == 0:
                lstate = list(tttnode.board)  # create a list to manipulate
                lstate[i] = tttnode.nextplayer  # fill an empty space

                # before we yield the successor, turn that child state back
                # into a tuple so no one can accidentally modify it...
                yield TTTNode(tttnode.nextplayer * -1,
                              tuple(lstate), tttnode)

    def count_outcomes(self, tttnode, verbose=False):
        """ _ Part 4: Implement this method _ 

        Counts the distinct outcomes of tictactoe games.

        Hints:
        (1) it may be easiest to create a recursive helper method
        to do the heavy lifting.
        (2) you can turn a list into a tuple by
        calling tuple() with the list as an argument.

        args:
            tttnode - a TTTNode instance representing the 'initial state'
            verbose - True for debugging output

        returns:
            a tuple of (# of ties, # of X wins, # of O wins) for all possible
            games generated by starting at the initial state and playing until
            completion.
        """

        total_game = (0, 0, 0)

        for node in self.successors(tttnode):
            # check the successor if it's the end game before recursively call the function again
            result = self.is_win(node)

            if not result:  # not end game, result == False
                total_game = addtuples(total_game, tuple(self.count_outcomes(node)))
            else:  # end game, increment the number according to the winner
                if result[2] == -1:  # O
                    total_game = addtuples(total_game, (0, 0, 1))
                elif result[2] == 1:  # X
                    total_game = addtuples(total_game, (0, 1, 0))
                else:  # stalemate
                    total_game = addtuples(total_game, (1, 0, 0))

        return total_game

    def evaluate_strategies(self, tttnode, verbose=False):
        """ _ Part 5: Implement this method _ 
        
        return a dictionary representing the strategic outcome table for
        a given input state (tttnode). If verbose is False, no
        output should be generated on stdout or stderr.
        
        the dictionary should have keys 'BB', 'RB', 'BR', and 'RR'
        representing the best ('B') and random ('R') strategies
        for player 1 (X) and player 2 (O) respectively. So 'RB'
        corresponds to X playing randomly and O playing its best.
        Values of this table should be a tuple of (ties, X-wins, O-wins).

        Hint: this method may be easiest to implement recursively.
        """

        if self.is_win(tttnode):  # when the given tttnode is already the end game, return with dictionary value
            value = (1, 0, 0)  # stalemate
            if tttnode.nextplayer * -1 == 1:  # X
                value = (0, 1, 0)
            elif tttnode.nextplayer * -1 == -1:  # O
                value = (0, 0, 1)
            return dict([('BB', value), ('BR', value), ('RB', value), ('RR', value)])

        return_dictionary = {  # (ties, X-wins, O-wins)
            'BB': (0, 0, 0),
            'BR': (0, 0, 0),
            'RB': (0, 0, 0),
            'RR': (0, 0, 0)
        }

        # default as X strategy
        key_best = 'BR'
        key_random = 'RB'
        tuple_value = (0, 1, 0)
        if tttnode.nextplayer == -1:
            key_best = 'RB'
            key_random = 'BR'
            tuple_value = (0, 0, 1)

        output_list = []  # list to store outcomes/dictionary from each successor

        # loop through each successor and append the output_list[] with the dictionary
        for each_successor in self.successors(tttnode):
            result = self.is_win(each_successor)
            if result:
                if result[2] == 0:  # stalemate
                    return_dictionary['BB'] = (1, 0, 0)
                    return_dictionary[key_best] = (1, 0, 0)
                    return_dictionary[key_random] = (1, 0, 0)
                    return_dictionary['RR'] = (1, 0, 0)
                else:
                    return_dictionary['BB'] = tuple_value
                    return_dictionary[key_best] = tuple_value
                    return_dictionary[key_random] = tuple_value
                    return_dictionary['RR'] = tuple_value
                output_list.append(return_dictionary)

            else:
                output_list.append(self.evaluate_strategies(each_successor))

        # loop through each item in the output_list[] and get update the strategy dictionary for the player
        return_dictionary = output_list[0].copy()
        for each in output_list[1:]:  # iterate from the second item
            return_dictionary['BB'] = bestchoice(return_dictionary['BB'], each['BB'], tttnode.nextplayer)
            return_dictionary[key_best] = bestchoice(return_dictionary[key_best], each[key_best], tttnode.nextplayer)
            return_dictionary[key_random] = addtuples(return_dictionary[key_random], each[key_random])
            return_dictionary['RR'] = addtuples(return_dictionary['RR'], each['RR'])

        if verbose:
            print(return_dictionary)
        return return_dictionary


def addtuples(t1, t2):
    """ _ Part 2: Implement this function _

    Given two tuples (of the same length) as input, 
    return a tuple that represents the element-wise sum
    of the inputs.  That is

    (out_0, ..., out_n) = (t1_0 + t2_0, ..., t1_n + t2_n)
    """
    return tuple([(x + y) for x, y in zip(t1, t2)])


def bestchoice(t1, t2, whom):
    """ _ Part 3: Implement this function _

    Given two tuples representing:
    (ties, p1-wins, p2-wins)
    
    return the 'best' choice for the player
    'whom'.

    The best choice decision is the one where
    the opponent is least likely to win. If the 
    likelihood (% wins) is insufficient to determine
    a 'best' choice, break ties by selecting the tuple
    in which the 'whom' has *won* the most games; if
    this is still insufficient, break ties further by
    selecting the tuple with the most stalemates.
    """
    # tuples are [TIES, P1, P2]
    # whom is -1 (P2); 1 (P1)

    # set the 'player' and 'opponent' for easy access
    if whom == -1:
        player = 2
        opponent = 1
    else:
        player = 1
        opponent = 2

    total_game1 = sum(list(t1))
    total_game2 = sum(list(t2))

    # get the (% wins) of the player and opponent over total games played
    if total_game1 > 0:
        game_player1 = t1[player] / total_game1
        game_opp1 = t1[opponent] / total_game1
        game_tie1 = t1[0] / total_game1
    else:
        game_player1 = game_opp1 = game_tie1 = 0

    if total_game2 > 0:
        game_player2 = t2[player] / total_game2
        game_opp2 = t2[opponent] / total_game2
        game_tie2 = t2[0] / total_game2
    else:
        game_player2 = game_opp2 = game_tie2 = 0

    # best choice of the opponent that is least likely to win
    if game_opp1 < game_opp2:
        return t1
    elif game_opp1 > game_opp2:
        return t2

    # break ties and look at the game that 'player' wins the most
    elif game_opp2 == game_opp1:
        if game_player1 > game_player2:
            return t1
        if game_player1 < game_player2:
            return t2
        return t1  # same %wins

    # break ties and get the most stalemates
    else:
        if game_tie1 > game_tie2:
            return t1
        return t2


if __name__ == "__main__":
    import argparse
    import random

    parser = argparse.ArgumentParser()
    parser.add_argument("--state")
    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("do_what", choices=['count', 'evaluate'])
    args = parser.parse_args()

    if args.state:
        assert len(args.state) == 9, "Expected string with 9 elements"

        state = [int(z) for z in args.state]
        state = [-1 if s == 2 else s for s in state]
        stateset = set(state)
        assert not stateset.issuperset(set([0, 1, 2])), \
            "Expected string with elements 0,1,2"
        state = tuple(state)
        assert sum(state) == 0 or sum(state) == 1, \
            "Doesn't look like moves are alternating!"

        if sum(state) == 1:
            nextturn = -1
        elif sum(state) == 0:
            nextturn = 1
        else:
            print("state is invalid...")
            sys.exit(1)

        if args.verbose:
            print("".join(TicTacToe.Chrs[i] for i in state[:3]))
            print("".join(TicTacToe.Chrs[i] for i in state[3:6]))
            print("".join(TicTacToe.Chrs[i] for i in state[6:]))

        t3s = TTTNode(nextturn, state, None)

        mss = MultiStrategySearch()
        mss.show(t3s)
        if args.do_what == 'evaluate':
            pm = mss.evaluate_strategies(t3s)
            for key in sorted(pm):
                print("%s:%s" % (str(key), str(pm[key])))

        elif args.do_what == 'count':
            wins = mss.count_outcomes(t3s, args.verbose)
            print("Wins:", wins)
