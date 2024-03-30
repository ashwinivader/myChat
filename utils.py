import streamlit as st
import os
from dotenv import load_dotenv
import pymongo
import json
import mimetypes
from langchain_openai import ChatOpenAI,OpenAI
from pydantic import BaseModel
from datamodels import QuestionDetails,mongodata


load_dotenv()
pymongoendpt=os.getenv("pymongodb")
datafolder=os.getenv("MYFILESDIR")
load_dotenv()
openai_key=os.getenv("OPENAI_KEY")




def save_files(uploaded_files):
    # Create a directory to store uploaded files
    if not os.path.exists(datafolder):
        os.makedirs(datafolder)

    if uploaded_files is not None:
    # Save the file to the uploads directory
        with open(os.path.join(datafolder, uploaded_files.name), "wb") as f:
            f.write(uploaded_files.read())
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


def get_files(directory):
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



def basicQandA(question: QuestionDetails):
      print("Do normal llm")
      model = ChatOpenAI(openai_api_key=openai_key,model="gpt-4")
      #way1
      """ans=model.invoke(question.question_text)
      print(ans)
      response_data = {
          "answer": ans}
      return (response_data)"""

      #way2      
      """prompt = ChatPromptTemplate.from_messages([
               ("system", "You are world class AI assistnet."),
               ("user", "{input}")
                ] )
      # Initialize the output parser
      output_parser = StrOutputParser()
      # Create the LangChain pipeline
      chain =  prompt | model | output_parser
      # Invoke the chain with a question
      ans = chain.invoke({"input":question.question_text})
      print(ans)
      response_data = {
          "answer": ans}
      return (response_data)"""
    
      # way3 using history passed in brower   
      history=question.history
      input=question.question_text
      print("*************history*******************")
      print(question)
      # create prompt template which is history of context and input
      prompt_template =f"""You are a conversational AI bot. Maintain a formal tone in your answers.
         Context of the communication is : {history}.
         Using this context provide summarised answer to the below quesion. 
         Question: {input}
         if question is not related to context
         provided ignore the context and use your knowlege and answer in short.
        """
      print(prompt_template)
      llm=OpenAI(api_key=os.getenv("OPENAI_KEY"),temperature=0)
      ans=llm.invoke(prompt_template)
      model=None      
      print(ans)
      return (ans)

def getCollectionData(user: str):
    print(user)
    collection= pymongoConnect("MyDataDetail",user)
    # Query the collection to get data for the specified user
    query = {"user": user}
    cursor = collection.find(query)
    result = [doc for doc in cursor]
    collection=None   
    return result




     

     


     
     
