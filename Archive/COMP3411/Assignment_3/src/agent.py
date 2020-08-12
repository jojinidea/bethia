from game import *
from client import *
import math
import time

MAXIMIZING_PLAYER = 0
MINIMIZING_PLAYER = 1
FACTOR = 0.925


class Agent(object):
    # deals with any agent-related decision making
    def __init__(self, letter):
        self._letter = letter
        self._playersLetters = [] # first letter is our letter, second is opponent's letter
    
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
            move = self.minimax(game.board[int(args[1])-1], game, int(args[1]))
            game.update_board(move,0)
            return move
        elif command == "third_move":
            game.third_move(int(args[0]), int(args[1]), int(args[2]))
            move = self.minimax(game.board[int(args[2])-1], game, int(args[2]))
            game.update_board(move,0)
            return move
        elif command == "next_move":
            tictic = time.time()
            game.update_board(int(args[0]), 1)
            move = self.minimax(game.board[int(args[0])-1], game, int(args[0]))
            game.update_board(move, 0)
            return move
    
    # controller function for minimax - discover all possible optimal moves from 'root' of the tree
    def minimax(self, node, game, lastMove):
        tic = time.time()
        possibleMoves = []
        D = 6
        X = math.floor(5.294*math.exp(0.0204*game.moves_made())*FACTOR)
        if X > D:
            D = X
        for move in self.legal_moves(node):
            game.update_board_minimax(move, lastMove, self._playersLetters[0])
            value = self.min_val(game.board[move-1], 0, game, move, lastMove, -(math.inf), math.inf, D) 
            if (value == 100): 
                return move
            possibleMoves.append((value, move))
            game.update_board_minimax(move, lastMove, ".")
        possibleMoves.sort(key=lambda x:x[0], reverse = True)
        optMove = possibleMoves[0][1]
        return optMove

    # part of minimax algorithm for the min player
    def min_val(self, node, depth, game, lastMove, lastMove2, alpha, beta, D):
        if depth == D or self.has_game_ended(game.board[lastMove2-1]) == True:
            return self.utility_val(game.board[lastMove2-1], MAXIMIZING_PLAYER, lastMove2)
        bestValue = math.inf
        for move in self.legal_moves(node):
            game.update_board_minimax(move, lastMove, self._playersLetters[1])
            value = self.max_val(game.board[move-1], depth+1, game, move, lastMove, alpha, beta, D)
            game.update_board_minimax(move, lastMove, ".")
            bestValue = min(bestValue, value)
            if bestValue <= alpha:
                return bestValue
            beta = min(beta, bestValue)
        return bestValue
   
    # part of minimax for the max player
    def max_val(self, node, depth, game, lastMove, lastMove2, alpha, beta, D):
        moves = []
        if depth == D or self.has_game_ended(game.board[lastMove2-1]) == True:
            return self.utility_val(game.board[lastMove2-1], MAXIMIZING_PLAYER, lastMove2) 
        bestValue = -(math.inf)
        for move in self.legal_moves(node):
            game.update_board_minimax(move, lastMove, self._playersLetters[0])
            value = self.min_val(game.board[move-1], depth+1, game, move, lastMove, alpha, beta, D)
            game.update_board_minimax(move, lastMove, ".")
            bestValue = max(bestValue, value)
            if bestValue >= beta:
                return bestValue
            alpha = max(alpha, bestValue)
        return bestValue
            
    # determines utility/value of a certain terminal state 
    def utility_val(self, subBoard, player, lastMove):
        if self.has_game_ended(subBoard) == True:
            return self.win_or_lose(subBoard, MAXIMIZING_PLAYER)
        else:
            return self.evaluate_heuristic(subBoard, MAXIMIZING_PLAYER, lastMove)
        
    # determines if the game has ended or if the game is still ongoing
    def has_game_ended(self, subBoard):
        if self.win_or_lose(subBoard, 0) != -1: # game has ended
            return True
        return False # if game is still ongoing, return false

    # determines if we have won or loss
    def win_or_lose(self, sub_board, player):
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
                
    # Rows 1,2,3 : 4,5,6 : 7,8,9
    #      1,4,7 : 2,5,8 : 3,6,9
    #      1,5,9 :       : 3,5,7


    #Board positions by heuristic value
    #
    #   | 3 2 3 |
    #   | 2 4 2 |
    #   | 3 2 3 |
    
    # evaluates heuristic value according to the diagram above
    def evaluate_heuristic(self, sub_board, player, lastMove):
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
        return(score) 
        

def main():
    portNum = int(sys.argv[2]) # filename, -p, port #
    client = TTTClientGame(portNum)
    client.connect()
    
    while True:
        serverMessage = client.receive()
        for line in serverMessage.split('\n'): 
            parsedData = client.parse_string(line) # parsed Data is a list that is returned by the parse_string method in the form [command, args]
            command = parsedData[0]
            args = parsedData[1]
            if command == "start":
                player = args[0].upper()
                if player == "X":
                    playerList = ["X", "O"]
                elif player == "O":
                    playerList = ["O", "X"]
                game = Game(playerList[0]) 
                agent = Agent(playerList[0])  
                agent.initialise_playersLetters()
            if "move" in command and command != "last_move":
                move = agent.make_move(game, command, args)
                client._socket.sendall((str(move) + "\n").encode()) 
            if "end" in command:
                client.close()
                return
                
if __name__ == "__main__":
    main()
