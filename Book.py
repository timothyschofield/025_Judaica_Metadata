"""
    Book.py
    e.g.
        uni-ucl-jud-0015052
        uni-ucl-jud-0015063

"""
from pathlib import Path

from NISC import NISC
from Item import Item

class Book:
    def __init__(self, app_index, row, name, df_rec_search):

        self.row = row
        self.name = name
        self.df_rec_search = df_rec_search # All <rec_search> metadata
        
        
        self.old_item_name = None
        self.current_item_name = None
        self.current_item = None
        
        self.items = dict() # A dictionary of Items indexed by the Item's name
        self.nisc_data = None
        
        self.is_nisc = False
        
        self.output_path = None
        
        # book_index is the index of the NISC or Item within the Book
        self.book_index = 1
        print(f"New Book: book_index {self.book_index} {self.name}")
        
    """
    """       
    def write_xml(self, output_path):
        
        self.output_path = Path(f"{output_path}/{self.name}")
        print(f"Book path:{self.output_path}")
        
        # Writes a NISC item folder and ocr folder but no XML written
        self.nisc_data.write_folders(output_path=self.output_path)
        
        for item_key, item, in self.items.items():
            item.write_xml(output_path=self.output_path)

    """
    """
    def update(self, app_index, row):
        self.row = row
        
        this_item_name = self._get_item_name(row)
        if this_item_name != self.current_item_name:
            self.old_item_name = self.current_item_name
            self.current_item_name = this_item_name
            
            # If the last three characters of the current_item_name = "000"
            # Then this is NISC data associated with the Book not a new Item
            if self.current_item_name[-3:] == "000": self.is_nisc = True
            else: self.is_nisc = False
            
            # Create either a new NISC instance for this Book or
            # A new Item for the items list 
            if self.is_nisc:
                self.nisc_data = NISC(app_index=app_index, book_index=self.book_index, name=self.current_item_name)
                self.nisc_data.update(app_index=app_index, book_index=self.book_index, row=row)
            else:
                self.current_item = Item(app_index=app_index, book_index=self.book_index, name=self.current_item_name, nisc_data=self.nisc_data, df_rec_search=self.df_rec_search, my_book=self)
                self.items[self.current_item_name] = self.current_item
                self.current_item.update(app_index, self.book_index, row)
                
            self.book_index = self.book_index + 1
        else:
            if self.is_nisc:  
                self.nisc_data.update(app_index=app_index, book_index=self.book_index, row=row)
            else:
                self.current_item.update(app_index=app_index, book_index=self.book_index, row=row)
                
            self.book_index = self.book_index + 1
        
    def _get_item_name(self, row):
        image_name = row["Image name"]                  
        file_name = Path(image_name).stem         
        
        file_name_list = file_name.split("-")
                        
        item_name = file_name_list[:-1]
        item_name = "-".join(item_name) 
        
        return item_name 
        
        