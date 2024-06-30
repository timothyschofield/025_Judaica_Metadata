"""
    Item.py

    Contains information on the regular (non NISC) pages in an Item
    
    Items in a Book "share" NISC data. This means that when an Item's XML file is written, 
    the same NISC data is copied in at the start of each XML file within a Book.

"""
from pathlib import Path
import math

class Item:
    def __init__(self, app_index, book_index, name, nisc_data, df_rec_search):
        
        self.name = name
        self.rows = dict()
        self.output_path = None
        self.df_rec_search = df_rec_search # All <rec_search> metadata
        
        # A pointer to the NISC data shared by all Items in this Book
        self.nisc_data = nisc_data
        
        print(f"\tNew Item: book_index {book_index} {self.name}")
    
    """
    """   
    def _create_xml(self):
        
        ret_data = f""
        ret_data = f"{ret_data}{self.nisc_data.create_xml()}"
        
        
        for image_name, (book_index, row), in self.rows.items():
            
            order = 0
            image_number = 0
            
            colour = row["Colour"]
            if type(colour) != str: colour = "None"

            page_type = row["Page Type"]   
            if type(page_type) != str: page_type = "None"     
                          
            # This is the basic line - all tabs included even if value "None"
            this_line = f"<itemimagefile1>{image_name}</itemimagefile1><order>{order}</order><imagenumber>1{image_number}</imagenumber><colour>{colour}</colour><pagetype>{page_type}</pagetype>"
            
            
            
            #######################
            # elements below here are not included in the output if they have no value
            page_number = row["Page number"] 
            if type(page_number) != str: page_number = ""
            this_line = f"{this_line}<orderlabel>{page_number}</orderlabel>"
        
            #######################
            # illustration_type_1 to illustration_type_5
            
            all_illustration_type = ""
            for i in range(1, 6):
                
                illustration_type = row[f"illustration_type_{i}"]  
                num_instances_of = row[f"instances_of_{i}"]
                
                # Collect the illustration types for the metadata
                #if type(illustration_type) == str: illustration_type_list.append(illustration_type)
                
                if type(illustration_type) == str:
               
                    if math.isnan(num_instances_of) == False: num_instances_of = int(num_instances_of)
                    else: num_instances_of = 1 # If some one has set the illustration type but forgotten to set num_instances_of to 1
                    
                    illustration_type = f'<pagecontent number="{num_instances_of}">{illustration_type}</pagecontent>'
                        
                    all_illustration_type = f"{all_illustration_type}{illustration_type}"
            
            this_line = f"{this_line}{all_illustration_type}"
            
            #######################
            translation = row["translation"]  
            if type(translation) != str: translation = ""
            else: translation = f"<translation>{translation}</translation>"
            
            this_line = f"{this_line}{translation}"

            # Wrap ithe line in tags for the image line
            ret_data = f"{ret_data}<itemimage>\n\t{this_line}\n</itemimage>\n" 
            
            
        return ret_data
  
    
    """
    """     
    def write_xml(self, output_path):
        self.output_path = Path(f"{output_path}/{self.name}")
        print(f"\tItem path:{self.output_path}")     
         
        self.output_path.mkdir(parents = True, exist_ok = True)
        
        ocr_path = Path(f"{self.output_path}/ocr")
        ocr_path.mkdir(parents = True, exist_ok = True)

        metadata_file = Path(f"{self.output_path}/{self.name}.xml")
        
        xml_data = self._create_xml()
        
        with open(metadata_file, 'a') as the_file:
            the_file.write(xml_data)
    
    """
    """   
    def update(self, app_index, book_index, row):

        image_name = Path(row["Image name"]).stem
        self.rows[image_name] = (book_index, row)
        #print(f"\t\tbook_index {book_index} {image_name}")
        
        
        