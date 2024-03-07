import streamlit as st
import os
from dotenv import load_dotenv
import pymongo
import json
import mimetypes
from pydantic import BaseModel

load_dotenv()
pymongoendpt=os.getenv("pymongodb")
datafolder=os.getenv("MYFILESDIR")




def save_files_to_myfiles(uploaded_files):
    # Display uploaded files
    if uploaded_files:
        for file in uploaded_files:
            file_details = {"filename": file.name, "filetype": file.type, "filesize": file.size}
            st.write(file_details)
        if st.button("Upload_files"):
           # Ensure 'MyFiles' folder exists
              if not os.path.exists(datafolder):
                  os.makedirs(datafolder)
              for uploaded_file in uploaded_files:
              # Copy each uploaded file to the 'MyFiles' folder
                 file_path = os.path.join(datafolder, uploaded_file.name)
                 with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
    else:
                   st.warning("Please upload a file first.")

def pymongoConnect(dbname,collectionm):
     # Connect to MongoDB (make sure MongoDB is running on localhost:27017)     
     client = pymongo.MongoClient(pymongoendpt)
     # Select database (create it if it doesn't exist)
     db = client[dbname]
      # Select collection (create it if it doesn't exist)
     collection = db[collectionm]
     return collection


def get_files_in_directory(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return []   
    # Get all files in the directory
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename)) 
    return files
     

     


     
     
