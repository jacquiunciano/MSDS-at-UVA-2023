import numpy as np
import pandas as pd
import unittest
from montecarlo import Dice as d
from montecarlo import Game as g
from montecarlo import Analyzer as a

class BookLoverTestSuite(unittest.TestCase):
    
    def test_1_init(self):
        mydie = d(np.array([1,2,3,4]))
        current = mydie.df
        expected = pd.DataFrame({"faces":[1,2,3,4],
                        "weights":[1,1,1,1]}).set_index("faces")
        message = "Hey, something is wrong with the initializer in Dice object!\
        It's not saving the dataframe correctly."
        self.assertEqual(current, expected, message)
        
    def test_2_change_weight(self):
        mydie = d([1,2,3,4])
        mydie.change_weight(2,2)
        current = mydie.df
        expected = pd.DataFrame({"faces":[1,2,3,4],
                        "weights":[1,2,1,1]}).set_index("faces")
        message = "Hey, something is wrong with the change_weight method in Dice object!\
        It's not updating the dataframe correctly."
        self.assertEqual(current, expected, message)
        
    def test_3_rolldie(self):
        

if __name__=='__main__':
    unittest.main(verbosity=3)