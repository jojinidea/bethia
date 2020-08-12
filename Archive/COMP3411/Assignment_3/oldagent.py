from game import *
from client import *
import math

# minimax recursion seems to be working, but for some reason we maximize v always!! or best moves have negative heuristic evaluation 

class Agent(object):
    # deals with any agent-related decision making
    def __init__(self, letter):
        self._letter = letter
        self._playersLetters = [] # first letter is our letter, second is opponent's letter
        #self._legalMoves = [] #stores list of all possible valid moves
    
    def initialise_playersLetters(self):
        if self._letter.upper() == "X":
            self._playersLetters = ["X","O"]
        else:
            self._playersLetters = ["O","X"]
        
    def legal_moves(self, subBoard): 
        legalMoves = []
        for i in range(0,9):
            if subBoard[i] == ".":
                legalMoves.append(i+1)
        return legalMoves
                
    
    def make_move(self, game, command, args): 
        if command == "second_move":
            game.second_move(int(args[0]), int(args[1])) 
            print("After our opponent has played second move the board looks like...")
            game.display_board()
            move = self.choose_opt_move(game.board[int(args[1])-1], 0, int(args[1])-1, game, True)
            game.update_board(move,0)
            print("Move in second move is %d"%(move))
            print("Board after our second_move is")
            game.display_board()
            return move
        elif command == "third_move":
            game.third_move(int(args[0]), int(args[1]), int(args[2]))
            print("After our opponent has played third move the board looks like...")
            game.display_board()
            move = self.choose_opt_move(game.board[int(args[2])-1], 0, int(args[2])-1, game, True)
            game.update_board(move,0)
            print("Move in third move is %d" %(move))
            print("Board after our third_move is")
            game.display_board()
            return move
        elif command == "next_move":
            game.update_board(int(args[0]), 1)
            print("After our opponent has played next move board looks like...")
            game.display_board()
            move = self.choose_opt_move(game.board[int(args[0])-1], 0, int(args[0])-1, game, True)
            game.update_board(move, 0)
            print("move in next move is %d"%(move))
            print("Board after our next_move is")
            game.display_board()
            return move
        elif command == "won":
            print("we won!")
            return -1
        elif command == "loss":
            print("we lost :(")
            return -1
    
    # node refers to a sub-board
    def minimax(self, node, depth, maximizingPlayer, game, lastMove):
        
        if self.has_game_ended(node) == True or depth == 2: 
            if self.win_or_lose(node, 0) == 100: 
                return 100
            elif self.win_or_lose(node, 1) == -100: 
                return -100
            elif self.win_or_lose(node, 0) == 50:
                return 0
            else:
                print("Depth is %d", depth)
                if maximizingPlayer == True:
                    player = 0
                else:
                    player = 1
                heuristic = self.evaluate_heuristic(game.board[lastMove-1], player)
                print("Heuristic evaluated using last move %d and player %d"%(lastMove, player))
                print("Evaluated using following subboard:")
                print(game.board[lastMove-1])     
                return heuristic                           
        if maximizingPlayer: # if our turn
            bestValue = -(math.inf) 
            print("Past move was %d", lastMove)
            print("Legal moves for the board are", node, self.legal_moves(node))
            for move in self.legal_moves(node):
                game.update_board_minimax(move,lastMove, self._playersLetters[0]) 
                print("In maximizing player", self._playersLetters[0])
                game.display_board()
                v = self.minimax(game.board[move-1], depth+1, False, game, move-1) # give subboard that we made a move in
                game.update_board_minimax(move, lastMove, ".") # so we don't overwrite the board
                print("Original board below")
                game.display_board()
                bestValue = max(bestValue, v)
                return bestValue
        else: # minimising player
            bestValue = math.inf
            print("Past move was %d", lastMove)
            print("Legal moves for the board are", node, self.legal_moves(node))
            for move in self.legal_moves(node):
                game.update_board_minimax(move, lastMove, self._playersLetters[1]) # update the board
                print("In minimixing player", self._playersLetters[1])
                v = self.minimax(game.board[move-1], depth+1, True, game, move-1)
                game.display_board()
                game.update_board_minimax(move, lastMove, ".") 
                print("Original board below")
                game.display_board()
                bestValue = min(bestValue, v)
                return bestValue
       
    def choose_opt_move(self, node, depth, lastMove, game, maximizingPlayer): #starts minimax - need to pass in lastMove
        tieValue = 0
        optMoves = []
        for move in self.legal_moves(node):
            print("In choose opt move considering move %d" %(move))
            game.update_board_minimax(move, lastMove, self._playersLetters[0]) # 0 is us, 1 is opponent
            v = self.minimax(game.board[move], depth+1, self.change_player(maximizingPlayer), game, move)
            game.update_board_minimax(move, lastMove, ".") # so we don't overwrite board
            if v == tieValue:
                hv = (v, move)
                optMoves.append(hv)
                print("Value of v is %d"%(v))
            elif v > tieValue:
                print("Value of v is %d > tievalue"%(v)) 
                return move
            elif v < tieValue:
                hv = (v, move)
                print("Value of v is %d < tievalue"%(v))
                optMoves.append(hv) 
        if len(optMoves) >=1:
            sorted(optMoves, key=lambda x:x[0])
            move = optMoves[0][0]
            return move
    
    def change_player(self, maximizingPlayer):
        if maximizingPlayer:
            maximizingPlayer = False
        else:
            maximizingPlayer = True
        return maximizingPlayer
        
    # to do: IMPLEMENT ALPHA BETA
    # if we timeout, then return the best move we can for a certain search space - hard to determine a fixed depth to search until because branching factor changes everytime depending on pruning (unless we can prune optimally in which case we will have a better approximation) - maybe set a timer??
    

    def has_game_ended(self, subBoard):
        # determines whether or not the game has ended
        if self.win_or_lose(subBoard, 0) != -1: # game has ended
            return True
        return False # if game is still ongoing, return false

    
    def win_or_lose(self, sub_board, player):
        # -100 for loss
        # 0 for draw
        # 100 for win
        Heuristic_Vals = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
        for val in Heuristic_Vals:
            C = 0
            for i in range(3):
                if sub_board[val[i]-1] == self._playersLetters[1-player]:
                    C = C - 1
                elif sub_board[val[i]-1] == self._playersLetters[player]: 
                    C = C + 1
            if abs(C) == 3:
                return(C*100/3)
        for i in range(0,9):
            if sub_board[i]=='.':
                return(-1)
        
        return(0)
                
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
                if sub_board[val[i]-1] == self._playersLetters[1-player]:
                    if localscore > 0:
                        localscore = 0
                        break
                    localscore = localscore - 1
                elif sub_board[val[i]-1] == self._playersLetters[player]:
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
        print("Score in heuristic is %d"%(score))
        return(score) 
