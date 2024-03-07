from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI,OpenAI
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import openai
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationSummaryMemory
from utils import pymongoConnect
import json





app = FastAPI()

load_dotenv()
openai_key=os.getenv("OPENAI_KEY")
weaviate_key=os.getenv("weaviate_key")
weaviate_cluster=os.getenv("weaviate_cluster")
weaviate_url=os.getenv("weaviate_url")

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
    filesize:str
    filetype:str
    weaviateprocess:bool
    filepath:str  



@app.post("/submit")
async def submit_question(question: QuestionDetails):
    """
    API endpoint to submit a question.
    """
    print("Inside submit")
    print(question)
    if question.talktodata==False:
        print(question)
        response= basicQandA(question)
        return (response)
    else:
       print("do weaviate coding here")  
    
@app.post("/addtomongo")
async def AddMongoRecord(data: mongodata):
    print(data)
    collection= pymongoConnect("MyDataDetail","mycollection")
    data=data.dict()
    inserted_data=collection.insert_one(data)
    object_id=inserted_data.inserted_id
    return({"id":str(object_id)})

    






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
    




#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000)


