"""
    Book.py
    e.g.
        uni-ucl-jud-0015052
        uni-ucl-jud-0015063 

"""
from pathlib import Path

from metadata_package import NISC as nisc_module
from metadata_package import Item as item_module

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
        All Item objects exist at this point
        
        We iterate through them twice.
        
        1) The first iteration we are collecting volumeimagefiles data.
        This is a complete collection of all image files data from all Items in a Book 
        
        2) On the seconds iteration XML data for each individual Item is generated. 
            The exact same volumeimagefiles data (collected above) is inserted into the middle of each Item's XML

    """       
    def write_xml(self, output_path):
        
        self.output_path = Path(f"{output_path}/{self.name}")
        print(f"Book path:{self.output_path}")
        
        # Writes a NISC item folder and ocr folder but no XML written
        # If it exists at all - sometimes there is no NISC data part 1 or part 2!
        if self.nisc_data is not None:
            self.nisc_data.create_folders(output_path=self.output_path)    # nisc_data is NoneType
        else:
            print("****self.nisc_data was None****")
        
        if len(self.items) == 1:
            volumeimagefiles_data = f""
            print("len is 1")
        else:
            volumeimagefiles_data = self.create_volumeimagefiles_data()
        
        for item_key, item, in self.items.items():
            item.write_xml(output_path=self.output_path, volumeimagefiles_data=volumeimagefiles_data)

    """
    <volumeimagefiles>
        NISC001
            lines001
                order = 0, imagenumber++
                
            lines002
                order = 3, imagenumber++
            ...
            
            linesXXX
                order = 3, imagenumber++
                
                ...
                at the end
                000-0003L order = NISC001, imagenumber++
                000-0004R order = NISC001, imagenumber++
    </volumeimagefiles>
    
    volumeimagefiles_data for all Items in this Book
    image_number gets passed to subsequent Items in a Book so their image_number can continue incrementing
    """
    def create_volumeimagefiles_data(self):
        
        volumeimagefiles_data = f"\n\n<volumeimagefiles>\n\n"
        image_number = 1
        for item_key, item, in self.items.items():
            
            this_data, image_number = item.get_item_volumeimagefiles_data(image_number)
            volumeimagefiles_data = f"{volumeimagefiles_data}{this_data}"
    
        back_part_001 = self.create_back_part_volumeimages_Item_001(image_number)
        volumeimagefiles_data = f"{volumeimagefiles_data}{back_part_001}"
    
        volumeimagefiles_data = f"{volumeimagefiles_data}\n</volumeimagefiles>\n"
    
        return volumeimagefiles_data
    
    """
        Create NISC back_part for volumeimagefile
        Only called with NISC info for Item 001
    """    
    def create_back_part_volumeimages_Item_001(self, image_number):
        
        # empty keys - problem was underscores in image name of 0050296
        # print(f"{self.name} The keys:{list(self.items.keys())}")
        
        item001_key = list(self.items.keys())[0]
        item001 = self.items[item001_key]
        
        returned_backpart = f""
        if item001.nisc_data is not None:
            image_file_tag = "volumeimagefile"
            image_line_tag = "volumeimage"  
            order = item001.order_for_volume_info_back_part
            # print(f"#################### order: {order}")     # 0 because we are collecting volumeimage this before the rest of the iteminfo is collected
            returned_backpart = item001.nisc_data.create_xml_back_part(order, image_number, image_file_tag, image_line_tag)
            
        return returned_backpart
    
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
                self.nisc_data = nisc_module.NISC(app_index=app_index, book_index=self.book_index, name=self.current_item_name)
                self.nisc_data.update(app_index=app_index, book_index=self.book_index, row=row)
            else:
                self.current_item = item_module.Item(app_index=app_index, book_index=self.book_index, name=self.current_item_name, nisc_data=self.nisc_data, df_rec_search=self.df_rec_search, my_book=self)
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
        
        