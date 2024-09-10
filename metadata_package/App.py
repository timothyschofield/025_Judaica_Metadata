"""
    App.py

"""
from pathlib import Path 

# Book = Volume = Boundwith
# There can be any number of Books in one CSV
# e.g. uni-ucl-jud-0015053, uni-ucl-jud-0130519, uni-ucl-jud-0130524 are different books
# Any one Book can have multiple Items, 
# e.g. uni-ucl-jud-0130524-001, uni-ucl-jud-0130524-002 are different items of the Book uni-ucl-jud-0130524

from metadata_package import Book as book_module

class App:
    def __init__(self, df_metadata, df_rec_search, output_path):
        
        self.df_metadata = df_metadata
        self.df_rec_search = df_rec_search 
        
        self.output_path = output_path
        
        self.old_book_name = None
        self.current_book_name = None
        self.current_book = None
        self.books = dict() # A dictionary of Books indexed by the Book's name
        
        # Iterate through the metadata csv
        # And create a structured representation of the csv
        for app_index, row in self.df_metadata.iloc[0:].iterrows(): 
            self.update(app_index, row)

        print("##### WRITING XML #####")
        self.write_xml()

    """
    """    
    def write_xml(self):
        for book_key, book, in self.books.items():
            book.write_xml(output_path=self.output_path)
            
    """
    """         
    def update(self, app_index, row):        

        this_book_name = self._get_book_name(row)
        
        if this_book_name != self.current_book_name:
            self.old_book_name = self.current_book_name
            self.current_book_name = this_book_name
            
            self.current_book = book_module.Book(app_index=app_index, row=row, name=self.current_book_name, df_rec_search=self.df_rec_search)
            
            self.books[self.current_book_name] = self.current_book
            self.current_book.update(app_index=app_index, row=row)
        else:
            self.current_book.update(app_index=app_index, row=row)
            

    """
    """
    def _get_book_name(self, row):
            image_name = row["Image name"]                  
            file_name = Path(image_name).stem         
            
            file_name_list = file_name.split("-")
                           
            book_name = file_name_list[:-2]
            book_name = "-".join(book_name)
            
            return book_name


