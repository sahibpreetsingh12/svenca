
import requests
import io,sys
from PIL import Image
from openai import OpenAI
import streamlit as st
import os,re
import pandas as pd
import numpy as np
from langchain.prompts import PromptTemplate
import base64
import json
import pickle
import uuid
from random import randint, randrange
from streamlit_image_select import image_select
from streamlit_extras.stateful_button import button as st_extra_button
from config import size_dalle2,size_dalle3
from st_keyup import st_keyup
import torch
import  numpy as np
from dotenv import load_dotenv
from config import API_URL, headers
import time
import replicate
from config import replicate_ai_token
from config import image_path

load_dotenv()
def bytes_to_image(byte_array):
    image = Image.open(io.BytesIO(byte_array))
    return image


#custom dowload utton for streamlit 
#becasue streamlit's download button reloads the page which costs and  credit

def custom_download_button(object_to_download, download_filename, button_text, pickle_it=False):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link


def background_changer_api(uploaded_file,text):
    bytes_data = uploaded_file.getvalue()
            
    r = requests.post('https://clipdrop-api.co/replace-background/v1',
    files = {
        'image_file': ('check1.jpg',bytes_data, 'image/jpeg'),
        },
    data = { 'prompt': text },
    headers = { 'x-api-key': clipdrop_key}
    )

    return r


# Set OpenAI API key
os.environ['OPENAI_API_KEY'] =  os.getenv('openai_key')
os.environ["REPLICATE_API_TOKEN"] = os.getenv('REPLICATE_API_TOKEN')
clipdrop_key = os.getenv('clipdrop_key')


# Create an OpenAI client
client = OpenAI()


# Function to generate images using the OpenAI API
def generate_using_api(input_prompt, n):
    """This function inputs a prompt and outputs image URLs"""
    try:
        # Call OpenAI API to generate images based on the input prompt and parameters selected in ui
        response = client.images.generate(
            model=model,
            style="natural",
            prompt=input_prompt,
            size=size,
            quality=option,
            n=num,
        )

        # Extract image URLs from the API response
        image_urls = [item.url for item in response.data]

        return image_urls

    except Exception as e:
        # Handle exceptions and display an error message
        st.write('Oops! Write Appropriate prompt', e)


# Sidebar Dropdown menu to navigate between different sections
choice = st.sidebar.selectbox('Select your choice', ['Home Page', 'Text To Image', 'Fun AI Generation!','Background Replacer'])

# Handling different sections based on the user's choice
if choice == 'Home Page':
    # Home Page content
    st.title('AI Image Generation Using Svenca')
    with st.expander('What is Svenca ?'):
        st.write("""Svenca is a cutting-edge text-to-image tool specially designed for fashion aficionados.
         Our innovative platform utilizes the powerful AI text-to-image engine to bring your fashion dreams to life. 
         With Svenca, you have the power to conceptualize and visualize the perfect dress or apparel by simply typing
          in your desires.""")
    st.write('How It Works :')
    st.write("""Input Your Desires:
     Whether it's a dreamy wedding gown, a casual summer dress, or a trendy streetwear 
    ensemble,
     let your imagination flow through your fingertips. Type in your specific prompts about the dress or apparel you 
     have in mind.""")
    st.image(image_path)
    st.title('See the next generation visual product discovery!')

