import datetime
import random


class New_Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

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
                print("Invalid input' enter number between 3 and 10.")
            
            else:
                board_size = int(board_size)

                if board_size > 2 and board_size < 11:

                    board = [[None for i in range(board_size)] for j in range(board_size)] # Initialize empty board

                    start_time = datetime.datetime.now()

                    self._game_engine(board, board_size)

                    end_time = datetime.datetime.now()
                    
                    duration_delta = end_time - start_time
                    self.duration = duration_delta.total_seconds()

                    break
                
                else: 
                    print("Invalid board size. Please choose a size between 3 and 10.")

    def _game_engine(self,board, board_size):
        round_count = 0

        while True:   
            round_count += 1

            base = random.randint(2,10) # Random base between 2 and 10
            print(f"\n = = = = = = = = = = \n Round {round_count} - base is: {base} \n = = = = = = = = = = \n")

            print(" - - - - - - - - - \n player 1 's turn \n - - - - - - - - - \n")

            self._print_board(board,board_size) # Print current board state

            action = input("Choose your action:\n 1) Insert number\n 2) Rotate Board ClockWise\n 3) Rotate Board CounterClockWise\n") # Get player action
            board, is_winner = self._exe_action(action, board, board_size, base) # Execute player action

            if is_winner != 0:
                self._print_board(board,board_size) # Print current board state

                if is_winner == 1:
                    print(f"Player 1 wins!")
                    self.game_result = 1

                elif is_winner == 2:
                    print(f"The board is full! It's a draw!")

                break

            print(" - - - - - - - - - \n player 2 's turn \n - - - - - - - - - \n")

            self._print_board(board,board_size) # Print current board state
            
            action = input("Choose your action:\n 1) Insert number\n 2) Rotate Board ClockWise\n 3) Rotate Board CounterClockWise\n") # Get player action
            board, is_winner = self._exe_action(action, board, board_size, base) # Execute player action

            if is_winner != 0:
                self._print_board(board,board_size) # Print current board state

                if is_winner == 1:
                    print(f"Player 1 wins!")
                    self.game_result = 2

                elif is_winner == 2:
                    print(f"The board is full! It's a draw!")
                    
                break
        
        self.rounds_played = round_count


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

    def _exe_action(self, action_number, board, board_size, base):
        is_winner = 0

        if action_number == '1': # Insert number
            board, is_winner = self._insert_number(board, board_size, base)

        elif action_number == '2': # Rotate Board ClockWise

            board = self._rotate_clockwise(board, board_size)

        elif action_number == '3': # Rotate Board CounterClockWise

            board = self._rotate_counter_clockwise(board, board_size)

        else:
            print("Invalid action, Please choose 1, 2, or 3.")
        
        return board, is_winner

    def _insert_number(self, board, board_size, base):

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
                    is_winner = self._check_winner(board, board_size, row, col)  # Check for a winner
                    return board, is_winner
                
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

    def _rotate_clockwise(self, board, board_size):
        while True:
            try:
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
            except:
                print("\nInvalid input, please enter a number\n")
                
    def _rotate_counter_clockwise(self, board, board_size):
        while True:
            try:
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
            except:
                print("\nInvalid input, please enter a number\n")

    def _check_equality(self, number_val_1, base_val_1, number_val_2, base_val_2):
        
        if base_val_1 == base_val_2 and number_val_1 == number_val_2:
            return True

        elif self._convert_to_decimal(number_val_1, base_val_1) == self._convert_to_decimal(number_val_2, base_val_2):
            return True
        

        return False

    def _check_winner(self, board, board_size, row, col):

        last_cell_number_val, last_cell_base_val = board[row][col] # last inserted cell values

        win = True
        for i in range(board_size):  # Check for win in row
            if board[row][i] is None:
                win = False
                break

            check_number_val, check_base_val = board[row][i]
            if not self._check_equality(last_cell_number_val, last_cell_base_val, check_number_val, check_base_val):
                win = False
                break        
        if win:
            return 1  # Winner

        win = True
        for i in range(board_size):  # Check for win in column
            if board[i][col] is None:
                win = False
                break

            check_number_val, check_base_val = board[i][col]
            if not self._check_equality(last_cell_number_val, last_cell_base_val, check_number_val, check_base_val):
                win = False
                break
        if win:
            return 1  # Winner

        if row == col: # check diagonal only if the last cell was on it
            win = True
            for i in range(board_size): # Diagonal 1 (top-left to bottom-right)
                if board[i][i] is None:
                    win = False
                    break
                check_number_val, check_base_val = board[i][i]
                if not self._check_equality(last_cell_number_val, last_cell_base_val, check_number_val, check_base_val):
                    win = False
                    break
            if win:
                return 1  # Winner
        
        if row + col == board_size - 1: # check diagonal only if the last cell was on it
            win = True
            for i in range(board_size): # Diagonal 2 (top-right to bottom-left)
                c = board_size - 1 - i
                if board[i][c] is None:
                    win = False
                    break
                check_number_val, check_base_val = board[i][c]
                if not self._check_equality(last_cell_number_val, last_cell_base_val, check_number_val, check_base_val):
                    win = False
                    break
            if win:
                return 1  # Winner
            
        for i in range(board_size): # Check if the board is full
            for j in range(board_size):
                if board[i][j] is None:
                    return 0 # Game continues
                
        return 2   # Draw

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

            return float(decimal_value)

        return float(number_val)

