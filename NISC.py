"""
    NISC.py

    NISC material is non-Item information and acts as a header for a Book
    It containes info on Back board, Front board, Spine etc.
    It is of variable length
    
    NISC material has two parts:
    The first part contains info to do with the outward appearance of the book:
    Back board, Front board, Spine, Head edge, Tail edge etc.
    The second part is infomation on Front and Back endpaper which cannot be seen when the book is closed
    but still counts as a part of NISC.
    Both these parts are of variable length - including, in some cases, zero length
    
    Items in a Book "share" NISC data. This means that when an Item's XML file is written, the same NISC data is
    copied in at the start of each XML file within a Book.
    
    Same NISC data - exept the numbering in the <order> and <imagenumber> will vary between Items in Book
    
    
"""
from pathlib import Path
# The irst row is eaten by the init and subsequent rows are processed by update
# Call update at end of init
# Like wise for Book - we are missing the first row because the Book init is eating it
class NISC:
    def __init__(self, app_index, book_index, name):
        
        self.name = name
        self.first_part = dict()  
        self.second_part = dict()
        
        self.output_path = None   
            
        print(f"\tNew NISC item: book_index {book_index} {self.name}")
        
    """
        No XML written, but NISC item folder and empty ocr folder created
    """     
    def write_metadata(self, output_path):       
        self.output_path = Path(f"{output_path}/{self.name}")
        print(f"\tNISC path:{self.output_path}")  
        
        self.output_path.mkdir(parents = True, exist_ok = True)       
        
        ocr_path = Path(f"{self.output_path}/ocr")
        ocr_path.mkdir(parents = True, exist_ok = True)
        
    """
    """       
    def update(self, app_index, book_index,  row):

        image_name = Path(row["Image name"]).stem
        
        # The only distinction I can think of between first_part and second_part is 
        # that first_part images contain four zeros in the final section like "0000S" as opposed to three zeros like "0003L"
        end_bit = image_name.split("-")[-1]
        if "0000" in end_bit:
            # first_part
            self.first_part[image_name] = (book_index, row)
            # print(f"\t\tbook_index {book_index} {image_name} part 1")
        else:
            # second_part
            self.second_part[image_name] = (book_index, row)
            # print(f"\t\tbook_index {book_index} {image_name} part 2")       
        
        
    