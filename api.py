from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI


app = FastAPI()


class QuestionDetails(BaseModel):
    question_text: str
    user:str
    session_id: int
    talktodata:bool


@app.post("/submit")
async def submit_question(question: QuestionDetails):
    """
    API endpoint to submit a question.
    """
    print(question)
    if question.talktodata==False:
        print("Do normal llm")
        llm = ChatOpenAI(openai_api_key="")

    else:
        print("do weaviate one")   

    return question.json()





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)