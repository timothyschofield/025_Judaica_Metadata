"""
    Item.py

    Contains information on the regular (non NISC) pages in an Item
    
    Items in a Book "share" NISC data. This means that when an Item's XML file is written, 
    the same NISC data is copied in at the start of each XML file within a Book.

"""
from pathlib import Path

class Item:
    def __init__(self, app_index, book_index, name, nisc_data):
        
        self.name = name
        self.rows = dict()
        self.output_path = None
        self.metadata = None
        
        # A pointer to the NISC data shared by all Items in this Book
        self.nisc_data = nisc_data
        
        print(f"\tNew Item: book_index {book_index} {self.name} nisc_data:{self.nisc_data}")
    
    """
    """     
    def write_xml(self, output_path):
        self.output_path = Path(f"{output_path}/{self.name}")
        print(f"\tItem path:{self.output_path}")     
         
        self.output_path.mkdir(parents = True, exist_ok = True)
        
        ocr_path = Path(f"{self.output_path}/ocr")
        ocr_path.mkdir(parents = True, exist_ok = True)

        metadata_file = Path(f"{self.output_path}/{self.name}.xml")
        
        xml_data = self.create_xml()
        
        with open(metadata_file, 'a') as the_file:
            the_file.write(xml_data)

    """
    """   
    def create_xml(self):
        
        ret_data = "No data"
        return ret_data
    
    
    """
    """   
    def update(self, app_index, book_index, row):

        image_name = Path(row["Image name"]).stem
        self.rows[image_name] = (book_index, row)
        #print(f"\t\tbook_index {book_index} {image_name}")
        
        
        