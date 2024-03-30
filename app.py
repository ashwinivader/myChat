import streamlit as st
import requests
from pydantic import BaseModel
from uuid import uuid4
import os
from dotenv import load_dotenv
from  utils import pymongoConnect,get_files,save_files
import mimetypes
from datamodels import QuestionDetails,mongodata,UpdateTableRequest
from langchain_openai import ChatOpenAI,OpenAI
from sql import sqlcreate
import sqlalchemy
from pandasai.llm.openai import OpenAI  
from pandasai import SmartDataframe
import pandas as pd
from pandasai.connectors import MySQLConnector
from chat import mychat



load_dotenv()
pymongoendpt=os.getenv("pymongodb")
datafolder=os.getenv("MYFILESDIR")


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
session_id = int(uuid4().int)

# If toggle button is True, show file upload button
if talk_to_data==True:
    talk_to_data=False
    st.write("Upload your file for on personalise Q and A")
    selectedFiles = st.file_uploader("Choose files", accept_multiple_files=False,label_visibility="hidden")
    if selectedFiles is not None:
       save_files(selectedFiles)
       files_in_directory = get_files(datafolder)
       print("========Files=================")
       print(files_in_directory)
       for names in  files_in_directory:
            filename= os.path.basename(names)
            file_type, _ = mimetypes.guess_type(names)
            file_size = os.path.getsize(names) 
            filedata = mongodata(
                   user="ashwini",
                   filename=filename,                
                   filesize=file_size,
                   filetype=file_type,
                   weaviateprocess=0,
                   filepath = os.path.join(os.path.join(os.path.dirname(__file__), datafolder), filename),
                   sqltablename="",
                   sessionid=str(session_id),
                   dbname="ashwini"
                   )  
            response = requests.post("http://localhost:8000/addtomongo", json=filedata.dict())
            print(response)
            if response.status_code==200 :
                sqloperation=sqlcreate("ashwini")
                df=sqloperation.create_dataframe_from_excel(filedata.filepath)
                tbname= os.path.splitext(os.path.basename(filename))[0]
                print("++++++++++++++++filename+++++++++++++++++++++")
                print(filename)
                #filepath=os.path.join(os.path.join(os.path.dirname(__file__), datafolder), filename)
                tbname=sqloperation.create_table(df,tbname)
                print(filename,filedata.user,tbname)
                UpdateTableRequest(filename=filename,user=filedata.user,sqltablename=tbname)
                response = requests.post("http://localhost:8000/updatetables", json=UpdateTableRequest(filename=filename,user=filedata.user,sqltablename=tbname).dict())
                chat=mychat(filedata.user)



            
       
       

    


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
    if 'history' in st.session_state:
        print(st.session_state.history)
        question = QuestionDetails(
                   question_text=str(userquestion),
                   user="ashwini",
                   talktodata=bool(talk_to_data),
                   history=str(st.session_state.history),
                   sessionid=session_id)
    else:
        question = QuestionDetails(
                   question_text=str(userquestion),
                   user="ashwini",
                   talktodata=bool(talk_to_data),
                   history="",
                   sessionid=session_id)
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
        print(response)
        st.success("Question submitted successfully!")
        api_response = response.json()
        st.write(api_response)
        st.session_state.history=st.session_state.history+" "+ api_response[int(len(api_response) * 0.70):]

    else:
        st.error("Failed to submit question. Please try again.")




