import pandas as pd
import numpy as np
from booklover import BookLover as bl
import unittest

class BookLoverTestSuite(unittest.TestCase):
    
    def test_1_add_book(self):
        df = pd.DataFrame({"book_name":["t", "b","c"], 
                                 "book_rating":[1,2,3]})
        testing = bl("Anna", "email", "mystery", 3, df)
    
        testing.add_book("g", 4)
        current = "g" in list(testing.book_list.loc[:,"book_name"])
        message = "Hey, something is wrong when adding the book.\
        The book you tried to add is not in the book list."
        self.assertTrue(current, message)
        
    def test_2_add_book(self):
        df = pd.DataFrame({"book_name":["t", "b","c"], 
                                 "book_rating":[1,2,3]})
        testing = bl("Anna", "email", "mystery", 3, df)
        testing.add_book("t", 4)
        current = list(testing.book_list.loc[:,"book_name"]).count('t')
        expected = 1
        message = "Hey, a book has appeared in the book list more than once."
        self.assertEqual(current, expected, message)
        
    def test_3_has_read(self):
        df = pd.DataFrame({"book_name":["t", "b","c"], 
                                 "book_rating":[1,2,3]})
        testing = bl("Anna", "email", "mystery", 3, df)
        current = testing.has_read("t")
        message = "Hey, a book that's supposed to be in the book list is not \
        in the book list."
        self.assertTrue(current, message)
        
    def test_4_has_read(self):
        df = pd.DataFrame({"book_name":["t", "b","c"], 
                                 "book_rating":[1,2,3]})
        testing = bl("Anna", "email", "mystery", 3, df)
        current = testing.has_read("h")
        message = "Hey, a book that's not supposed to be in the book list is \
        in the book list."
        self.assertFalse(current, message) 
        
    def test_5_num_books_read(self):
        df = pd.DataFrame({"book_name":["t", "b","c"], 
                                 "book_rating":[3,4,5]})
        testing = bl("Anna", "email", "mystery", 3, df) 
        current = testing.num_books_read()
        expected = 3
        message = "Hey, the number of books does not match the length of the \
        book list."
        self.assertEqual(current, expected, message)
        
    def test_6_fav_books(self):
        df = pd.DataFrame({"book_name":["t", "b","c"], 
                                 "book_rating":[3,4,5]})
        testing = bl("Anna", "email", "mystery", 3, df)
        current = all(testing.fav_books().book_rating > 3)
        message = "Hey, there's at least one book that has a rating <= 3."
        self.assertTrue(current, message)
        
if __name__=='__main__':
    unittest.main(verbosity=3)
        