elif choice == 'Text To Image':
    # Section for Text to Image functionality
    st.title('AI Image Generation Using Svenca')
    with st.expander('What is Svenca ?'):
        st.write("""Svenca is a cutting-edge text-to-image tool specially designed for fashion aficionados.
         Our innovative platform utilizes the powerful AI text-to-image engine to bring your fashion dreams to life. 
         With Svenca, you have the power to conceptualize and visualize the perfect dress or apparel by simply typing in 
         your desires.""")

    st.subheader('Visualize your Fashion Fantasies !')

    # Text input for user to input their desires
    input_text = st.text_input('What do you have in mind today?', value=None, key='input_text')

    # Container to display generated images
    image_container = st.empty()

    # Slider to choose the number of images to generate
    num = st.slider(label='Number of Images:', min_value=1, max_value=10)

    # Set the model and size based on the number of images
    size_list = []


    # Generate images based on user input
    if num == 1:
        # if st.button('Generate Image'):
            if input_text is not None:
                # if num == 1:
                    model = 'dall-e-3'
                    size_list = size_dalle3
                # Dropdown to select the size of an image
            size = st.selectbox('Select Image Size', size_list)
            # Dropdown to select quality of an image
            option = st.radio(label="Quality", options=('standard', 'hd'))
            st.info(input_text)
            if st.button('Generate Image'):
                # Call function to generate images using the OpenAI API
                image_urls = generate_using_api(input_text, num)
                print('image_urls==', image_urls)

                # Display the generated images
                for image_url in image_urls:
                    st.image(image_url)



    elif num > 1:
            if st.button(label="Generate"):
                output = replicate.run(
                    "fofr/sdxl-emoji:dee76b5afde21b0f01ed7925f0665b7e879c50ee718c5f78a9d38e04d523cc5e",
                    input={
                        "prompt": f"{input_text}, 8k, full hd, raw, dslr",
                        "negative_prompt": "unreal,digital,cartoon,deformed face, bad quality, ugly, deformed hands, deformed body, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation",
                        "num_outputs": num
                    }
                )
                print(output)
                for image in output:
                    st.image(image=image)

    else:
        st.write('Please Enter a Prompt')

    # Real-time generation toggle
    on = st.toggle(label="RealTime Generation")

    if on:
        # Function to handle keypress events for real-time generation

        os.environ["REPLICATE_API_TOKEN"] = replicate_ai_token
        value = st_keyup("Enter Text", debounce=500, key="2")

        start = time.time()
        # using sdxl turbo inference api for realtime generation
        output = replicate.run(
            "dhanushreddy291/sdxl-turbo:53a8078c87ad900402a246bf5e724fa7538cf15c76b0a22753594af58850a0e3",
            input={
                "prompt": value,
                "num_outputs": 1,
                "negative_prompt": "3d, cgi, render, bad quality, normal quality, malformed, deformed face,deformed body, deformed hand, nfsw, anime, animated",
                "num_inference_steps": 3,

            }
        )
        print(output)
        st.image(image=output)
        end = time.time()
        print(end - start)
        # st.write(end - start)


elif choice == 'Fun AI Generation!':
    # Section for Fun AI Generation functionality
    st.header('Let Us Fuel Your Imagination🔥 ')
    text = st.text_input(label="Let's have fun!", key='text',)
    st.write('Choose Your Style :')
    # dropdown for image style
    style_choice = st.selectbox(label='Select Style', options=['Natural', 'Anime', 'Digital-Art', 'Pixel-Art', 'Manga', 'Neo Punk'])
    # Add extra spaces for generate button
    st.text('')
    st.text('')
    st.text('')
    _, col7, _ = st.columns([1, 1, 1])

    # If style choice is natural, prompt is sent to dall-e-3
    if style_choice == "Natural":
        prompt = f'{style_choice}: {text}, 8k, high quality'

        if col7.button(label="Generate"):
            with st.spinner(text='Cooking the best shot .... :coffee:'):
                try:

                    output = replicate.run(
                        "fofr/sdxl-emoji:dee76b5afde21b0f01ed7925f0665b7e879c50ee718c5f78a9d38e04d523cc5e",
                        input={
                            "prompt": prompt,
                            "negative_prompt": "deformed face, ugly, deformed hands, deformed limbs, anime, digital"
                        }
                    )
                except:
                    st.header('Seems some NSFW Prompt or Backend Issue on our side')
                    st.image(image='images/error.jpeg')

            print(output)
            
            st.image(image=output)

            number_random = randint(100000,1000000)
              
            name_of_image = f'Svenca_{number_random}.png'

            #its a custom download button
            download_button_str = custom_download_button(output[0], name_of_image, 'Download')

            st.markdown(download_button_str, unsafe_allow_html=True)

    else:
        if col7.button(label="Generate Fun Images :smile:"):
            with st.spinner(text='Fun shots coming :smile: .... :coffee:'):
                try:
                    # The prompt includes style selected by the user and the prompt
                    prompt = f'{style_choice}: {text}'

                    # Stable diffusion 2 inference API (config.py)
                    output = replicate.run(
                        "fofr/sdxl-emoji:dee76b5afde21b0f01ed7925f0665b7e879c50ee718c5f78a9d38e04d523cc5e",
                        input={
                            "prompt": prompt,
                            "negative_prompt": "deformed face, bad quality, ugly, deformed hands, deformed body, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation"
                        }
                    )
                    print(output)
                    st.image(image=output)

                    number_random = randint(100000,1000000)
              
                    name_of_image = f'Svenca_{number_random}.png'

                    #its a custom download button
                    download_button_str = custom_download_button(output[0], name_of_image, 'Download')

                    st.markdown(download_button_str, unsafe_allow_html=True)
                except:
                    st.header('Seems some NSFW Prompt or Backend Issue on our side')
                    st.image(image='images/error.jpeg')

                
