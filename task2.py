import random

def print_board(board,board_size):
    print("\nCurrent board state:\n")

    separator = '-' * ((board_size * 19)+ 1)
    
    for row in range(board_size):
        print(separator)
        for col in range(board_size):
            if board[row][col] is None:
                print(f"| {' ' * 16} ", end='')
            else:
                size = len(board[row][col])
                print(f"| {board[row][col]} {' '*(15 -len(board[row][col]))} ", end='')
        print("|")

    print(separator)

def Exe_Action(action_number, board, board_size, base):
    is_winner = 0

    if action_number == '1': # Insert number
       board, is_winner = insert_number(board, board_size, base)

    elif action_number == '2': # Rotate Board ClockWise

        board = Rotate_ClockWise(board, board_size)

    elif action_number == '3': # Rotate Board CounterClockWise

        board = Rotate_CounterClockWise(board, board_size)

    else:
        print("Invalid action, Please choose 1, 2, or 3.")
    
    return board, is_winner

def insert_number(board, board_size, base):

    while True:
            row = int(input(f"Enter the row (1 to {board_size}) to insert the number: ")) - 1
            col = int(input(f"Enter the column (1 to {board_size}) to insert the number: ")) - 1
            number = (input(f"Enter a number in base {base} to insert: "))

            if row < 0 or row >= board_size or col < 0 or col >= board_size: # Check if selection in the board bounds
                print("\nRow or column out of bounds, Please try again.\n")

            elif board[row][col] is not None:   # Check if cell is already occupied
                print("\nCell already occupied, Please choose another cell.\n")
            
            elif len(number) > 10 or len(number) == 0:   # Check if number length is valid
                print("\nInvalid number length, Please try again.\n")

            elif not number_validation(number, base):   #Check if number is valid for the base
                print(f"\nInvalid number for base {base}, Please try again.\n")

            else:
                board[row][col] = f"{float(number)} ,B:{base}"  # Insert number into the board
                is_winner = check_winner(board, board_size, row, col)  # Check for a winner
                return board, is_winner
    
def number_validation(number, base):
    for index in number:
        if index != "." and int(index) >= base:
            return False
    return True

def Rotate_ClockWise(board, board_size):
    while True:

        number_of_rotations = int(input("Enter number of ClockWise rotations: "))

        if number_of_rotations <= 0:
            print("\nInvalid number of rotations, Please enter a positive integer.\n")

        else:
            for rotate in range(number_of_rotations % 4):
                new_board = [[None for i in range(board_size)] for j in range(board_size)]
                for i in range(board_size):
                    for j in range(board_size):
                        new_board[j][board_size - 1 - i] = board[i][j]
                board = new_board
            
            return board
            
def Rotate_CounterClockWise(board, board_size):
    while True:
        number_of_rotations = int(input("Enter number of counterClockWise rotations: "))

        if number_of_rotations <= 0:
            print("\nInvalid number of rotations, Please enter a positive integer.\n") 
        
        else:
            for rotate in range(number_of_rotations % 4):
                new_board = [[None for i in range(board_size)] for j in range(board_size)]
                for i in range(board_size):
                    for j in range(board_size):
                        new_board[board_size - 1 - j][i] = board[i][j]
                board = new_board

            return board 

def check_winner(board, board_size, row, col):

    win = True
    for i in range(board_size): # Check for win in row
        if board[row][i] is None or convert_to_decimel(board[row][i]) != convert_to_decimel(board[row][col]):
            win = False
            break
    if win:
        return 1 # Winner
    
    win = True
    for i in range(board_size): # Check for win in column
        if board[i][col] is None or convert_to_decimel(board[i][col]) != convert_to_decimel(board[row][col]):
            win = False
            break
    if win:
        return 1 # Winner

    win = True
    for i in range(board_size): # Check for win in diagonal 1
        if board[i][i] is None or convert_to_decimel(board[i][i]) != convert_to_decimel(board[row][col]):
            win = False
            break
    if win:
        return 1 # Winner
    
    win = True
    for i in range(board_size): # Check for win in diagonal 2
        if board[i][board_size - 1 - i] is None or convert_to_decimel(board[i][board_size - 1 - i]) != convert_to_decimel(board[row][col]):
            win = False
            break
    if win:
        return 1 # Winner
    
    for i in range(board_size): # Check if the board is full
        for j in range(board_size):
            if board[i][j] is None:
                return 0 # Game continues
            
    return 2   # Draw

def convert_to_decimel(cell_value):
    
    number = cell_value.split(" ,B:")[0]
    base = int(cell_value.split(" ,B:")[1])

    if base != 10:
        point_index = number.index('.') 
        after_point = len(number) - point_index # count of digits after point

        decimal_value = 0

        j = 0
        for i in range(point_index-1, (-1 * after_point), -1): # go through each power
            
                if j == point_index: # skip the point
                    j += 1

                decimal_value += int(number[j]) * (base ** i)  
                j += 1

        return decimal_value


    return float(number)


if __name__ == "__main__":

    print("=================================\n Welcome to the Board Game! \n=================================\n")

    board_size = int(input("Choose board size (3-10): ")) # Get board size from user

    if board_size > 2 and board_size < 11:

        board = [[None for i in range(board_size)] for j in range(board_size)] # Initialize empty board
        converted_board = [[None for i in range(board_size)] for j in range(board_size)] # Initialize empty board to hold converted values

        round_count = 0

        while True:   
            round_count += 1

            base = random.randint(2,10) # Random base between 2 and 10
            print(f"\n = = = = = = = = = = \n Round {round_count} - base is: {base} \n = = = = = = = = = = \n")

            print(" - - - - - - - - - \n player 1 's turn \n - - - - - - - - - \n")

            print_board(board,board_size) # Print current board state

            action = input("Choose your action:\n 1) Insert number\n 2) Rotate Board ClockWise\n 3) Rotate Board CounterClockWise\n") # Get player action
            board, is_winner = Exe_Action(action, board, board_size, base) # Execute player action

            if is_winner == 1:
                print(f"Player 1 wins!")
                break

            elif is_winner == 2:
                print(f"The board is full! It's a draw!")
                break

            print(" - - - - - - - - - \n player 2 's turn \n - - - - - - - - - \n")

            print_board(board,board_size) # Print current board state
            
            action = input("Choose your action:\n 1) Insert number\n 2) Rotate Board ClockWise\n 3) Rotate Board CounterClockWise\n") # Get player action
            board, is_winner = Exe_Action(action, board, board_size, base) # Execute player action

            if is_winner == 1:
                print(f"Player 2 wins!")
                break

            elif is_winner == 2:
                print(f"The board is full! It's a draw!")
                break
        

    else: 
        print("Invalid board size. Please choose a size between 3 and 10.")