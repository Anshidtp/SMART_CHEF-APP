import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()   ## initializing/loading all enviroment variable

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt,image[0]])
    return response.text

def input_image_setup(file):
    # Check if a file has been uploaded
    if file is not None:
        # Read the file into bytes
        bytes_data = file.getvalue()

        image_parts = [
            {
                "mime_type": file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Initializing streamlit



# Setting the page config to change the page title and layout
st.set_page_config(page_title="Smart_CHEF", layout="wide")

# Use st.markdown to add some custom styles to the page and widgets
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    font-weight: bold;
}
.uploaded-image {
    border: 2px solid #cccccc;
    border-radius: 5px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)
# Using custom styles in headers or text
st.markdown('<p class="big-font">Smart_CHEF: SnapToCook</p>', unsafe_allow_html=True)

# File uploader allows user to add their own image
upload_file = st.file_uploader("Click here to upload the image", type=["jpg", "jpeg", "png"])
image = ""

if upload_file is not None:
    image = Image.open(upload_file)

    # Display the uploaded image with a custom CSS class for styling
    st.image(image, caption='Uploaded Image', use_column_width=True )

    # Optionally, display a message that the image was successfully uploaded
    st.success("Image uploaded successfully!")

submit = st.button("Tell me about the Recipe")


if submit:
    if image:
        # Placeholder for functionality to analyze the image and suggest a recipe
        st.write("Analyzing the recipe...")
        # Imagine here goes your code or function call to analyze the image and fetch the recipe
    else:
        # Prompt user to upload an image if they haven't already
        st.error("Please upload an image to proceed.")

 #Prompt setup       
input_prompt="""
You are an expert and experiened  chef where you need to see the food items from the image
               and provide the cooking recipe details of every food items with calories intake
               is below format

               Title of the Recipe:make it as header 
               Introduction : a brief idea of the dish at a glance
               Prep Time and Cook Time:
               Ingredients: List all ingredients in the order they will be used
               Instructions: Step-by-step directions on how to make the dish

            finally you can also mention the food is healthy or not and also mention 
            pencentage of carbo hydrate , sugur ,fats,fibers and required things 
            for our diet


"""

# if sbmit is clicked 
if submit:
    image_data = input_image_setup(upload_file)
    result = get_gemini_response(input_prompt,image_data)
    st.write(result)


