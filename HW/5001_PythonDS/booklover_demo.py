from booklover import BookLover as bl
import pandas as pd

df = pd.DataFrame({"book_name":["t", "b","c"], 
                   "book_rating":[1,2,3]})
testing = bl("Anna", "email", "mystery", 3, df)
testing.add_book("g", 4)
print(testing.num_books)