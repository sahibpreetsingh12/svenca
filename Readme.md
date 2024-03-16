# Svenca AI Images from Text

### Problem Statement :-
In the dynamic world of fashion, brands invest substantial 
resources in creating visually appealing representations of their
models adorned in diverse clothing. The traditional approach
involves extensive photoshoots and model selection, incurring
significant costs. However, with the advent of AI-powered 
text-to-image generation tools, there is an opportunity to 
revolutionize the fashion industry's content creation process.
##### Challenge:
Brands, big and small, face the ongoing challenge of managing tight budgets while striving to maintain a strong visual presence in the market. The need for diverse and high-quality visual content demands substantial financial investments in models, clothing, and professional photoshoots.


### Solution Adopted :-
In addressing the challenges faced by fashion and apparel
brands in managing costs while maintaining a compelling visual 
presence, our proposed solution leverages state-of-the-art AI
models specifically designed for text-to-image generation.

1. **Stable Diffusion**, released in 2022, is a text-to-image AI that generates stunningly realistic visuals. It blends diffusion processes with U-Net architecture, progressively refining noise into detailed images matching your text prompts. Key to its success:

   * Hybrid diffusion model for efficient noise removal and detail generation.
   * Frozen text encoder extracting semantic information from the prompt, ensuring consistency.
   * Lightweight U-Net for fast generation times.
   

2. **Midjourney**, also launched in 2022, takes a text-to-image approach distinct from Stable Diffusion. Instead of refining noise, it learns image representations from text, generating dreamlike visions. Users refine these with iterative feedback, guiding the model to their desired outcome. Its custom architecture remains mysterious, but hints suggest attention mechanisms and transformer-based modules. Midjourney excels in artistic flair and user-controlled refinement, making it ideal for concept art, design, and creative exploration. 


However, even with their impressive capabilities, both Stable Diffusion and Midjourney exhibit limitations. They sometimes struggle to capture intricate details, especially when faced with complex prompts or scenarios demanding a high level of precision. Additionally, achieving optimal results often requires users to possess a deep understanding of prompt formulation, making the process somewhat challenging and less accessible.

3. **DALL-E3**: In contrast, our solution places a spotlight on DALL-E3, a state-of-the-art text-to-image generation model. DALL-E3 not only meets but exceeds the expectations set by its counterparts. Its architecture excels in handling complex prompts with precision and capturing minute details with remarkable accuracy, making it an ideal choice for the nuanced world of fashion and apparel.

**Why DALL-E3 over others :**

While Stable Diffusion, Midjourney, Dreambooth and other Open-Source models are impressive in image generation, but sometimes fail to capture the minute details. Even if they get the details right by further fine-tuning, they require the user to be very good at writing prompts. Whereas, Dall-e3 can perform very well on complex prompts and is precise at following the minute details. For better results, after entering the prompt, it is sent to gpt-4 for further enhancement and then finally sent to Dall-e3 for image generation.

### How to Start :-
* git clone the project
* go to project directory
* Open terminal and type"pip install -r requirements.txt"
* In main.py, line number 4, os.environ['OPENAI_API_KEY'] = "enter your openai api key"

* Run the app using "streamlit run _path_to_directory_ main.py"
### Files and its uses :-
main.py :- streamlit text to image app

query.py :- To check relevancy of user's prompt to product using gpt 3.5 turbo.


### Realtime Gen :
Realtime Gen is a feature which generates images in an instant. Model keeps creating
images till the user types.

**Solution Adopted :**
Sdxl turbo model by Stability AI is a text to image model which generates images in realtime.
Around 16 gb of VRam is required to run the model. So, alternative was found at Replicate.com where inference api for the model was found.

Only drawback of this inference api was that it took huge amount of time to generate its first image.
  
After researching, i found out that when the models are not used frequently, they are shut down to 
save the resources. So when the model form replicate is called,if it is not a already running model,
it first boots up and then is available to use.
https://replicate.com/docs/how-does-replicate-work#cold-boots

### Fun AI Generation :
Fun AI Generation is a feature which allows the user to get images in different styles such
as Anime, Natural, Manga, Digital-Art, Pixel-Art.

**Solution Adopted:**
First Inference Api of Stable Diffusion 2 was Used which had some unpromising results. On the contrary, 
the sdxl-emoji model from replicate had some very good results. 

Sdxl-emoji's results may seem promising, but it still has issues while generating images.
Even with the help of negative prompts, sdxl-emoji is more prone to error while generating images
which result in bad anatomy, mutated limbs and body parts.
the comparison of both is shared here in this drive link.
https://drive.google.com/drive/folders/1odxY8pE6ps38kqt5CBXTVky3LUHiIhvp?usp=sharing



_Disclaimers :-_
There can be certain scenarios where AI generated images 
can be off from the expected output. 
