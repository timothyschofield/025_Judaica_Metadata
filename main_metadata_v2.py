"""
    File: main_metadata_v2.py
    Author: Tim Schofield
    Date: 27 June 2024   
    
    This uses a double scan - first we collect the data from the input speadsheet and in a hierachical data structure of Books, Items and NISCs.
    Once we have the structured data we can go through it and write out the metadata xml in a sensible fashion.

    This is specificaly required to address the problem of linked data, where items in a book/volume need to know about one another's existance.
    A single scan is no good for this, because the earlyer items in a book/volume do not know about later items because the data has not been collected yet.

    OOPs approch required

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
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from helper_functions_judaica import get_file_timestamp

from App import App

input_folder = Path(f"metadata_input")
input_file = Path(f"Illustration METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - BENCHMARK.csv")
input_path = Path(f"{input_folder}/{input_file}")

output_folder = Path(f"metadata_output")
output_file = Path(f"judaica_xml_{get_file_timestamp()}")
output_path = Path(f"{output_folder}/{output_file}")

if os.path.exists(input_path) != True:
    print(f"ERROR: {input_path} file does not exits")
    exit()
else:
    print(f"READING: {input_path}")       

df_metadata = pd.read_csv(input_path)

app1 = App(df_metadata=df_metadata, output_path=output_path)

























