import os
import shutil
import streamlit as st
from PIL import Image
from lyzr import ChatBot

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

# Set Streamlit page configuration
st.set_page_config(
    page_title="Lyzr",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title(" Domain Name Generator ")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown(" ")

# Function to remove existing files in the directory
def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")

# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)

# Function to implement RAG Lyzr Chatbot
def rag_implementation(file_path):
    # Check the file extension
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".pdf":
        # Initialize the PDF Lyzr ChatBot
        rag = ChatBot.pdf_chat(
            input_files=[file_path],
            llm_params={"model": "gpt-4"},
        )
    elif file_extension.lower() == ".docx":
        # Initialize the DOCX Lyzr ChatBot
        rag = ChatBot.docx_chat(
            input_files=[file_path],
            llm_params={"model": "gpt-4"},
        )
    else:
        # Handle unsupported file types
        raise ValueError("Unsupported file type. Only PDF and DOCX files are supported.")

    return rag

# Function to get Lyzr response
def advisor_response(file_path, preferred_genre):
    rag = rag_implementation(file_path)
    prompt = f""" 
You are an Expert DOMAIN NAME GENERATOR. Your task is to CREATE domain names that PERFECTLY MATCH the uploaded company profile and the user's  preferred keyword.

Here is your DETAILED INSTRUCTION SET:

1. First, IDENTIFY key attributes of the company that will serve as the foundation for your domain name suggestions.
2. ENSURE each domain name you develop is MEMORABLE by choosing SIMPLE and CATCHY names that are easy to spell and recall.
3. Prioritize BREVITY by generating domain names that are SHORT and UNCOMPLICATED, facilitating quick recognition and ease of use.
4. INCORPORATE the user entered {preferred_keywords}) seamlessly into each domain name to enhance search engine optimization (SEO) and relevance.
5. CONDUCT a SEARCH to VERIFY that your suggested domain names do not violate any trademarks, thus ensuring they are legally sound.
6. For every domain name you create, ASSIGN an appropriate DOMAIN EXTENSION such as .com, .net, or .org that aligns with the company's image and purpose.
7. Think about LONG-TERM GROWTH when selecting a domain name, making sure it allows for FUTURE EXPANSION without restrictions.
8. AVOID including hyphens and numbers in your domain names to maintain simplicity unless they are integral to the brand.

For EACH generated DOMAIN NAME with the preferred keyword , IMMEDIATELY SPECIFY a matching DOMAIN EXTENSION and a DESCRIPTION before proceeding to generate the next one.
Display ALL these in a organized TABULAR format."""
    response = rag.chat(prompt)
    return response.response

# File upload widget
uploaded_file = st.file_uploader("Upload your company documentation here⬇️", type=["pdf", "docx"])

# If a file is uploaded
if uploaded_file is not None:
    # Save the uploaded file to the data directory
    file_path = os.path.join(data_directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    # Display the path of the stored file
    st.success("File successfully saved")

    # Get preferred genre after file upload
    preferred_keywords = st.text_input("Enter your preferred keyword")

    # Generate advice button
    if st.button("Generate"):
        automatic_response = advisor_response(file_path, preferred_keywords)
        st.markdown(automatic_response)

# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """Experience the seamless integration of Lyzr's ChatBot as you refine your documents with ease. For any inquiries or issues, please contact Lyzr."""
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )
