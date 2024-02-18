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
 


@app.post("/submit")
async def submit_question(question: QuestionDetails):
    """
    API endpoint to submit a question.
    """
    print("Inside submit")
    print(question)

    if question.talktodata==False:
        response= basicQandA(question)
        return (response)

    else:
       print("do weaviate one")  
    

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
    
      #conversational chain    
      memory= ConversationBufferMemory()
      #history=question.history
      print("*************history*******************")
      #print(history)
      # Define the prompt template
      prompt_template = PromptTemplate(
         input_variables=["history","input"],
         template="""You are a conversational AI bot. Maintain a formal tone in your answers.
         Conversational history: {history}
         Human: {input}
          AI: 
          """
          )
      llm=OpenAI(api_key=os.getenv("OPENAI_KEY"),temperature=0)
      conversation_chain=LLMChain(llm=llm,prompt=prompt_template,memory=memory,verbose=True)
      if len(question.history) ==0:
         memory.save_context({"input":question.question_text}, {"output": ""})
      else:
         #memory.save_context({"input":question.question_text}, {"output": question.history})
         memory.save_context( {"output": question.history})
       
      ans=conversation_chain(question.question_text)
      print(ans)
      return (ans)
    


#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000)


