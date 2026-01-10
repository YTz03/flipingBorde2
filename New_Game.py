import datetime
import random


class New_Game:
    def __init__(self, player1, player2):
        self.player1 = player1  # just player name
        self.player2 = player2  # just player name

        self.game_result = 0 # 0 - draw, 1 - player 1 wins, 2 - player 2 wins

        self.rounds_played = 0

        self.duration = 0

 
    def play(self):

        self._start_new_game()

        return self.game_result, self.rounds_played, self.duration

    
    def _start_new_game(self):
        print("\n===============Game started===============\n")

        while True:
            board_size = input("Choose board size (3-10): ") # Get board size from user

            if not board_size.isdigit():
                print("Invalid input, enter number between 3 and 10.")
            
            else:
                board_size = int(board_size)

                if board_size > 2 and board_size < 11:

                    board = [[None for i in range(board_size)] for j in range(board_size)] # Initialize empty board
                    decimal_board = [[None for i in range(board_size)] for j in range(board_size)] # Initialize empty decimal board

                    start_time = datetime.datetime.now()

                    self._game_engine(board, board_size, decimal_board)

                    end_time = datetime.datetime.now()
                    
                    duration_delta = end_time - start_time
                    self.duration = duration_delta.total_seconds()

                    break
                
                else: 
                    print("Invalid board size. Please choose a size between 3 and 10.")

    def _game_engine(self,board, board_size, decimal_board):
        round_count = 0
        full_board = board_size ** 2
        filled_cells_counter = 0

        while True:   
            round_count += 1

            base = random.randint(2,10) # Random base between 2 and 10
            print(f"\n = = = = = = = = = = \n Round {round_count} - base is: {base} \n = = = = = = = = = = \n")

            print(f" - - - - - - - - - \n {self.player1}'s turn \n - - - - - - - - - \n")

            self._print_board(board,board_size) # Print current board state

            board, board_size, decimal_board, base, is_winner, filled_cells_counter = self._singel_turn(board, board_size, decimal_board, base, filled_cells_counter)

            if self._check_game_status(board, board_size, is_winner, filled_cells_counter, full_board, 1): # if game over
                break

            print(f" - - - - - - - - - \n {self.player2}'s turn \n - - - - - - - - - \n")

            self._print_board(board,board_size) # Print current board state
            
            board, board_size, decimal_board, base, is_winner, filled_cells_counter = self._singel_turn(board, board_size, decimal_board, base, filled_cells_counter)

            if self._check_game_status(board, board_size, is_winner, filled_cells_counter, full_board, 2): # if game over
                break

        
        self.rounds_played = round_count


    def _singel_turn(self, board, board_size, decimal_board, base, filled_cells_counter):
            turn_completed = False
            while not turn_completed:
                action = input("Choose your action:\n 1) Insert number\n 2) Rotate Board ClockWise\n 3) Rotate Board CounterClockWise\n") # Get player action
                
                if action != "1" and action != "2" and action != "3":
                    print("Invalid action, Please choose 1, 2, or 3.")

                else:
                    board, decimal_board, is_winner, success = self._exe_action(action, board, board_size, decimal_board, base) # Execute player action
        
                    if success:
                        turn_completed = True
                        
                        if action == "1":
                            filled_cells_counter +=1
                    else:
                        print(f"\nAction faild")

            return board, board_size, decimal_board, base, is_winner, filled_cells_counter

    def _check_game_status(self, board, board_size, is_winner, filled_cells_counter, full_board, player):
        if is_winner == 1:
            self._print_board(board,board_size) # Print current board state
            if player == 1:
                print(f"{self.player1} wins!")
                self.game_result = 1
            else:
                print(f"{self.player2} wins!")
                self.game_result = 2
            return True
        
        elif filled_cells_counter == full_board:
            self._print_board(board,board_size) # Print current board state
            print(f"The board is full! It's a draw!")
            self.game_result = 0
            return True
        
        return False

    def _print_board(self, board, board_size):
        print("\nCurrent board state:\n")

        separator = '-' * ((board_size * 19)+ 1)
        
        for row in range(board_size):
            print(separator)
            for col in range(board_size):
                if board[row][col] is None:
                    print(f"| {' ' * 16} ", end='')
                else:
                    number_val, base_val = board[row][col]
                    cell_str = f"{number_val} ,B:{base_val}"
                    size = len(cell_str)
                    print(f"| {cell_str} {' '*(15 - size)} ", end='')
            print("|")

        print(separator)

    def _exe_action(self, action_number, board, board_size, decimal_board, base):
        is_winner = 0
        success = False

        if action_number == '1': # Insert number
            board, decimal_board, is_winner, success = self._insert_number(board, board_size, decimal_board, base)

        elif action_number == '2': # Rotate Board ClockWise

            while True:
                try: 
                    number_of_rotations = int(input("Enter number of ClockWise rotations: "))
                    if number_of_rotations <= 0:
                        print("\nInvalid number of rotations, Please enter a positive integer.\n")
                    else:
                        break
                except:
                    print("\nInvalid input, please enter a positive integer")

            board, decimal_board = self._board_rotate(board, board_size, decimal_board, number_of_rotations)
            success = True

        elif action_number == '3': # Rotate Board CounterClockWise
            while True:
                try:
                    number_of_rotations = int(input("Enter number of counterClockWise rotations: "))
                    if number_of_rotations <= 0:
                        print("\nInvalid number of rotations, Please enter a positive integer.\n") 
                    else:
                        break
                except:
                    print("\nInvalid input, please enter a positive integer")
            
            fixd_number_of_rotations = (4 - (number_of_rotations % 4)) % 4

            board, decimal_board = self._board_rotate(board, board_size, decimal_board, fixd_number_of_rotations)
            success = True

        else:
            print("Invalid action, Please choose 1, 2, or 3.")
        
        return board, decimal_board, is_winner, success

    def _insert_number(self, board, board_size, decimal_board, base):

        while True:
            try: 
                row = int(input(f"Enter the row (1 to {board_size}) to insert the number: ")) - 1
                col = int(input(f"Enter the column (1 to {board_size}) to insert the number: ")) - 1
                number = input(f"Enter a number in base {base} to insert: ")

                if row < 0 or row >= board_size or col < 0 or col >= board_size: # Check if selection in the board bounds
                    print("\nRow or column out of bounds, Please try again.\n")

                elif board[row][col] is not None:   # Check if cell is already occupied
                    print("\nCell already occupied, Please choose another cell.\n")
                
                elif len(number) > 10 or len(number) == 0:   # Check if number length is valid
                    print("\nInvalid number length, Please try again.\n")

                elif not self._number_validation(number, base):   #Check if number is valid for the base
                    print(f"\nInvalid number, Must contain exactly one dot (.) and formatted 'dddd.dddd' with valid digits for base {base}.\n")

                else:
                    board[row][col] = (number, int(base))  # Insert number into the board as tuple - (number:str base:int)

                    if base != 10:
                        decimal_val = self._convert_to_decimal(number, int(base))
                        decimal_board[row][col] = decimal_val # Insert number into the board as float
                    else:
                        decimal_board[row][col] = str(float(number)) # Insert number into the board as float

                    is_winner = self._check_winner(decimal_board, board_size, row, col)  # Check for a winner
                    return board, decimal_board, is_winner, True
                
            except:
                print("\nInvalid input, please try again.\n")
            
    def _number_validation(self, number, base):
        if number.count(".") != 1:
            return False
        
        parts = number.split('.')
        if len(parts) != 2:
            return False
        
        elif not (1 <= len(parts[0]) <= 4) or not (1 <= len(parts[1]) <= 4):
            return False
        
        for char in number:
            if char == ".":
                continue

            elif not char.isdigit():
                return False

            elif int(char) >= base:
                return False
            
        
        return True

    def _board_rotate(self, board, board_size, decimal_board, number_of_rotations):
                for rotate in range(number_of_rotations % 4):
                    new_board = [[None for i in range(board_size)] for j in range(board_size)] 
                    new_decimal_board = [[None for i in range(board_size)] for j in range(board_size)] # decimal board
                    for i in range(board_size):
                        for j in range(board_size):
                            new_board[j][board_size - 1 - i] = board[i][j]
                            new_decimal_board[j][board_size - 1 - i] = decimal_board[i][j]
                    board = new_board
                    decimal_board = new_decimal_board
                
                return board, decimal_board
        
    def _check_winner(self, decimal_board, board_size, row, col):

        last_cell_number_val = decimal_board[row][col] # last inserted cell values

        win = True
        for i in range(board_size):  # Check for win in row
            if decimal_board[row][i] is None:
                win = False
                break

            check_number_val = decimal_board[row][i]
            if last_cell_number_val != check_number_val:
                win = False
                break        
        if win:
            return 1  # Winner

        win = True
        for i in range(board_size):  # Check for win in column
            if decimal_board[i][col] is None:
                win = False
                break

            check_number_val = decimal_board[i][col]
            if last_cell_number_val != check_number_val:
                win = False
                break
        if win:
            return 1  # Winner

        if row == col: # check diagonal only if the last cell was on it
            win = True
            for i in range(board_size): # Diagonal 1 (top-left to bottom-right)
                if decimal_board[i][i] is None:
                    win = False
                    break
                check_number_val = decimal_board[i][i]
                if last_cell_number_val != check_number_val:
                    win = False
                    break
            if win:
                return 1  # Winner
        
        if row + col == board_size - 1: # check diagonal only if the last cell was on it
            win = True
            for i in range(board_size): # Diagonal 2 (top-right to bottom-left)
                c = board_size - 1 - i
                if decimal_board[i][c] is None:
                    win = False
                    break
                check_number_val = decimal_board[i][c]
                if last_cell_number_val != check_number_val:
                    win = False
                    break
            if win:
                return 1  # Winner
            
        return 0

    def _convert_to_decimal(self, number_val, base_val):
        if base_val != 10:
            # Convert float to string to process digits
            point_index = number_val.index('.')
            after_point = len(number_val) - point_index

            decimal_value = 0

            j = 0
            for i in range(point_index - 1, (-1 * after_point), -1):  # go through each power
                if j == point_index:  # skip the point
                    j += 1

                decimal_value += int(number_val[j]) * (base_val ** i)
                j += 1

            return str(float(decimal_value))
        
        return str(float(number_val))


