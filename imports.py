
# import requests
# import io,sys
# from PIL import Image
# from openai import OpenAI
# import streamlit as st
# import os,re
# import pandas as pd
# import numpy as np
# from langchain.prompts import PromptTemplate
# import base64
# import json
# import pickle
# import uuid
# from random import randint, randrange
# from streamlit_image_select import image_select
# from streamlit_extras.stateful_button import button as st_extra_button
# # from api_key import Api_key
# from config import size_dalle2,size_dalle3
# from st_keyup import st_keyup
# import torch
# import  numpy as np
# # from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
# from config import API_URL, headers
# import time
# import replicate
# from config import replicate_ai_token
# from config import image_path
# from important_keys import openai_key,clipdrop_key

# def bytes_to_image(byte_array):
#     image = Image.open(io.BytesIO(byte_array))
#     return image


# #custom dowload utton for streamlit 
# #becasue streamlit's download button reloads the page which costs th credit

# def custom_download_button(object_to_download, download_filename, button_text, pickle_it=False):
#     """
#     Generates a link to download the given object_to_download.
#     Params:
#     ------
#     object_to_download:  The object to be downloaded.
#     download_filename (str): filename and extension of file. e.g. mydata.csv,
#     some_txt_output.txt download_link_text (str): Text to display for download
#     link.
#     button_text (str): Text to display on download button (e.g. 'click here to download file')
#     pickle_it (bool): If True, pickle file.
#     Returns:
#     -------
#     (str): the anchor tag to download object_to_download
#     Examples:
#     --------
#     download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
#     download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
#     """
#     if pickle_it:
#         try:
#             object_to_download = pickle.dumps(object_to_download)
#         except pickle.PicklingError as e:
#             st.write(e)
#             return None

#     else:
#         if isinstance(object_to_download, bytes):
#             pass

#         elif isinstance(object_to_download, pd.DataFrame):
#             object_to_download = object_to_download.to_csv(index=False)

#         # Try JSON encode for everything else
#         else:
#             object_to_download = json.dumps(object_to_download)

#     try:
#         # some strings <-> bytes conversions necessary here
#         b64 = base64.b64encode(object_to_download.encode()).decode()

#     except AttributeError as e:
#         b64 = base64.b64encode(object_to_download).decode()

#     button_uuid = str(uuid.uuid4()).replace('-', '')
#     button_id = re.sub('\d+', '', button_uuid)

#     custom_css = f""" 
#         <style>
#             #{button_id} {{
#                 background-color: rgb(255, 255, 255);
#                 color: rgb(38, 39, 48);
#                 padding: 0.25em 0.38em;
#                 position: relative;
#                 text-decoration: none;
#                 border-radius: 4px;
#                 border-width: 1px;
#                 border-style: solid;
#                 border-color: rgb(230, 234, 241);
#                 border-image: initial;
#             }} 
#             #{button_id}:hover {{
#                 border-color: rgb(246, 51, 102);
#                 color: rgb(246, 51, 102);
#             }}
#             #{button_id}:active {{
#                 box-shadow: none;
#                 background-color: rgb(246, 51, 102);
#                 color: white;
#                 }}
#         </style> """

#     dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

#     return dl_link


# def background_changer_api(uploaded_file,text):
#     bytes_data = uploaded_file.getvalue()
            
#     r = requests.post('https://clipdrop-api.co/replace-background/v1',
#     files = {
#         'image_file': ('check1.jpg',bytes_data, 'image/jpeg'),
#         },
#     data = { 'prompt': text },
#     headers = { 'x-api-key': clipdrop_key}
#     )

#     return r

