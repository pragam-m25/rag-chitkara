
# from langchain_google_genai import ChatGoogleGenerativeAI 
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# from dotenv import load_dotenv
# from langchain_chroma import Chroma
# from langchain_core.prompts import PromptTemplate

# from langchain_core.runnables import RunnablePassthrough



# load_dotenv()


# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=0
# )

# def load_vector_store():
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="gemini-embedding-001"
#     )

#     return Chroma(
#         embedding_function=embeddings,
#         persist_directory="chroma_db",
#         collection_name="rag"
#     )

# vector_store = load_vector_store()

# def create_retriever(vector_store):
#     return vector_store.as_retriever(
#         search_kwargs={"k": 4}
#     )


# retriever = create_retriever(vector_store)

# def format_docs(docs):
#     return "\n\n".join(
#         doc.page_content
#         for doc in docs
#     )

# # def retrieve_context(retriever, question):
# #     docs = retriever.invoke(question)

# #     context = "\n\n".join(
# #         doc.page_content
# #         for doc in docs
# #     )

# #     return context, docs

# context, docs = retrieve_context(
#     retriever,
#     question
# )


# for i, doc in enumerate(docs, 1):
#     print(f"\n--- Retrieved Document {i} ---")
#     print(doc.page_content)
#     print(doc.metadata)


# prompt = PromptTemplate(
#     template='''
#     You are a Chitkara University assistant.

#     Answer the question using ONLY the provided context.

#    Do not use your own knowledge.
#     Do not infer missing facts.
#     Do not combine unrelated information to create an answer.
#     If the context does not contain enough information, clearly say that the information was not found in the available Chitkara documents.

#     Context:
#     {context}

#     Question:
#     {question}
#     ''' ,

#     input_variables=["context","question"] 
# )

# final_prompt = prompt.format(
#     context = context ,
#     question = question 
# )

# response = llm.invoke(final_prompt)

# print(response.content)


from fastapi import FastAPI
from pydantic import BaseModel

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableLambda

from dotenv import load_dotenv




load_dotenv()


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Chitkara RAG Assistant",
    description="RAG-based assistant for Chitkara University documents",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)




def load_vector_store():

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    return Chroma(
        embedding_function=embeddings,
        persist_directory="chroma_db",
        collection_name="rag"
    )


vector_store = load_vector_store()




def create_retriever(vector_store):

    return vector_store.as_retriever(
        search_kwargs={"k": 4}
    )


retriever = create_retriever(vector_store)




def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )



prompt = PromptTemplate(
    template="""
You are a Chitkara University assistant.

Answer the question using ONLY the provided context.

Do not use your own knowledge.
Do not infer missing facts.
Do not combine unrelated information to create an answer.

If the context does not contain enough information,
clearly say that the information was not found
in the available Chitkara documents.

Context:
{context}

Question:
{question}
""",
    input_variables=["context", "question"]
)



def build_context(data):
    docs = data["docs"]

    return format_docs(docs)


rag_chain = (
    {
        "docs": retriever,
        "question": RunnablePassthrough()
    }
    | RunnableLambda(
        lambda x: {
            "docs": x["docs"],
            "context": format_docs(x["docs"]),
            "question": x["question"]
        }
    )
)



class QuestionRequest(BaseModel):

    question: str




@app.get("/")
def root():

    return {
        "message": "Chitkara RAG Assistant is running"
    }




@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = rag_chain.invoke(request.question)

    final_prompt = prompt.format(
        context=result["context"],
        question=result["question"]
    )

    response = llm.invoke(final_prompt)

    sources = []

    for doc in result["docs"]:
        sources.append({
            "document": doc.metadata.get("source"),
            "page": doc.metadata.get("page_label")
        })

    return {
        "question": request.question,
        "answer": response.content,
        "sources": sources
    }