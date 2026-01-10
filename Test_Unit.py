import unittest
from New_Game import New_Game 

class TestGameRotation(unittest.TestCase):

    def setUp(self):

        self.game = New_Game("Test1", "Test2")
        

        self.board_size = 3
        self.board = [
            [("1", 10), ("2", 10), ("3", 10)],
            [("4", 10), ("5", 10), ("6", 10)],
            [("7", 10), ("8", 10), ("9", 10)]
        ]

        self.decimal_board = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]

#============================================================================================================

    # Test 1: rotate_clockwise_once , N = 1
    def test_rotate_clockwise_once(self):
        new_board, new_decimal = self.game._board_rotate(self.board, self.board_size, self.decimal_board, 1)
        
        self.assertEqual(new_board[0][0][0], "7")
        self.assertEqual(new_board[0][2][0], "1")

        # decimal board checks
        self.assertEqual(new_decimal[0][0], "7")
        self.assertEqual(new_decimal[0][2], "1") 

    # Test 2: rotate_counter_clockwise_once , N = 1
    def test_rotate_counter_clockwise_once(self):
        rotations = (4 - (1 % 4)) % 4  
        new_board, new_decimal = self.game._board_rotate(self.board, self.board_size, self.decimal_board, rotations)
        
        self.assertEqual(new_board[0][0][0], "3") 
        self.assertEqual(new_board[0][2][0], "9")

        # decimal board checks
        self.assertEqual(new_decimal[0][0], "3")
        self.assertEqual(new_decimal[0][2], "9")


#============================================================================================================

    # Test 3: rotate_clockwise_twice , N = 2
    def test_rotate_clockwise_twice(self):
        new_board, new_decimal = self.game._board_rotate(self.board, self.board_size, self.decimal_board, 2)
        
        self.assertEqual(new_board[2][2][0], "1")

        # decimal board checks
        self.assertEqual(new_decimal[2][2], "1")
    
    # Test 4: rotate_counter_clockwise_twice , N = 2
    def test_rotate_counter_clockwise_twice(self):
        rotations = (4 - (2 % 4)) % 4
        new_board, new_decimal = self.game._board_rotate(self.board, self.board_size, self.decimal_board, rotations)
        
        self.assertEqual(new_board[0][0][0], "9")

        # decimal board checks
        self.assertEqual(new_decimal[0][0], "9")


#============================================================================================================

    # Test 5: rotate_counter_clockwise_three_times , N = 3
    def test_rotate_clockwise_three_times(self):
        new_board, new_decimal = self.game._board_rotate(self.board, self.board_size, self.decimal_board, 3)
        
        self.assertEqual(new_board[0][1][0], "6")

        # decimal board checks
        self.assertEqual(new_decimal[0][1], "6")
    
    # Test 6: rotate_counter_clockwise_three_times , N = 3
    def test_rotate_counter_clockwise_three_times(self):
        rotations = (4 - (3 % 4)) % 4
        new_board, new_decimal = self.game._board_rotate(self.board, self.board_size, self.decimal_board, rotations)
        
        self.assertEqual(new_board[1][2][0], "2") 

        # decimal board checks
        self.assertEqual(new_decimal[1][2], "2") 

#============================================================================================================

    # Test 7: rotate_clockwise_four_times , N = 4
    def test_rotate_clockwise_four_times(self):
        new_board, new_decimal = self.game._board_rotate(self.board, self.board_size, self.decimal_board, 4)
        
        self.assertEqual(new_board[1][0][0], "4")

        # decimal board checks
        self.assertEqual(new_decimal[1][0], "4")
    
    # Test 8: rotate_counter_clockwise_four_times , N = 4
    def test_rotate_counter_clockwise_four_times(self):
        rotations = (4 - (4 % 4)) % 4  
        new_board, new_decimal = self.game._board_rotate(self.board, self.board_size, self.decimal_board, rotations)
        
        self.assertEqual(new_board[2][1][0], "8") 

        # decimal board checks
        self.assertEqual(new_decimal[2][1], "8") 
    


if __name__ == '__main__':
    unittest.main()