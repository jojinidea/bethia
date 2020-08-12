import random
# import other files

class AIAgent(object):
    
    def __init__(self, identity): 
        # sets AI's identity to either x or o
        self._identity = identity # 'X' or 'O'
    
    def generate_rand_move(self, Board, prevMove)
        possibleMoves = []
        for i in range(1, 9):
            if valid_move(i, prevMove): # might need to change the function method/class attributes of valid_move from basic_game_functions.py
                possibleMoves.append(i)
        return random.choice(possibleMoves)
    
    def calculate_score(self, Board):
                
    
    def check_winner(self, Board):
        
        return    
    
    # returns best move to make based on the evaluation of all available moves using minimax PSEUDOCODE ONLY
    def findBestMove(Board, player):
        bestmove = NULL
        for each move in board:
            if current move is better than bestMove
                bestMove = currentmove
        return bestMove

    # minimax search algorithm PSEUDOCODE ONLY
    def minimax(Board, depth, isMaximisingPlayer):
        if current board state is a terminal state:
            return value of the board
        if isMaximisingPlayer:
            bestMaxVal= -infinity
            for each move in board:
                value = minimax(board, depth-1, False)
                bestMaxVal = max(bestMaxVal, value)
            return bestVal
        else:
            bestMinVal = +infinity
            for each move in board:
                value = minimax(child, depth-1, True)
                bestMinVal = min(bestMinVal, eval)
            return minEval
    
