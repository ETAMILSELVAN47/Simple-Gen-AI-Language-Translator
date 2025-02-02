import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from fastapi import FastAPI
from langserve import add_routes
import uvicorn




#1.Create a prompt
system_prompt_template='Translate the following to {language}'
user_prompt_template='{text}'
prompt=ChatPromptTemplate.from_messages(
    [
        ('system',system_prompt_template),        
        ('user',user_prompt_template)
    ]
)

#2.Create a model
model=ChatGroq(model='gemma2-9b-It',groq_api_key=os.getenv(key='GROQ_API_KEY'))

#3.output parser
parser=StrOutputParser()

#4.chain
chain=prompt|model|parser


## App definition:
app=FastAPI(title='GenAI Language Translator App',
        version='1.0',
        description='A simple language translator GenAI app using LangChain'
        )


## add routes
add_routes(app=app,runnable=chain,path='/chain')

if __name__=='__main__':
    uvicorn.run(app=app,host='localhost',port=5000)
