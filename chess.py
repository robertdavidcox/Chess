from termcolor import colored


class Game(object):

    chars = "ABCDEFGH"
    codes = "CkBKQBkCPPPPPPPP                                PPPPPPPPCkBKQBkC"
    players = ["blue", "red"]
    current_player = "blue"
    
    def __init__(self, i):
        self.i = i
        self.board = [[None for x in range(size)] for y in range(size)]

        for i in range(size):
            for j in range(size):
                if j > 5:
                    player = "red"
                else:
                    player = "blue"

                if self.codes[i + size*j] <> " ":
                    self.board[i][j] = Piece(self.codes[i + size*j], i, j, player, self)

        print(colored("-----------------------------", 'green'))
        print(colored("Welcome to Rob's Chess Game!!", "red"))
        print(colored("-----------------------------", 'green'))

        self.player1 = raw_input("Player 1, what is your name?\n")
        self.player2 = raw_input("Player 2, what is your name?\n")

        self.play()


    def play(self):

        turn = 1

        while (True):
            self.draw()
            move = raw_input("Player {}, please enter a move or type 'h' for help: ".format(turn % 2 +1))

            while self.move_to_xy(move) == False:
                move = raw_input("Player {}, please enter a move or type 'h' for help: ".format(turn % 2 +1))

            (x, y, new_x, new_y) = self.move_to_xy(move)

            self.move(x, y, new_x, new_y)
            turn += 1
            self.current_player = self.players[(turn+1)%2]



    def move_to_xy(self, move):

        if len(move) > 4:
            print("Incorrect format, format should be 'A1D2'")
            return False

        x = move[0]
        if x in chars:
            x = chars.index(x)
        else:
            print("Horizontal axis of piece to be moved is out of range")
            return False

        y = int(move[1])
        if y <0 or y > size:
            print("Vertical axis of piece to be moved is out of range")
            return False

        new_x = move[2]
        if new_x in chars:
            new_x = chars.index(new_x)
        else:
            print("Horizontal axis of location to be moved to is out of range")
            return False

        new_y = int(move[3])
        if new_y <0 or new_y > size:
            print("Vertical axis of location to be moved to is out of range")
            return False

        print("{}{}{}{}".format(x, y, new_x, new_y))
        if self.valid_move(x, y, new_x, new_y) == False:
            return False

        return (x, y, new_x, new_y)



    def get_piece_player(self, x, y):
        if self.board[x][y] is None:
            return "none"
        else:
            return self.board[x][y].player

    def move(self, x, y, new_x, new_y):
        self.board[new_x][new_y] = self.board[x][y]
        self.board[x][y] = None


    def valid_move(self, x, y, new_x, new_y):        

        if self.get_piece_player(x, y) == self.get_piece_player(new_x, new_y):
            return False

        if self.current_player <> self.get_piece_player(x, y):
            return False

        d = self.direction(x, y)
        if self.board[x][y].code == "P":
            if new_y - y == 1 * d and abs(new_x - x) == 1:
                return self.get_piece_player(new_x, new_y) <> self.get_piece_player(x, y)
            elif new_y - y == 1 * d:
                return self.get_piece_player(new_x, new_y) == "none"

        elif self.board[x][y].code == "C":
            if (new_y <> y and new_x == x) or (new_y == y and new_x <> x):
               return self.spaces_between_straight(x, y, new_x, new_y)

        elif self.board[x][y].code == "k":
            if (abs(new_y - y) == 2 and abs(new_x - x) == 1) or (abs(new_y - y) == 1 and abs(new_x - x) == 2):
                return True

        elif self.board[x][y].code == "B":
            if abs(new_y - y) == abs(new_x - x):
                return True

        elif self.board[x][y].code == "K":
            print("Here")
            if abs(new_x - x) <= 1 and abs(new_y - y) <= 1:
                print("Here2")
                return True

        elif self.board[x][y].code == "Q":
            if abs(new_y - y) == abs(new_x - x):
                return self.spaces_between_diagonal(x, y, new_x, new_y)
            elif (new_y <> y and new_x == x) or (new_y == y and new_x <> x):
                return self.spaces_between_straight(x, y, new_x, new_y)

        return False



    def spaces_between_straight(self, x, y, new_x, new_y):

        if new_x - x <> 0:
            for  i in range(min(x, new_x)+1, max(x, new_x)):
                if self.board[i][y] <> None:
                    return False
        else:
            for i in range(min(y, new_y)+1, max(y, new_y)):
                if self.board[x][i] <> None:
                    return False
        return True

    def spaces_between_diagonal(self, x, y, new_x, new_y):

        if new_x > x:
            x_dir = 1
        else:  
            x_dir = -11

        if new_y > y:
            y_dir = 1
        else:
            y_dir = -1

        counter =1

        while counter < abs(new_x - x):
            print("checking {} {}".format(x+counter*x_dir,y+counter*y_dir))
            if self.board[x+counter*x_dir][y+counter*y_dir] <> None:
                return False

            counter += 1

        return True


    def direction(self, x, y):

        if self.get_piece_player(x, y) == "blue":
            return 1
        else:
            return -1           

    def draw(self):
        print("\n "),
        for i in range(0, size):
            print(colored(" " + self.chars[i] + " ", "yellow")),

        print("\n")
        for i in range(0, size):
            print(colored(i, "yellow")),
            for j in range(0, size):
                if self.board[j][i] == None:
                    print("[ ]"),
                else:
                    if self.board[j][i].player == "red":
                        print(colored("[{}]".format(self.board[j][i].code), "red")),
                    else:
                        print(colored("[{}]".format(self.board[j][i].code), "blue")),
            print("\n")


class Piece:

    def __init__(self, code, x, y, player, board):
        self.code = code
        self.x = x
        self.y = y
        self.player = player
        self.board = board

    def make_move(self, move):
        return 0

    def print_piece(self):
        print("code")
        



size = 8
chars = "ABCDEFGH"
castle = "C"
pawn = "P"
bishop = "B"
knight = "K"
queen = "Q"
king = "K"


def int_to_loc(x, y):

    return "{}{}".format(chars[x], y)





c = Game(1)
c.draw()