elif choice=='Background Replacer':
     # Section for Fun AI Generation functionality
    st.header('Imagine a Backgound 🔥 and Create it')


    col1, col2, col3 = st.columns(3)
    # col1,col2 = st.columns(2)

    with col1:
        button1 = st_extra_button('Vehicle',key="Vehicle")

    with col2:
        button2 = st_extra_button('Gadgets',key="Gadgets")

    with col3:
        button3 = st_extra_button('Other Products',key="Products")

    common_prompt = PromptTemplate.from_template(
    """You have to take care and have to make realistic image and no animation, no black and white
        no blurred image and disformed images . 
        Please make High quality, Ultra Realistic Image and no text on the image
        Now put the image of the {product_type} 
        involved in a {background_selected} background""")
   
    uncommon_prompt =  PromptTemplate.from_template("""
        Please change set the background based on {background_selected} for a {product_type}""")
    
    ## to check which button is selected
    ## for image selection refer -> https://shorturl.at/lqMOQ
    if button1:
            
            img = "images/vehicle/downtown.jpeg"
            img = image_select(
            label="Select a Background for Your Vehicle",
            images=[
                "images/vehicle/downtown.jpeg",
                "images/vehicle/mountain.jpeg",
                "images/vehicle/garage.jpg"
    
            ],
            captions=["Downtown New York", "Mountains", "Garage"] )

            # if some background is selected then only create prompt template
            if img: 

                if 'downtown' in img:
                    text = uncommon_prompt.format(product_type="Vehicle", background_selected="Downtown view with tall buildigs in a sunny day")
                elif 'mountain' in img:
                    text = uncommon_prompt.format(product_type="Vehicle", background_selected="Snow covered Mountain view with Sun shine  ")
                elif 'garage' in img:
                    text = common_prompt.format(product_type="Vehicle", background_selected="Ultra realistic,4k, HD garage background in high quality,clean background")

            
                # st.text(f'Vehicle was selected {button1} and {text}')

    elif button2:

        img = "images/Gadget/kitchen.jpeg"
        img = image_select(
        label="Select a Background for Your Gadget",
        images=[
            "images/Gadget/kitchen.jpeg",
            "images/Gadget/bedroom.webp",
            "images/Gadget/living.avif"

        ],
        captions=["Kicthen Shelf", "Bedroom", "Living"] )

        # if some background is selected then only create prompt template
        if img: 

            if 'kitchen' in img:
                text = uncommon_prompt.format(product_type="Gadget", background_selected="a cozy marble kitchen and wood cupboards")
            elif 'bedroom' in img:
                text = uncommon_prompt.format(product_type="Gadget", background_selected="a bedroom background with blue bed and blue pillows and windows")
            elif 'living' in img:
                text = uncommon_prompt.format(product_type="Gadget", background_selected="a huge living room with brown sofa and LED television")

        # st.text(f'Gadegts was selected {button2}')


    elif button3:


        img = "images/Gadget/living.avif"
        img = image_select(
        label="Select a Background for Your product",
        images=[
            "images/products/kitchen2.avif",
            "images/Gadget/bedroom.webp",
            "images/Gadget/living.avif"

        ],
        captions=["Kicthen Shelf", "Bedroom", "Living"] )

        # if some background is selected then only create prompt template
        if img: 

            if 'kitchen' in img:
                text = uncommon_prompt.format(product_type="product", background_selected="a cozy marble kitchen and wood cupboards")
            elif 'bedroom' in img:
                text = uncommon_prompt.format(product_type="product", background_selected="a bedroom background with blue bed and blue pillows and windows")
            elif 'living' in img:
                text = uncommon_prompt.format(product_type="product", background_selected="a huge living room with brown sofa and LED television")

      
    
    st.markdown('##### Recommendation - Use High Quality Images for BEST RESULTS ')
    uploaded_file = st.file_uploader("Choose an Image (webp,jpeg,jpg,png) only")

    on = st.toggle('Prompt - Premium Feature - :money_with_wings: ')
    if on:
        text1 = st.text_input(label="", key='text',)

        text = f"""You have to take care and have to make realistic image and no animation, no black and white
        no blurred image and disformed images . Now make changes based on {text1}"""
    

        #if file is uploaded
        if len(text1)!=0 and (on) and uploaded_file:
            
        # To read file as bytes:
            print(text,"--->",text1,type(text1),len(text1))
            
            with st.spinner(text="Making best Backgorund according to your images :)"):
                r = background_changer_api(uploaded_file=uploaded_file,text=text)
            
           
            # if positive reposnse
            if r.status_code==200:
                
                number_random = randint(100000,1000000)
                # using the output from api
                byte_data = r.content
                image = bytes_to_image(byte_data)

                st.image(image, caption=text1)
                name_of_image = f'Svenca_{number_random}.png'

                # st.text(f"You are left with -> {r.headers['x-remaining-credits']}")

                #its a custom download button
                download_button_str = custom_download_button(byte_data, name_of_image, 'Download')
                st.markdown(download_button_str, unsafe_allow_html=True)

                           
            elif r.status_code==400:
                st.text('Image file might not be uploaded')
                st.text('or Input Image format is not valid')
                st.text('or Image resolution too big')
            elif r.status_code==402:
                st.text('Your account has no remaining credits, you can buy more in your account page.')
            elif r.status_code==406:
                st.text('Headers not acceptable')
            elif r.status_code==429:
                st.text(""" Too many requests, blocked by the rate limiter.
                            You should space out your requests in time or contact us to increase your quota.""")
            else:
                st.text("This seems a bug in our website")

        else:
            st.text(' ')

    else:
        # if button1 or button2:
        if button1 or button2 or button3:

            if text and uploaded_file:
                
                
                with st.spinner(text="Making best Backgorund according to your images :)"):
                    r = background_changer_api(uploaded_file=uploaded_file,text=text)

                if r.status_code==200:
                    
                    number_random = randint(100000,1000000)
                    # using the output from api
                    byte_data = r.content
                    image = bytes_to_image(byte_data)

                    st.image(image)
                    name_of_image = f'Svenca_{number_random}.png'

                    # st.text(f"You are left with -> {r.headers['x-remaining-credits']}")

                    #its a custom download button
                    download_button_str = custom_download_button(byte_data, name_of_image, 'Download')
                    st.markdown(download_button_str, unsafe_allow_html=True)

        else:
            st.text("")

        



























