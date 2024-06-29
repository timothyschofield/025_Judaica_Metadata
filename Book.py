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
    def __init__(self, app_index, row, name):

        self.row = row
        self.name = name
        print(f"New Book: {self.name}")
         
        self.old_item_name = None
        self.current_item_name = None
        self.current_item = None
        
        self.items = dict() # A dictionary of Items indexed by the Item's name
        self.nisc_data = None
        
        self.is_nisc = False
        
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
                self.nisc_data = NISC(app_index, self.current_item_name)
                self.nisc_data.update(app_index, row)
            else:
                self.current_item = Item(app_index, self.current_item_name)
                self.items[self.current_item_name] = self.current_item
                self.current_item.update(app_index, row) 
        else:
            if self.is_nisc:  
                self.nisc_data.update(app_index, row)
            else:
                self.current_item.update(app_index, row)

        
    def _get_item_name(self, row):
        image_name = row["Image name"]                  
        file_name = Path(image_name).stem         
        
        file_name_list = file_name.split("-")
                        
        item_name = file_name_list[:-1]
        item_name = "-".join(item_name) 
        
        return item_name 
        
        