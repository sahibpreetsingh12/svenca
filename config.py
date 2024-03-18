import os
from dotenv import load_dotenv
size_dalle2 = ['256x256', '512x512', '1024x1024']
size_dalle3 = ['1024x1024', '1024x1792', '1792x1024']
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": "Bearer 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"}

replicate_ai_token= os.getenv('REPLICATE_API_TOKEN')
image_path='extras/searcly.png'

