"""
    Item.py

    Contains information on the regular (non NISC) pages in an Item
    
    Items in a Book "share" NISC data. This means that when an Item's XML file is written, 
    the same NISC data is copied in at the start of each XML file within a Book.

"""
from pathlib import Path
import math
from helper_functions_judaica import validate_xml, decimal_encode_for_xml, log_message


class Item:
    def __init__(self, app_index, book_index, name, nisc_data, df_rec_search, my_book):
        
        self.name = name
        self.rows = dict()
        self.output_path = None
        
        # A pointer to the NISC data shared by all Items in this Book
        self.nisc_data = nisc_data
        
        # rec_search metadata for all Items
        self.df_rec_search = df_rec_search 
        
        self.my_book = my_book # A pointer to the book this item is part of
        
        # Collect all the illustration_types in this Item for the rec_search metadata
        self.illustration_type_list = []
        
        print(f"\tNew Item: book_index {book_index} {self.name}")
    
    """
    """   
    def _create_xml(self):
        
        ret_data =  (
                    f"<rec>\n\n<itemid>{self.name}</itemid>\n\n<subscription>\n\t<unit>unpublished</unit>\n\t<country>uni</country>\n</subscription>\n\n"
                    f"<itemimagefiles>\n"
                    )
        
        ret_data = f"{ret_data}{self.nisc_data.create_xml()}"
        
        # Now the main image non NISC lines
        len_first_part = len(self.nisc_data.first_part)
        len_second_part = len(self.nisc_data.second_part)
    
        # always counts on from order in the NISC
        order = len_second_part + 1
        
        # This depend on whether image_number resets with each new Item or just counts on through Items in a Book
        # In which case use book_index
        # Jessica says the image_number resetting for every item is the correct way
        image_number =  len_first_part + len_second_part + 1
        
        for image_name, (book_index, row), in self.rows.items():
            
            colour = row["Colour"]
            if type(colour) != str: colour = "None"

            page_type = row["Page Type"]   
            if type(page_type) != str: page_type = "None"     
                          
            # This is the basic line - all tabs included even if value "None"
            this_line = f"<itemimagefile1>{image_name}</itemimagefile1><order>{order}</order><imagenumber>{image_number}</imagenumber><colour>{colour}</colour><pagetype>{page_type}</pagetype>"
            
            #######################
            # elements below here are not included in the output if they have no value
            page_number = row["Page number"] 
            if type(page_number) == str:
                this_line = f"{this_line}<orderlabel>{page_number}</orderlabel>"
        
            #######################
            # illustration_type_1 to illustration_type_5 and instances_of_1 toinstances_of_5
            
            all_illustration_type = ""
            for i in range(1, 6):
                
                illustration_type = row[f"illustration_type_{i}"]  
                num_instances_of = row[f"instances_of_{i}"]
                
                # Collect the illustration types for the rec_search metadata
                if type(illustration_type) == str: self.illustration_type_list.append(illustration_type)
                
                if type(illustration_type) == str:
               
                    if math.isnan(num_instances_of) == False: num_instances_of = int(num_instances_of)
                    else: num_instances_of = 1 # If some one has set the illustration type but forgotten to set num_instances_of to 1
                    
                    illustration_type = f'<pagecontent number="{num_instances_of}">{illustration_type}</pagecontent>'
                        
                    all_illustration_type = f"{all_illustration_type}{illustration_type}"
            
            this_line = f"{this_line}{all_illustration_type}"
            
            #######################
            translation = row["translation"]
            if type(translation) == str: 
                this_line = f"{this_line}<translation>{translation}</translation>"
            
            # Wrap the line in tags for the image line
            ret_data = f"{ret_data}<itemimage>\n\t{this_line}\n</itemimage>\n" 
            
            order = order + 1
            image_number = image_number + 1
            # end of for each image line
        
        # list of unique illustration types for rec search metadata
        self.illustration_type_list = list(set(self.illustration_type_list))
        
        ret_data = f"{ret_data}</itemimagefiles>"
        
        ret_data = f"{ret_data}{self.create_rec_search_xml()}"

        return ret_data
  
    """
    """
    def create_rec_search_xml(self):
        
        # For the link section
        # Collect all the titles of the other Items in this Item's Book
        other_items_in_this_book = dict()
        for item_name, item, in self.my_book.items.items():
            
            print(f"Item name: {item_name}")
        
        
        this_line = self.df_rec_search.loc[self.name]
        pqid = this_line["<pqid>"]
        
        title = decimal_encode_for_xml(this_line["<title>"])
        
        author_main = this_line["<author_main>"]
        author_corrected = author_main
        author_uninverted = author_main
           
        imprint = this_line["<imprint>"]
        if type(imprint)!= str: imprint = "unknown"   
    
        startdate = this_line["<startdate>"]
        if math.isnan(startdate): startdate = "unknown" 
        else: startdate = int(startdate)   
    
        enddate = this_line["<enddate>"]
        if math.isnan(enddate): enddate = "unknown" 
        else: enddate = int(enddate)   
    
        displaydate = this_line["<displaydate>"]
        if math.isnan(displaydate): displaydate = "unknown" 
        else: displaydate = int(displaydate)    
    
        shelfmark = this_line["<shelfmark>"] 
        pagination = this_line["<pagination>"] 
        source_library = this_line["<source_library>"] 
        source_collection = this_line["<source_collection>"]
        language = this_line["<language>"]   
    
        illustrations_tag = f""
        if len(self.illustration_type_list) != 0:
            
            illustrations_tag = f"<illustrations>\n"
            for illustration in self.illustration_type_list:
                illustrations_tag = f"{illustrations_tag}\t<illustration>{illustration}</illustration>\n"
        
            illustrations_tag = f"{illustrations_tag}</illustrations>\n"   
    
        link_tag = f""
        links = this_line["<link>"]
        if type(links) == str:
            links_list = list(eval(links))
            
            link_tag = f"<linksec>\n"
            # Annoying thing with single tuple/link
            if type(links_list[0]) == str:
                this_link_title = decimal_encode_for_xml(links_list[0])
                this_link_id = links_list[1]
                link_tag = f"{link_tag}\t<link>\n\t\t<linktitle>{this_link_title}</linktitle>\n"
                link_tag = f"{link_tag}\t\t<linkid>{this_link_id}</linkid>\n\t</link>\n"
            else:
                # For multiple tuples/links
                for this_link in links_list:
                    this_link_title = this_link[0]
                    this_link_id = this_link[1] 
                    link_tag = f"{link_tag}\t<link>\n\t\t<linktitle>{this_link_title}</linktitle>\n"
                    link_tag = f"{link_tag}\t\t<linkid>{this_link_id}</linkid>\n\t</link>\n"       
            
            link_tag = f"{link_tag}</linksec>\n"   
    
    
        rec_search = (   f"\n\n<rec_search>\n<pqid>{pqid}</pqid>\n"
                        f"<title>{title}</title>\n"
                        f"<author_main>\n\t<author_name>{author_main}</author_name>\n\t<author_corrected>{author_corrected}</author_corrected>\n\t<author_uninverted>{author_uninverted}</author_uninverted>\n</author_main>\n"
                        f"<imprint>{imprint}</imprint>\n"
                        f"<startdate>{startdate}</startdate>\n"
                        f"<enddate>{enddate}</enddate>\n"
                        f"<displaydate>{displaydate}</displaydate>\n"
                        f"<shelfmark>{shelfmark}</shelfmark>\n"
                        f"<pagination>{pagination}</pagination>\n"
                        f"<source_library>{source_library}</source_library>\n"
                        f"<source_collection>{source_collection}</source_collection>\n"
                        f"<language>{language}</language>\n"
                        
                        f"{illustrations_tag}"
                        
                        f"\n</rec_search>\n\n"
                        
                        f"{link_tag}"
                        
                        f"\n</rec>"
            
                        )   
    
        return rec_search
    
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
        
        is_valid, message = validate_xml(xml_data)
        if is_valid == False:
            log_message(f"{metadata_file} - {message}")
        
        with open(metadata_file, 'a') as the_file:
            the_file.write(xml_data)
    
    """
    """   
    def update(self, app_index, book_index, row):

        image_name = Path(row["Image name"]).stem
        self.rows[image_name] = (book_index, row)
        #print(f"\t\tbook_index {book_index} {image_name}")
        
        
        