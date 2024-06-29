"""

A helper file for main_metadata.py
Helps with the XML layout

"""

from pathlib import Path 
import math

# The front matter of the book
def get_nsic_line(this_row, index):
    image_name = this_row["Image name"]
    file_name = Path(image_name).stem
    
    itemimagefile_element = f"<itemimagefile1>{file_name}</itemimagefile1>"
    imagenumber_element = f"<imagenumber>{index}</imagenumber>"
    
    order = 0
    if file_name[-2:] == "1L": order = 1
    if file_name[-2:] == "2R": order = 2
    if file_name[-2:] == "3L": order = 3
    if file_name[-2:] == "4R": order = 4
    
    #print(file_name[-2:])
    
    order_element = f"<order>{order}</order>"
    
    colour = this_row["Colour"]
    if type(colour).__name__ != "str": colour = "None"
    colour_element = f"<colour>{colour}</colour>"
        
    page_type = this_row["Page Type"]
    if type(page_type).__name__ != "str": page_type = "None"
    page_type_element = f"<pagetype>{page_type}</pagetype>"
        
    this_line = f"<itemimage>\n\t{itemimagefile_element}{order_element}{imagenumber_element}{colour_element}{page_type_element}\n</itemimage>"
    return  this_line


####################################################################
# Regular body of the book
def get_page_line(this_row, image_index, book_index):
    image_name = this_row["Image name"]
    file_name = Path(image_name).stem
    
    illustration_type_list = []
    
    itemimagefile_element = f"<itemimagefile1>{file_name}</itemimagefile1>"
    imagenumber_element = f"<imagenumber>{image_index}</imagenumber>"
    
    order = book_index # because of the weird NISC numbering
   
    order_element = f"<order>{order}</order>"
    
    colour = this_row["Colour"]
    if type(colour).__name__ != "str": colour = "None"
    colour_element = f"<colour>{colour}</colour>"
        
    page_type = this_row["Page Type"]
    if type(page_type).__name__ != "str": page_type = "None"
    page_type_element = f"<pagetype>{page_type}</pagetype>"
        
    # This is the basic line - all tabs included even if value "None"
    this_line = f"{itemimagefile_element}{order_element}{imagenumber_element}{colour_element}{page_type_element}"
    
    ###########################################################################################
    # elements below here are not included in the output if they have no value
    page_number = this_row["Page number"]  
    if type(page_number).__name__ != "str": 
        order_label_element = ""
    else:
        order_label_element = f"<orderlabel>{page_number}</orderlabel>"
    
    this_line = f"{this_line}{order_label_element}"
    
    #######################
    # illustration_type_1 to illustration_type_5
    all_illustration_type = ""
    for i in range(1, 6):
        
        illustration_type = this_row[f"illustration_type_{i}"]  
        instances_of = this_row[f"instances_of_{i}"]
        
        # Collect the illustration types for the metadata
        if type(illustration_type) == str: illustration_type_list.append(illustration_type)
        
        if type(illustration_type).__name__ != "str": 
            illustration_type = ""
        else:
            if math.isnan(instances_of) != True:
                instances_of = int(instances_of)
            illustration_type = f'<pagecontent number="{instances_of}">{illustration_type}</pagecontent>'
            
        all_illustration_type = f"{all_illustration_type}{illustration_type}"
    
    this_line = f"{this_line}{all_illustration_type}"


    #######################
    translation = this_row["translation"]  
    if type(translation).__name__ != "str": 
        translation = ""
    else:
        translation = f"<translation>{translation}</translation>"
    
    this_line = f"{this_line}{translation}"

    # Wrap it in tags
    this_line = f"<itemimage>\n\t{this_line}\n</itemimage>\n"
    
    return  (this_line, illustration_type_list)


####################################################################
"""

"""
def get_front_tags(item_name, df_rec_search):
    front_tags = f"<rec>\n\n<itemid>{item_name}</itemid>\n\n<subscription>\n\t<unit>unpublished</unit>\n\t<country>uni</country>\n</subscription>\n\n<itemimagefiles>\n"
    return front_tags

"""
    use item_name as index into rec_data.csv
    https://docs.google.com/spreadsheets/d/1hmBUjLONWi2XRhz45K3lJuNRNXr3IPJR/edit?gid=2000716270#gid=2000716270

"""
def get_back_tags(item_name, df_rec_search, illustration_list):
    
    illustration_list = list(set(illustration_list))
    
    # print(illustration_list)
    
    this_line = df_rec_search.loc[item_name]
    
    pqid = this_line["<pqid>"]
    title = this_line["<title>"]
    author_main = this_line["<author_main>"]
    author_corrected = author_main
    author_uninverted = author_main
    
    imprint = this_line["<imprint>"]
    if type(imprint).__name__ != "str": imprint = "unknown"
    
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
    if len(illustration_list) != 0:
        
        illustrations_tag = f"<illustrations>\n"
        for illustration in illustration_list:
            illustrations_tag = f"{illustrations_tag}\t<illustration>{illustration}</illustration>\n"
    
        illustrations_tag = f"{illustrations_tag}</illustrations>\n"
    
    link_tag = f""
    links = this_line["<link>"]
    if type(links) == str:
        links_list = list(eval(links))
        
        link_tag = f"<linksec>\n"
        # Annoying thing with single tuple/link
        if type(links_list[0]) == str:
            this_link_title = links_list[0]
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
        
    
    back_tags = (   f"</itemimagefiles>\n\n<rec_search>\n<pqid>{pqid}</pqid>\n"
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
    
    return back_tags











