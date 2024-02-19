import streamlit as st
import requests
from pydantic import BaseModel
from uuid import uuid4
import os
from dotenv import load_dotenv
from  utils import pymongoConnect,get_files_in_directory,save_files_to_myfiles
import mimetypes


session_id = int(uuid4().int)
load_dotenv()
pymongoendpt=os.getenv("pymongodb")
datafolder=os.getenv("MYFILESDIR")


class QuestionDetails(BaseModel):
    question_text: str
    user:str
    session_id: int
    talktodata:bool
    history:str


class mongodata(BaseModel):
    user:str
    session_id: str
    filename:str
    filesize: str
    filetype:str 
    weaviateprocess:bool
    filepath:str  

 

# Set page title and background color
st.markdown(
    """
    <style>
    body {
        background-color: #FFFFE0; /* light yellow */
        color: #000000;
    }
    .title {
        color: #FF5733;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #1E90FF; /* blue */
    }
    .stTextInput>div>div>div>input {
        border: 2px solid #FFD700; /* gold */
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Add title with custom color and center alignment
st.title("My ChatBot")

# Add Ask Question text input
#ask_question = st.text_input("Ask Question")

# Add toggle button and position it left side center
st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        display: flex;
        align-items: center;
        justify-content: flex-start;
    
    }
    </style>
    """,
    unsafe_allow_html=True
)




talk_to_data = st.sidebar.checkbox("Talk to my data", False, key='toggle')

# If toggle button is True, show file upload button
if talk_to_data:
    st.write("Upload your files for personalise Q and A")
    selectedFiles = st.file_uploader("Choose files", accept_multiple_files=True,label_visibility="hidden")
    save_files_to_myfiles(selectedFiles)
    #Add meta data to pymongo
    collection= pymongoConnect("MyDataDetail","mycollection")
    files_in_directory = get_files_in_directory(datafolder)
    directory_path = os.path.join(os.path.dirname(__file__), datafolder)
    files_in_directory = get_files_in_directory(datafolder)
    for names in  files_in_directory:
       filename= os.path.basename(names)
       file_type, _ = mimetypes.guess_type(names)
       file_size = os.path.getsize(names) 
       filedata = mongodata(
                   user="ashwini",
                   session_id = session_id,
                   filename=filename,                
                   filesize=file_size,
                   filetype=file_type,
                   weaviateprocess=0,
                   filepath = os.path.join(directory_path, filename)
                   )  
       response = requests.post("http://localhost:8000/addtomongo", json=filedata.dict())
       print(response)
       

    


# Add CSS styling for the text input container
st.markdown(
    """
    <style>
    .text-input-container {
        display: inline-block; /* Ensure container and input field are inline */
        width: 100%; /* Allow container to expand to fit input field */
        border: 2px solid #000000; /* Black border */
        border-radius: 5px; /* Rounded border */
        padding: 5px; /* Add some padding */
        margin-bottom: 40px; /* Add margin at the bottom */
    }
    .text-input-container input {
        width: 100%; /* Ensure input field takes up entire width of container */
        border: #0000FF; /* Remove default input field border */
        outline: none; /* Remove default input field focus outline */
        padding: 0; /* Remove default input field padding */
        margin: 0; /* Remove default input field margin */
        background-color: transparent; /* Set input field background to transparent */
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Text input for asking a question
userquestion = st.text_input("Ask Question")



if st.button("Submit"):
    #talktodata=talk_to_data

    if 'history' in st.session_state:
        print(st.session_state.history)
        question = QuestionDetails(
                   question_text=str(userquestion),
                   user="ashwini",
                   session_id = session_id,
                   talktodata=bool(talk_to_data),
                   history=str(st.session_state.history))
    else:
        question = QuestionDetails(
                   question_text=str(userquestion),
                   user="ashwini",
                   session_id = session_id,
                   talktodata=bool(talk_to_data),
                   history="")


    

    #print(question.json())
    print(question.dict())


    if 'history' not in st.session_state:
            st.session_state.history=str(question.question_text)
    else :        
            st.session_state.history=st.session_state.history+ str(question.question_text)

    response = requests.post("http://localhost:8000/submit", json=question.dict())
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        st.success("Question submitted successfully!")
        api_response = response.json()
        st.write(api_response)
        st.session_state.history=st.session_state.history+" "+str(api_response["text"])
        #if 'history' not in st.session_state:
        #    st.session_state.history=str(api_response["input"])+str(api_response["text"])
        #else: 
        #   st.session_state.history=st.session_state.history+ str(api_response["input"])+str(api_response["text"])



    else:
        st.error("Failed to submit question. Please try again.")




