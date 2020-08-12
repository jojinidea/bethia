from game import *
from client import *
import math

class Agent(object):
    # deals with any agent-related decision making
    def __init__(self, letter):
        self._letter = letter
        self._playersLetters = [] # first letter is our letter, second is opponent's letter
        self._legalMoves = [] #stores list of all possible valid moves
    
    def initialise_playersLetters(self):
        if self._letter.upper() = "X":
            self._playersLetters = ["X","O"]
        else:
            self._playersLetters = ["O","X"]
        
    def generate_rand_move(self, game): 
        for i in range(1,9):
            if game.valid_move(i):
                self._legalMoves.append(i)
        move = random.choice(self._legalMoves)
        game.update_board(move, 0)
        return move
    
    def reset_legal_moves(self):
        self._legalMoves = []
    
    def make_move(self, game, command, args): 
        if command == "second_move":
            game.second_move(int(args[0]), int(args[1])) 
            game.display_board()
            move = self.generate_rand_move(game)
            self.reset_valid_moves()
            return move
        elif command == "third_move":
            game.third_move(int(args[0]), int(args[1]), int(args[2]))
            game.display_board()
            move = self.generate_rand_move(game)
            self.reset_valid_moves()
            return move
        elif command == "next_move":
            game.update_board(int(args[0]), 1)
            move = self.generate_rand_move(game)
            self.reset_valid_moves()
            return move
        elif command == "won":
            print("we won!")
            return -1
        elif command == "loss":
            print("we lost :(")
            return -1
    
    def switchPlayer(self, player):
        if player == "X":
            return "O"
        return "X"
    
    def minimax(self, game, depth, maximizingPlayer):
        game_ended = self.has_game_ended(game)
        if depth == 0 or game_ended != False: # we are at terminal state # 0 is placeholder for max depth, in which case we return value of heuristic
            if self.win_or_lose(game_ended) == 100:
                return 100
            elif self.win_or_lose(game_ended) == -100 
                return -100
            else: 
                return 0
        if maximizingPlayer: # if our turn
            bestValue = -(math.inf) 
            for move in self._legalMoves:
                game.update_board(move, self._playersLetters[0]) 
                v = self.minimax(game.board, depth+1, False)
                game.update_board(move, ".") # so we don't overwrite the board
                bestValue = max(bestValue, v)
                return bestValue
        else: # minimising player
            bestValue = math.inf
            for move in self._legalMoves:
                game.update_board(move, self._playersLetters[1]) # update the board
                v = self.minimax(game.board, depth+1, True)
                game.update_board(move, ".") 
                bestValue = max(bestValue, v)
                return bestValue
       
    def choose_opt_move(depth, game): #starts minimax
        tieValue = 0
        optMoves = []
        for move in self.legalMoves():
            game.update_board(move, self._letter)
            v = self.minimax(game, depth+1, False)
            game.update_board(move, ".") # so we don't overwrite board
            if v == tieValue:
                optMoves.append(move)
            elif v > tieValue: 
                return move
        return random.choice(optMoves)
                
    # to do: IMPLEMENT ALPHA BETA
    # if we timeout, then return the best move we can for a certain search space - hard to determine a fixed depth to search until because branching factor changes everytime depending on pruning (unless we can prune optimally in which case we will have a better approximation) - maybe set a timer??

    def has_game_ended(self, game.board):
        # determines whether or not the game has ended
        for sub_board in range(1,9)
            if (self.win_or_lose(game.board[sub_board]) != 0) # working under assumption return value of 0 means nobody has won/loss (game is still ongoing)
                return sub_board 
        return False # if game is still ongoing, return false

    def win_or_lose(self, sub_board):
        # -100 for loss
        # 0 for draw
        # 100 for win
        Heuristic_Vals = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
        for val in Heuristic_Vals:
            C = 0
            for i in range(3):
                if sub_board[val[i]-1] == self.playersLetters[0]:
                    C = C - 1
                elif sub_board[val[i]-1] == self.playersLetters[1]:
                    C = C + 1
            if abs(C) == 3:
                return(C*100/3)
        return(0) # does this actually determine whether or not we've drawn - doesn't it only determine that nobody has won ... ?
                
    def evaluate_heuristic(self, sub_board, player):
        # Rows 1,2,3 : 4,5,6 : 7,8,9
        #      1,4,7 : 2,5,8 : 3,6,9
        #      1,5,9 :       : 3,5,7


        #Board positions by heuristic value
        #
        #   | 3 2 3 |
        #   | 2 4 2 |
        #   | 3 2 3 |

        
        Heuristic_Vals = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
        score = 0
        for val in Heuristic_Vals:
            localscore = 0
            for i in range(len(val)):
                if sub_board[val[i]-1] == self.player_letters[1-player]:
                    if localscore > 0:
                        localscore = 0
                        break
                    localscore = localscore - 1
                elif sub_board[val[i]-1] == self.player_letters[player]:
                    if localscore < 0:
                        localscore = 0
                        break
                    localscore = localscore + 1
            if localscore > 1:
                for i in range(abs(localscore)-1):
                    localscore = localscore*(10)
            elif localscore < 1:
                for i in range(abs(localscore)-1):
                    localscore = localscore*(10)-2
            score = score + localscore
        return(score) 
