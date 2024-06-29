"""
    Item.py

    Contains information on the regular (non NISC) pages in an Item
    
    Items in a Book "share" NISC data. This means that when an Item's XML file is written, 
    the same NISC data is copied in at the start of each XML file within a Book.

    >>>>>>>>>>>>>>>>> Give each Item in a Book a pointer to its shared NISC data



"""
from pathlib import Path

class Item:
    def __init__(self, app_index, item_name):
        self.item_name = item_name
        self.rows = dict()
        
        print(f"\tNew Item: {self.item_name}")
    
    def update(self, app_index, row):

        image_name = Path(row["Image name"]).stem
        print(f"\t\t{image_name}")
        
        self.rows[image_name] = row