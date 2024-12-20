
def log_message(message):
    print(message)
    
    error_log_dir = Path(f"error_logs")
    error_log_dir.mkdir(parents = True, exist_ok = True)
    error_log_path = Path(f"{error_log_dir}/error_log.txt")
    
    # flag "a" is open to append file
    with open(error_log_path, "a") as f:
        f.write(f"{get_file_timestamp()}: {message}\n")


import html
# You do not pass XML in here, just data you want to be carried in XML
def decimal_encode_for_xml(data_in):
  
  # print(f"In decimal_encode_for_xml ****{data_in}****")
  
  html_escaped = html.escape(data_in) # this will turn & into &amp;

  html_escaped = html_escaped.replace("&amp;","&#38;") # Is this OK? 2024-10-25

  binary_encoded = html_escaped.encode('ascii', 'xmlcharrefreplace') # this turns ü into &#252;

  non_binary = binary_encoded.decode("utf-8") # Gets rid of the leading 'b'
  
  non_binary = non_binary.replace("&#x27;","&#39;") # Is this OK? 2024-10-25
  
  return non_binary

import xml.etree.ElementTree as ET
def validate_xml(xml_text):
    try:
        ET.fromstring(xml_text)
        return True, "The XML is well-formed."
    except ET.ParseError as e:
        return False, f"XML is not well-formed: {e}"


import base64
# Function to base64 encode an image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
from datetime import datetime
# e.g. 2024-05-18T06-53-26
def get_file_timestamp():
  current_dateTime = datetime.now()
  year = current_dateTime.year
  month = current_dateTime.month
  day = current_dateTime.day
  hour = current_dateTime.hour
  minute = current_dateTime.minute
  second = current_dateTime.second
  return f"{year}-{month:02}-{day:02}T{hour:02}-{minute:02}-{second:02}"
    
import json
def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True
 
import torch
def get_torch_cuda_info():
  print("-----------------------")
  print("torch version", torch.__version__)
  print("CUDA avaliable", torch.cuda.is_available())
  print("torch.CUDA version", torch.version.cuda)
  print("-----------------------")

  if torch.cuda.is_available():
      print('__CUDNN VERSION:', torch.backends.cudnn.version())   # CUDA Deep Neural Networks
      print('__Number CUDA Devices:', torch.cuda.device_count())
      print('__CUDA Device Name:',torch.cuda.get_device_name(0))
      print('__CUDA Device Total Memory [GB]:',torch.cuda.get_device_properties(0).total_memory/1e9)
      print("-----------------------")

import pandas as pd
from pathlib import Path
def create_and_save_dataframe(output_list, key_list_with_logging, output_path_name):
  output_df = pd.DataFrame(output_list)

  if key_list_with_logging != []:
    output_df = output_df[key_list_with_logging]  # Bring reorder dataframe to bring source url and error column to the front

  output_path = Path(output_path_name)
  with open(output_path, "w") as f:
    output_df.to_csv(f, index=False)
    
    
def make_payload(model, prompt, url_request, num_tokens):
  
  payload = {
    "model": model,
    "logprobs": False,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "temperature": "0.0",
            "text": prompt
          },
          {
            "type": "image_url",
            "image_url": {"url": url_request}
          }
        ]
      }
    ],
    "max_tokens": num_tokens
  } 
  
  return payload
    