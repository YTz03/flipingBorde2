import unittest
from unittest.mock import patch
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

#============================================================================================================

    # Test 1: rotate_clockwise_once , N = 1
    @patch('builtins.input', return_value='1') 
    def test_rotate_clockwise_once(self, mock_input):
        
        new_board = self.game._rotate_clockwise(self.board, self.board_size)
        
        self.assertEqual(new_board[0][0][0], "7")
        self.assertEqual(new_board[0][2][0], "1") 

    # Test 2: rotate_counter_clockwise_once , N = 1
    @patch('builtins.input', return_value='1')
    def test_rotate_counter_clockwise_once(self, mock_input):
        
        new_board = self.game._rotate_counter_clockwise(self.board, self.board_size)
        
        self.assertEqual(new_board[0][0][0], "3") 
        self.assertEqual(new_board[0][2][0], "9")


#============================================================================================================

    # Test 3: rotate_counter_clockwise_twice , N = 2
    @patch('builtins.input', return_value='2')
    def test_rotate_clockwise_twice(self, mock_input):
        new_board = self.game._rotate_clockwise(self.board, self.board_size)
        
        self.assertEqual(new_board[2][2][0], "1")
    
    # Test 4: rotate_counter_clockwise_twice , N = 2
    @patch('builtins.input', return_value='2')
    def test_rotate_counter_clockwise_twice(self, mock_input):
        new_board = self.game._rotate_counter_clockwise(self.board, self.board_size)
        
        self.assertEqual(new_board[0][0][0], "9")


#============================================================================================================

    # Test 5: rotate_counter_clockwise_three_times , N = 3
    @patch('builtins.input', return_value='3')
    def test_rotate_clockwise_three_times(self, mock_input):
        new_board = self.game._rotate_clockwise(self.board, self.board_size)
        
        self.assertEqual(new_board[0][1][0], "6")
    
    # Test 6: rotate_counter_clockwise_three_times , N = 3
    @patch('builtins.input', return_value='3')
    def test_rotate_counter_clockwise_three_times(self, mock_input):
        new_board = self.game._rotate_counter_clockwise(self.board, self.board_size)
        
        self.assertEqual(new_board[1][2][0], "2") 

#============================================================================================================

    # Test 7: rotate_counter_clockwise_four_times , N = 4
    @patch('builtins.input', return_value='4')
    def test_rotate_clockwise_four_times(self, mock_input):
        new_board = self.game._rotate_clockwise(self.board, self.board_size)
        
        self.assertEqual(new_board[1][0][0], "4")
    
    # Test 8: rotate_counter_clockwise_four_times , N = 4
    @patch('builtins.input', return_value='4')
    def test_rotate_counter_clockwise_four_times(self, mock_input):
        new_board = self.game._rotate_counter_clockwise(self.board, self.board_size)
        
        self.assertEqual(new_board[2][1][0], "8") 
    


if __name__ == '__main__':
    unittest.main()