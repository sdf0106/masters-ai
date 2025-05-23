import os


def ask_question(chain, question):
    response = chain.invoke({"question": question})
    answer = response["answer"].strip()
    documents = response['source_documents']

    if "<INFO_NOT_FOUND_IN_PDFS>" in answer or not documents:
        return "<INFO_NOT_FOUND_IN_PDFS>", None

    sources = set()
    for doc in documents:
        source_name = os.path.basename(doc.metadata.get('source', 'unknown'))
        page = doc.metadata.get('page', 'Unknown')
        sources.add(f"{source_name}, page {page + 1}")

    sources = list(set(sources))
    sources_text = "; ".join(sources)

    return answer, sources_text
