"""
    File: main_metadata_v2.py
    Author: Tim Schofield
    Date: 27 June 2024   
    
    This uses a double scan - first we collect the data from the input speadsheet in a hierachical data structure of Books, Items and NISCs.
    Once we have the structured data we can go through it and write out the metadata xml in a sane fashion.

    This is specificaly required to address the problem of linked data, where items in a book/volume need to know about one another's existance.
    A single scan is no good for this, because the earlyer items in a book/volume can not know about later items because the data has not yet been collected.
    The double scan is also required for collecting volumeimagefiles info, which includes all the imagedata for all Items in a Book and
    is inserted into the XML for each Item.

    OOPs approach required

    Required file hierachy

    uni-ucl-jud-0015052                             <<<<< this the Volume or Book level
        
        uni-ucl-jud-0015052-000                     <<<<< this Item folder contains no XML but there is an ocr folder
            ocr
            *.jpg
            *.tiff
    
        uni-ucl-jud-0015052-001                     <<<<< this is the Item level - contains NISC data for this Item + data for all XML files in this item
            uni-ucl-jud-0015052-001.xml             <<<<< this is the metadata file for Item 001
            *.jpg
            *.tiff
            ocr
                uni-ucl-jud-0015052-001-0001L.xml
                uni-ucl-jud-0015052-001-0001R.xml
                ...
                
         uni-ucl-jud-0015052-002                    <<<<<<< second Item in Book
            uni-ucl-jud-0015052-002.xml             <<<<< this is the metadata file for item 002
            
            etc.
             
        ... 

"""
from pathlib import Path 
import pandas as pd
import os
from helper_functions_judaica import get_file_timestamp

from metadata_package import App

input_folder = Path(f"metadata_input")

# 0050296
# input_file = Path(f"Illustration METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - BENCHMARK.csv")
# input_file = Path(f"Illustration METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240807-2.csv")
# input_file = Path(f"Illustration METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240807-3.csv")
# input_file = Path(f"Illustration METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240807-4.csv")
# input_file = Path(f"Illustration METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240809.csv") # compilation
# input_file = Path(f"Illustration METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240927.csv") 
input_file = Path(f"Illustration METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20241011.csv") 


input_path = Path(f"{input_folder}/{input_file}")

# re_search_input_file = Path(f"_rec search_ METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - Benchmark.csv")
# re_search_input_file = Path(f"_rec search_ METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240807-2.csv")
# re_search_input_file = Path(f"_rec search_ METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240807-3.csv")
# re_search_input_file = Path(f"_rec search_ METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240807-4.csv")
# re_search_input_file = Path(f"_rec search_ METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240809.csv") # compilation
# re_search_input_file = Path(f"_rec search_ METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20240927.csv") 
re_search_input_file = Path(f"_rec search_ METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - 20241011.csv") 


re_search_input_path = Path(f"{input_folder}/{re_search_input_file}")

output_path = Path(f"metadata_output/judaica_xml_{get_file_timestamp()}")

if os.path.exists(input_path) != True:
    print(f"ERROR: {input_path} file does not exits")
    exit()
else:
    print(f"READING: {input_path}")       

if os.path.exists(re_search_input_path) != True:
    print(f"ERROR: {re_search_input_path} file does not exits")
    exit()
else:
    print(f"READING: {re_search_input_path}") 

df_metadata = pd.read_csv(input_path)

df_rec_search = pd.read_csv(re_search_input_path)
df_rec_search.set_index("Item name", inplace=True)


app1 = App(df_metadata=df_metadata, df_rec_search=df_rec_search, output_path=output_path)



