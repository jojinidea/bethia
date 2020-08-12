class Game(object):
    #Defines an empty board and initiates some parameters
    def __init__(self, char):
        self.board = []
        self.dupBoard = []
        for i in range(9):
            self.board.append([".",".",".",".",".",".",".",".","."])
        self.lastmove = ""
        if char == "O":
            self.player_letters = ["O", "X"]
        else:
            self.player_letters = ["X", "O"]
      
    #Displays a simple board separated by | or _
    def display_board(self):
        for RowMod in range(0,9,3):
            print("_______________________________")
            for ColMod in range(0,9,3):
                for Row in range(RowMod, RowMod+3):
                    print("|", end="")
                    for Col in range(ColMod, ColMod+3):
                        print(" "+self.board[Row][Col]+" ",end="")
                print("|")
        print("_______________________________")
    
    
    # calculates how many moves have been made
    def moves_made(self):
        size = 0
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != ".":
                    size = size + 1
        return(size)
    
    #Changes the given cell using the last known Letter
    def update_board(self, Arg, Letter):
        if self.lastmove == "":
            self.lastmove = Arg-1
        else:
            self.board[self.lastmove][Arg-1] = self.player_letters[Letter]
            self.lastmove = Arg-1
    
    # updates board for minimax        
    def update_board_minimax(self, move, subboard, playerLetter):
        if playerLetter != ".":
            self.board[subboard-1][move-1] = playerLetter
        elif playerLetter == ".":
            self.board[subboard-1][move-1] = "." # ensures nothing gets overwritten by minimax
    
    ## REFACTOR the below ## 
    def second_move(self, A,B): # A is the subboard, B is the move
        self.update_board(A, 1)
        self.update_board(B, 1)
    
    #Get my choice of move
    def third_move(self, A,B,C):
        self.update_board(A, 0)
        self.update_board(B, 0)
        self.update_board(C, 1)
        #Get my choice of move
    
    def next_move(self, A):
        self.update_board(A,1)
        #Get my choice of move
    def make_move(self, A):
        self.update_board(A,0)
    
    def last_move(self, A):
        self.update_board(A,1)


