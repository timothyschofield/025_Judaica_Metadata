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

class NISC:
    def __init__(self, app_index, book_index, name):
        
        self.name = name
        self.first_part = dict()  
        self.second_part = dict()
        
        # For the two 000-0003L and 000-0004R NISC items that have to be written 
        # at the bottom of the non-NISC lines
        self.back_part = dict()
        
        self.output_path = None   
            
        print(f"\tNew NISC item: book_index {book_index} {self.name}")
        
    """
        Creates a NISC item folder and ocr folder but no XML is written
    """     
    def create_folders(self, output_path):       
        self.output_path = Path(f"{output_path}/{self.name}")
        print(f"\tNISC path:{self.output_path}")  
        
        self.output_path.mkdir(parents = True, exist_ok = True)       
        
        ocr_path = Path(f"{self.output_path}/ocr")
        ocr_path.mkdir(parents = True, exist_ok = True)
        
    """
    """       
    def update(self, app_index, book_index,  row):

        image_name = Path(row["Image name"]).stem
        
        # e.g. uni-ucl-jud-0015052-001-0001L
        # The only distinction I can think of between first_part and second_part is
        # that first_part images contain four zeros in the final section like "0000S" as opposed to three zeros like "0003L"
        end_bit = image_name.split("-")[-1]
        if "0000" in end_bit:
            # first_part
            self.first_part[image_name] = (book_index, row)
            # print(f"\t\tbook_index {book_index} {image_name} part 1")
        else:
            # second_part and back_part
            
            # If there is a second_part can we assume it is always 4 in length? As far as all the batches go this is true
            # If there is a back_part are always called 000-0003L and 000-0004R? As far as all the batches go this is true
            
            # For the two 000-0003L and 000-0004R NISC items that have to be written 
            # at the bottom of the non-NISC lines
            # This feels very arbitrary and fragile
            if end_bit == "0003L" or end_bit == "0004R":
                self.back_part[image_name] = (book_index, row)
            else:
                self.second_part[image_name] = (book_index, row)
            # print(f"\t\tbook_index {book_index} {image_name} part 2")
        
    """  
        Write first_part and second_part of NISC
    """ 
    def create_xml(self):
    
        return_data = f""
        image_number = 1
        order = 0
        # Write first_part
        for image_name, (book_index, row), in self.first_part.items():
        
            image_file_tag = "itemimagefile1"
            image_line_tag = "itemimage"
            this_line = self._create_xml_line(image_name, book_index, row, order, image_number, image_file_tag, image_line_tag)
            return_data =  f"{return_data}{this_line}"        
        
            image_number = image_number + 1

        order = 1
        # Write second_part
        for image_name, (book_index, row), in self.second_part.items():
            
            image_file_tag = "itemimagefile1"
            image_line_tag = "itemimage"            
            this_line = self._create_xml_line(image_name, book_index, row, order, image_number, image_file_tag, image_line_tag)
            return_data =  f"{return_data}{this_line}"
                            
            image_number = image_number + 1
            order = order + 1

        return return_data
    
    """
        Writes the back_part of NISC
        Called at the bottom of the Item _create_xml method
    """
    def create_xml_back_part(self, order, image_number):
        
        return_data = f""
        for image_name, (book_index, row), in self.back_part.items():
            
            image_file_tag = "itemimagefile1"
            image_line_tag = "itemimage"            
            this_line = self._create_xml_line(image_name, book_index, row, order, image_number, image_file_tag, image_line_tag)
            return_data =  f"{return_data}{this_line}"
                            
            image_number = image_number + 1
            order = order + 1
            
        return return_data
    
    """
    """
    def _create_xml_line(self, image_name, book_index, row, order, image_number, image_file_tag, image_line_tag):
        
        colour = row["colour"]
        colour_tab = f""
        if type(colour) == str:
            colour_tab = f"<colour>{colour}</colour>"

        page_type_1 = row["Page_type_1"] 
        if type(page_type_1) == str:
            page_type_1_tab = f"<pagetype>{page_type_1}</pagetype>"
        else:
            page_type_1_tab = f"<pagetype>None</pagetype>"                   
        
        page_type_2 = row["Page_type_2"] 
        page_type_2_tab = f""
        if type(page_type_2) == str:
            page_type_2_tab = f"<pagetype>{page_type_2}</pagetype>"
        
        return_data =  (
                        f"<{image_line_tag}>\n"
                        f"\t<{image_file_tag}>{image_name}</{image_file_tag}><order>{order}</order><imagenumber>{image_number}</imagenumber>{colour_tab}{page_type_1_tab}{page_type_2_tab}\n"
                        f"</{image_line_tag}>\n"
                       )
        
        return return_data
    
    
    
    
    
    
    
    

    
    
    
    
    
    