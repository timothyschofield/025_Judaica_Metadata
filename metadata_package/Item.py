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
        
        # Header for the XML file
        return_data =  (
                    f"<rec>\n\n<itemid>{self.name}</itemid>\n\n<subscription>\n\t<unit>unpublished</unit>\n\t<country>uni</country>\n</subscription>\n\n"
                    f"<itemimagefiles>\n"
                    )
        
        # Writes a NISC item folder and ocr folder but no XML written
        # If it exists at all - sometimes there is no NISC data part 1 or part 2!
        if self.nisc_data is not None:
            
            # Writes all the NISC XML
            return_data = f"{return_data}{self.nisc_data.create_xml()}"
        
            # Now the main image non NISC lines
            len_first_part = len(self.nisc_data.first_part)
            len_second_part = len(self.nisc_data.second_part)
        
            # always counts on from order in the NISC
            order = len_second_part + 1
            
            # This depend on whether image_number resets with each new Item or just counts on through Items in a Book
            # In which case use book_index
            # Jessica says the image_number resetting for every item is the correct way
            image_number =  len_first_part + len_second_part + 1
        else:
            # If no NISC data
            order = 0 + 1
            image_number =  0 + 0 + 1
        
     
        # Create lines for the regular non-NISC metadata
        for image_name, (book_index, row), in self.rows.items():
            
            image_file_tag = "itemimagefile1"
            image_line_tag = "itemimage"
            this_line = self._create_xml_line(image_name, book_index, row, order, image_number, image_file_tag, image_line_tag)
            return_data = f"{return_data}{this_line}"
            
            order = order + 1
            image_number = image_number + 1
            # end of for each image line
        
        # list of unique illustration types used in rec_search metadata
        # Collected in _create_xml_line, squash into a set and make a list of it
        self.illustration_type_list = list(set(self.illustration_type_list))
        
        # After all the non-NISC lines written
        # We write the back_part - if there is a back_part
        if self.nisc_data is not None:
            returned_backpart = self.nisc_data.create_xml_back_part(order, image_number)
            return_data = f"{return_data}{returned_backpart}"
        
        return_data = f"{return_data}</itemimagefiles>"
        
        
        # <volumeimagefiles> section goes here
        # and contains info on ALL items in the Volume
        # so item001.xml contains info on item002.xml etc.
        # So must be collected BEFORE all Items _create_xml methods
        
        return_data = f"{return_data}{self._create_rec_search_xml()}"

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
            
            
        page_number = row["Pagenumber"]
        orderlabel_tag = f""
        if type(page_number) == str:
            orderlabel_tag = f"<orderlabel>{page_number}</orderlabel>"    
            
        this_line = f"<{image_file_tag}>{image_name}</{image_file_tag}><order>{order}</order><imagenumber>{image_number}</imagenumber>{orderlabel_tag}{colour_tab}{page_type_1_tab}{page_type_2_tab}"  
        
        # illustration_type_1 to illustration_type_5 and instances_of_1 toinstances_of_5
        all_illustration_type = ""
        for i in range(1, 6):
            
            illustration_type = row[f"illustration_type_{i}"]  
            num_instances_of = row[f"instances_of_{i}"]
            
            # Collect the illustration types for the rec_search metadata
            # Can this cause problems when collecting for volumeimage
            if type(illustration_type) == str: self.illustration_type_list.append(illustration_type)
            
            if type(illustration_type) == str:
            
                if math.isnan(num_instances_of) == False: num_instances_of = int(num_instances_of)
                else: num_instances_of = 1 # If some one has set the illustration type but forgotten to set num_instances_of to 1
                
                illustration_type = f'<pagecontent number="{num_instances_of}">{illustration_type}</pagecontent>'
                    
                all_illustration_type = f"{all_illustration_type}{illustration_type}"
        
        this_line = f"{this_line}{all_illustration_type}"
        
        # Wrap the line in tags for the image line
        return_data = f"<{image_line_tag}>\n\t{this_line}\n</{image_line_tag}>\n" 
    
        return return_data

    """
    """
    def _create_rec_search_xml(self):
        
        this_line = self.df_rec_search.loc[self.name]
        pqid = this_line["<pqid>"]
        
        title = decimal_encode_for_xml(this_line["<title>"])
        
        author_main = this_line["<author_name>"]
        author_corrected = this_line["<author_corrected>"]      # new
        author_uninverted = this_line["<author_uninverted>"]    # new
           
        # shelfmark publisher_printer place_of_publication country_of_publication pagination
        # All of these have no tag if no value
        publisher_printer = this_line["<publisher_printer>"]
        publisher_printer_tag = f""
        if type(publisher_printer) == str and publisher_printer != "":
            publisher_printer_tag = f"<publisher_printer>{publisher_printer}</publisher_printer>\n" 

        place_of_publication = this_line["<place_of_publication>"]
        place_of_publication_tag = f""
        if type(place_of_publication) == str and place_of_publication != "":
            place_of_publication_tag = f"<place_of_publication>{place_of_publication}</place_of_publication>\n"         
        
        country_of_publication = this_line["<country_of_publication>"]
        country_of_publication_tag = f""
        if type(country_of_publication) == str and country_of_publication != "":
            country_of_publication_tag = f"<country_of_publication>{country_of_publication}</country_of_publication>\n"                  
        
        shelfmark = this_line["<shelfmark>"]
        shelfmark_tag = f""
        if type(shelfmark) == str and shelfmark != "":
            shelfmark_tag = f"<shelfmark>{shelfmark}</shelfmark>\n"         
        
        pagination = this_line["<pagination>"]
        pagination_tag = f""
        if type(pagination) == str and pagination != "":
            pagination_tag = f"<pagination>{pagination}</pagination>\n"         
          
        #################################################################
                   
        imprint = this_line["<imprint>"]
        if type(imprint)!= str: imprint = "unknown"   
    
        startdate = this_line["<startdate>"]
        if type(startdate) == str:
            if startdate == "": startdate = "unknown"
        else:
            if math.isnan(startdate): startdate = "unknown" 
            else: startdate = int(startdate)  
    
        enddate = this_line["<enddate>"]
        if type(enddate) == str:
            if enddate == "": enddate = "unknown"
        else:
            if math.isnan(enddate): enddate = "unknown" 
            else: enddate = int(enddate)        
    
        displaydate = this_line["<displaydate>"]
        if type(displaydate) == str:
            if displaydate == "": displaydate = "unknown"
        else:
            if math.isnan(displaydate): displaydate = "unknown" 
            else: displaydate = int(displaydate) 
  
        
        source_library = this_line["<source_library>"] 
        source_collection = this_line["<source_collection>"]
        language = decimal_encode_for_xml(this_line["<language>"]) # Latin & Hebrew 
    
        illustrations_tag = f""
        if len(self.illustration_type_list) != 0:
            
            illustrations_tag = f"<illustrations>\n"
            for illustration in self.illustration_type_list:
                illustrations_tag = f"{illustrations_tag}\t<illustration>{illustration}</illustration>\n"
        
            illustrations_tag = f"{illustrations_tag}</illustrations>\n"   
    
        link_tag = f""
        if len(self.my_book.items) > 1: # If there are other Items in this Book
            link_tag = f"<linksec>\n"
            
            for item_name, item, in self.my_book.items.items():
                if item_name != self.name:
                    other_item_line = self.df_rec_search.loc[item_name]
                    this_link_id = item_name
                    this_link_title = decimal_encode_for_xml(other_item_line["<title>"])
                    
                    link_tag = f"{link_tag}\t<link>\n\t\t<linktitle>{this_link_title}</linktitle>\n"
                    link_tag = f"{link_tag}\t\t<linkid>{this_link_id}</linkid>\n\t</link>\n"
       
            link_tag = f"{link_tag}</linksec>\n" 
            
        rec_search = (   f"\n\n<rec_search>\n<pqid>{pqid}</pqid>\n"
                        f"<title>{title}</title>\n"
                        f"<author_main>\n\t<author_name>{author_main}</author_name>\n\t<author_corrected>{author_corrected}</author_corrected>\n\t<author_uninverted>{author_uninverted}</author_uninverted>\n</author_main>\n"
                        
                        f"<startdate>{startdate}</startdate>\n"
                        f"<enddate>{enddate}</enddate>\n"
                        f"<displaydate>{displaydate}</displaydate>\n"
                        
                        f"<imprint>{imprint}</imprint>\n"
                        
                        # shelfmark publisher_printer place_of_publication country_of_publication pagination
                        # All of these have no visible tag if no value
                        f"{shelfmark_tag}"
                        f"{publisher_printer_tag}"                        
                        f"{place_of_publication_tag}"                        
                        f"{country_of_publication_tag}"                        
                        f"{pagination_tag}"
                        
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
        
        
        