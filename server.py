from flask import Flask, jsonify, request, Response
from flask_cors import CORS

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="gemma")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a chatbot assistant. You may be asked to write code or commands, in which case you should reply with only code or commands and no additonal descriptive words.."),
    ("user", "{input}")
])
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

##

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/', methods=['GET', 'POST'])
def query():
    query_request = request.get_json()
    if query_request and 'query' in query_request:
        query_value = query_request['query']
    else:
        print("No 'query' property found in the request JSON.")
        return "Missing 'query' property", 400

    def generate():
        for chunks in chain.stream({"input": query_value}):
            print(chunks, end="", flush=True)
            yield chunks
    return app.response_class(generate(), content_type='text/plain')
        
if __name__ == "__main__":
    app.run(port=4000)
