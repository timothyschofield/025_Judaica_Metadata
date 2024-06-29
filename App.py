"""
    App.py

"""
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from helper_functions_judaica import get_file_timestamp

from Book import Book

class App:
    def __init__(self, df_metadata, output_path):
        
        self.df_metadata = df_metadata
        self.output_path = output_path
        
        self.old_book_name = None
        self.current_book_name = None
        self.current_book = None
        self.books = dict() # A dictionary of Books indexed by the Book's name
        
        # Iterate through the metadata csv
        # And create a structured representation of the csv
        for app_index, row in self.df_metadata.iloc[0:].iterrows(): 
            self.update(app_index, row)

    """
    """        
    def update(self, app_index, row):        

        this_book_name = self._get_book_name(row)
        
        if this_book_name != self.current_book_name:
            self.old_book_name = self.current_book_name
            self.current_book_name = this_book_name
            
            self.current_book = Book(app_index, row, self.current_book_name)
            self.books[self.current_book_name] = self.current_book
            self.current_book.update(app_index, row)
        else:
            self.current_book.update(app_index, row)
            

    """
    """
    def _get_book_name(self, row):
            image_name = row["Image name"]                  
            file_name = Path(image_name).stem         
            
            file_name_list = file_name.split("-")
                           
            book_name = file_name_list[:-2]
            book_name = "-".join(book_name)
            
            return book_name


