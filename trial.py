import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI,OpenAI

from langchain_community.llms import openai
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def main():
    load_dotenv()
    openai_key = os.getenv("OPENAI_KEY")

    print("Do normal llm")
    """
    model = ChatOpenAI(model="gpt-4", api_key=openai_key,temperature=0)
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class AI assistnet."),
    ("user", "{input}"),
    ] )
    # Initialize the output parser
    output_parser = StrOutputParser()
    # Create the LangChain pipeline
    chain =  prompt | model | output_parser
    # Invoke the chain with a question
    ans = chain.invoke({"input":"What is SQL?"})
    print(ans)"""

memory= ConversationBufferMemory()
# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template="""You are a conversational AI bot. Maintain a formal tone in your answers.
    Conversational history: {history}
    Human: {input}
    AI: 
    """,
)


llm=OpenAI(api_key=os.getenv("OPENAI_KEY"),temperature=0)
conversation_chain=LLMChain(llm=llm,prompt=prompt_template,memory=memory,verbose=True)

print(conversation_chain("hi"))
print(conversation_chain("how are you"))
print(conversation_chain("Tell me"))
if __name__ == "__main__":
    main()