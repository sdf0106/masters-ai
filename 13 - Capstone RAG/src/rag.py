from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

def setup_rag_chain(vectorstore, prompt):
    retriever = vectorstore.as_retriever(kwargs={"k": 4})
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("human", "{question}")
    ])

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt_template},
        return_source_documents=True
    )

    return qa_chain
