import numpy as np
import pandas as pd
import unittest
import random as rn
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
        self.assertTrue(current.equals(expected), message)
        
    def test_2_change_weight(self):
        mydie = d(np.array([1,2,3,4]))
        mydie.change_weight(2,2)
        current = mydie.df.iloc[1].item()
        expected = 2
        message = "Hey, something is wrong with the change_weight method in Dice object!\
        It's not updating the dataframe correctly."
        self.assertEqual(current, expected, message)
        
    def test_3_rolldie(self):
        mydie = d(np.array([1,2,3,4]))
        current = len(mydie.rolldie(5))
        expected = 5
        message = "Hey, something is wrong with the rolldie method in Dice object!\
        It's not rolling the die the amount of times that you want."
        self.assertEqual(current, expected, message)
        
    def test_4_currentdie(self):
        mydie = d(np.array([1,2,3,4]))
        mydie.change_weight(2,2)
        current = mydie.currentdie()
        expected = pd.DataFrame({"faces":[1,2,3,4],
                        "weights":[1,2,1,1]}).set_index("faces")
        message = "Hey, something is wrong with the currentdie method in Dice object!\
        It's not returning the updated dataframe."
        self.assertTrue(current.equals(expected), message)
        
    def test_5_init(self):
        mydie1 = d(np.array([1,2,3,4]))
        mydie2 = d(np.array([1,2,3,4]))
        mygame = g([mydie1, mydie2])
        current = mygame.mylist
        expected = [mydie1, mydie2]
        message = "Hey, something is wrong with the initializer in Game object!\
        It's not saving the list correctly."
        self.assertEqual(current, expected, message)
        
    def test_6_play(self):
        mydie1 = d(np.array([1,2,3,4]))
        mydie2 = d(np.array([1,2,3,4]))
        mygame = g([mydie1, mydie2])
        mygame.play(4)
        current = mygame.df_rolls.shape
        expected = (4, 2)
        message = "Hey, something is wrong with the play method in Game object!\
        The dataframe is not saving as a wide dataframe correctly."
        self.assertEqual(current, expected, message)
        
    def test_7_recent_play(self):
        mydie1 = d(np.array([1,2,3,4]))
        mydie2 = d(np.array([1,2,3,4]))
        mygame = g([mydie1, mydie2])
        mygame.play(4)
        current = mygame.recent_play(narrow=True).shape
        expected = (8,1)
        message = "Hey, something is wrong with the recent play method in Game object!\
        The dataframe is not in long format."
        self.assertEqual(current, expected, message)
        
    def test_8_init(self):
        mydie1 = d(np.array([1,2,3,4]))
        mydie2 = d(np.array([1,2,3,4]))
        mygame = g([mydie1, mydie2])
        myana = a(mygame)
        current = myana.mygame
        message = "Hey, something is wrong with the initializer in Analyzer object!\
        The Game object did not save as a dataframe."
        self.assertTrue(isinstance(current, pd.DataFrame), message)
        
    def test_9_jackpot(self):
        mydie1 = d(np.array([1,2,3,4]))
        mydie2 = d(np.array([1,2,3,4]))
        mygame = g([mydie1, mydie2])
        myana = a(mygame)
        current = myana.jackpot()
        message = "Hey, something is wrong with the jackpot method in Analyzer object!\
        It's not returning an integer."
        self.assertTrue(isinstance(current, int), message)
        
    def test_10_face_counts(self):
        mydie1 = d(np.array([1,2,3,4]))
        mydie2 = d(np.array([1,2,3,4]))
        mygame = g([mydie1, mydie2])
        myana = a(mygame)
        test1 = myana.face_counts().index.name == "Roll Number"
        test2 = myana.face_counts().columns.name == "Face Number"
        test3 = all(myana.face_counts().apply(pd.Series.sum, axis=1)==2)
        message = "Hey, something is wrong with the face counts method in Analyzer object!\
        The data frame returned is not in the correct format."
        self.assertTrue(test1==test2==test3==True, message)
        
    def test_11_combo_count(self):
        mydie1 = d(np.array([1,2,3,4]))
        mydie2 = d(np.array([1,2,3,4]))
        mygame = g([mydie1, mydie2])
        myana = a(mygame)
        test1 = myana.combo_count()['Combo Count'].sum() == 0
        test2 = isinstance(myana.combo_count().index, pd.MultiIndex)
        message = "Hey, something is wrong with the combo count method in Analyzer object!\
        The dataframe returned is not in the correct format."
        self.assertTrue(test1==test2==True, message)
        
    def test_12_perm_count(self):
        mydie1 = d(np.array([1,2,3,4]))
        mydie2 = d(np.array([1,2,3,4]))
        mygame = g([mydie1, mydie2])
        myana = a(mygame)
        test1 = myana.perm_count()['Permutation Count'].sum() == 0 
        test2 = isinstance(myana.perm_count().index, pd.MultiIndex)
        message = "Hey, something is wrong with the perm count method in Analyzer object!\
        The dataframe returned is not in the correct format."
        self.assertTrue(test1==test2==True, message)
        
if __name__=='__main__':
    unittest.main(verbosity=3)