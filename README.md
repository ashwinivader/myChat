# myChat
# Add .env
OPENAI_KEY=
weaviate_key=
weaviate_cluster=
weaviate_url=

# to start uvicorn on local
uvicorn api:app --reload

# to start streamlit app
 streamlit run app.py
