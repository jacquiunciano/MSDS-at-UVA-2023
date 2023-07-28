import pandas as pd
import numpy as np

class BookLover:
    
    name = ""
    email = ""
    fav_genre = ""
    num_books = 0
    book_list = pd.DataFrame()
    
    def __init__(self, name, email, fav_genre, 
                num_books=0, book_list=pd.DataFrame({"book_name":[], 
                                                     "book_rating":[]})):
        self.name = name
        self.email = email
        self.fav_genre = fav_genre
        self.num_books = num_books
        self.book_list = book_list
        self.num_books = len(book_list)
        
    def add_book(self, book_name, rating):
        blist = list(self.book_list.loc[:,"book_name"])
        
        if book_name not in blist:
            new_book = pd.DataFrame({"book_name":[book_name], 
                                     "book_rating":[rating]})
            self.book_list = pd.concat([self.book_list, new_book],
                                      ignore_index=True)
            self.num_books+=1
            print(f"Congrats! You have added {book_name} with a rating of {rating} to your records!")
        else:
            print("You have already included this book in your records!")
            
    def has_read(self, book_name):
        blist = list(self.book_list.loc[:,"book_name"])
        
        if book_name in blist:
            return True
        else:
            return False
        
    def num_books_read(self):
        if self.num_books==len(self.book_list):
            return self.num_books
        
    def fav_books(self):
        filtered = self.book_list\
        .loc[np.where(self.book_list["book_rating"]>3)]
        return filtered
        
