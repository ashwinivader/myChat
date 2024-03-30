from fastapi import FastAPI,Request,HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI,OpenAI
from dotenv import load_dotenv
import os
#from langchain_core.output_parsers import StrOutputParser
#from langchain_core.prompts import ChatPromptTemplate
#from langchain_community.llms import openai
#from langchain.memory import ConversationBufferMemory
#from langchain.chains import LLMChain
#from langchain.prompts import PromptTemplate
#from langchain.chains.conversation.memory import ConversationSummaryMemory
from utils import pymongoConnect,basicQandA
import json
from datamodels import QuestionDetails,mongodata,UpdateTableRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse





app = FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

load_dotenv()
openai_key=os.getenv("OPENAI_KEY")
weaviate_key=os.getenv("weaviate_key")
weaviate_cluster=os.getenv("weaviate_cluster")
weaviate_url=os.getenv("weaviate_url")


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
    collection= pymongoConnect("MyDataDetail",data.user)
    data=data.dict()
    inserted_data=collection.insert_one(data)
    object_id=inserted_data.inserted_id
    collection=None
    return({"id":str(object_id)})


@app.post("/updatetables")
def insert_mongo_table(data:UpdateTableRequest):
    collection= pymongoConnect("MyDataDetail",data.user)
    result= collection.update_one(
        {"user":data.user},
        {"$set": {"sqltablename": data.sqltablename}} 
    )
    collection=None  

@app.get("/getcollectiondata/{user}")
async def getCollectionData(request: Request,user: str):
    try:
        print(user)
        collection= pymongoConnect("MyDataDetail",user)

        # Query the collection to get data for the specified user
        query = {"user": user}
        result = collection.find_one(query)
        for document in result:
            print(document)     
        if result is None:
            return JSONResponse(content={"message": "Data not found for the specified user"}, status_code=404)
        return JSONResponse(content=document, status_code=200)   
    except Exception as e:
        raise HTTPException(status_code=500,detail="failed to retrive results")




@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}






#if __name__ == "__main__":
#    import uvicorn
#uvicorn services:app --reload
#    uvicorn.run(app, host=localhost, port=8000)


