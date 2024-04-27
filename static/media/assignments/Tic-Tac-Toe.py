board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
x_moves = []
o_moves = []
count = 0


def progress(pos: int, symbol):
    global board
    if pos < 3:
        board[0][pos] = symbol
    elif 3 <= pos < 6:
        board[1][pos-3] = symbol
    elif 6 <= pos < 9:
        board[2][pos-6] = symbol


def show_board():
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                print("[ ]", end=" ")
            elif board[i][j] == "X":
                print("[X]", end=" ")
            elif board[i][j] == "O":
                print("[O]", end=" ")
        print()


def check_pos(pos):
    if pos in (o) or pos in (x):
        return False
    else:
        return True


def winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == "X" or board[i][0] == board[i][1] == board[i][2] == "O":
            w = board[i][0]
            return f"Player {w} Is The Winner !", True
        elif board[0][i] == board[1][i] == board[2][i] == "X" or board[0][i] == board[1][i] == board[2][i] == "O":
            w = board[0][i]
            return f"Player {w} Is The Winner !", True,
    if (board[0][0] == board[1][1] == board[2][2] == "X") or (board[0][2] == board[1][1] == board[2][0] == "X") or (board[0][0] == board[1][1] == board[2][2] == "O") or (board[0][2] == board[1][1] == board[2][0] == "O"):
        w = board[1][1]
        return f"Player {w} Is The Winner !", True,


def x_turn():
    show_board()
    print("---------------------")
    print("Chose Position for X:")
    x_pos = int(input("1-9: "))
    while check_pos(x_pos-1) is False:
        print("This Place Is Occupied, Try Again ")
        x_pos = int(input("1-9: "))
    global x
    x.append(x_pos - 1)
    progress(x_pos - 1, "X")
    print("---------------------")


def o_turn():
    show_board()
    print("---------------------")
    print("Chose Position for O:")
    o_pos = int(input("1-9: "))
    while check_pos(o_pos-1) is False:
        print("This Place Is Occupied")
        o_pos = int(input("1-9: "))
    global o
    o.append(o_pos - 1)
    progress(o_pos - 1, "O")
    print("---------------------")


while True:
    if count % 2 == 0:
        x_turn()
    else:
        o_turn()
    if winner() is not None:
        print(winner()[0])
        break
    elif count == 8:
        print("It's a tie!")
        show_board()
        break
    count += 1